import os
import hmac
import hashlib
import json
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request, status
from dotenv import load_dotenv
import razorpay
import models
import security
from pydantic import BaseModel

load_dotenv()

router = APIRouter()

# ── Razorpay Client ───────────────────────────────────────────────────────────

RAZORPAY_KEY_ID      = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET  = os.getenv("RAZORPAY_KEY_SECRET")
RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET")

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

PRICING_PLANS = {
    "Pro":        {"amount": 150000, "currency": "INR", "description": "Fleet Pro — ₹1,500/month"},
    "Enterprise": {"amount": 500000, "currency": "INR", "description": "Enterprise Node — ₹5,000/month"},
}


# ── Request / Response Schemas ────────────────────────────────────────────────

class CreateOrderRequest(BaseModel):
    plan_type: str                  # "Pro" | "Enterprise"
    email: Optional[str] = None
    contact: Optional[str] = None


class CreateOrderResponse(BaseModel):
    order_id: str
    amount: int
    currency: str
    plan_type: str


# ── ENDPOINT 1: Create Order ──────────────────────────────────────────────────

@router.post("/create-order", response_model=CreateOrderResponse)
async def create_order(
    request: CreateOrderRequest,
    current_user: models.User = Depends(security.get_current_user),
):
    if request.plan_type not in PRICING_PLANS:
        raise HTTPException(status_code=400, detail="Invalid plan_type. Must be 'Pro' or 'Enterprise'.")

    if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
        raise HTTPException(status_code=500, detail="Razorpay keys not configured on server.")

    plan = PRICING_PLANS[request.plan_type]
    receipt = f"sub_{(current_user.email or 'anon').replace('@','_')}_{request.plan_type}"

    try:
        order = client.order.create(data={
            "amount":   plan["amount"],
            "currency": plan["currency"],
            "receipt":  receipt[:40],           # Razorpay receipt max 40 chars
            "notes": {
                "plan_type":   request.plan_type,
                "email":       current_user.email,
                "description": plan["description"],
            },
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Razorpay order creation failed: {e}")

    return CreateOrderResponse(
        order_id=order["id"],
        amount=order["amount"],
        currency=order["currency"],
        plan_type=request.plan_type,
    )


# ── ENDPOINT 2: Webhook (HMAC-verified) ───────────────────────────────────────

@router.post("/webhook")
async def razorpay_webhook(request: Request):
    if not RAZORPAY_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="RAZORPAY_WEBHOOK_SECRET not configured.")

    raw_body  = await request.body()
    signature = request.headers.get("x-razorpay-signature", "")

    # Verify HMAC-SHA256 signature
    expected = hmac.new(
        RAZORPAY_WEBHOOK_SECRET.encode(),
        raw_body,
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected, signature):
        raise HTTPException(status_code=401, detail="Webhook signature verification failed.")

    try:
        body = json.loads(raw_body)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid webhook payload.")

    event   = body.get("event")
    payload = body.get("payload", {})

    try:
        if event == "payment.captured":
            payment_entity = payload.get("payment", {}).get("entity", {})
            notes          = payment_entity.get("notes", {})
            email          = notes.get("email") or payment_entity.get("email")
            plan_type      = notes.get("plan_type")
            customer_id    = payment_entity.get("customer_id")
            if email and plan_type:
                user = await models.User.find_one(models.User.email == email)
                if user:
                    user.subscription_plan = plan_type
                    user.is_active = True
                    if customer_id:
                        user.razorpay_customer_id = customer_id
                    await user.save()
                    print(f"[Webhook] {email} → upgraded to {plan_type}")

        elif event == "subscription.charged":
            sub_entity = payload.get("subscription", {}).get("entity", {})
            notes      = sub_entity.get("notes", {})
            email      = notes.get("email") or sub_entity.get("email")
            plan_type  = notes.get("plan_type") or "Pro"
            if email:
                user = await models.User.find_one(models.User.email == email)
                if user:
                    user.subscription_plan = plan_type
                    user.is_active = True
                    await user.save()
                    print(f"[Webhook] {email} → subscription.charged → {plan_type}")

        elif event == "subscription.halted":
            sub_entity = payload.get("subscription", {}).get("entity", {})
            notes      = sub_entity.get("notes", {})
            email      = notes.get("email") or sub_entity.get("email")
            if email:
                user = await models.User.find_one(models.User.email == email)
                if user:
                    user.subscription_plan = "Free"
                    await user.save()
                    print(f"[Webhook] {email} → subscription.halted → downgraded to Free")

    except Exception as e:
        # Always return 200 to stop Razorpay from retrying
        print(f"[Webhook] Error processing event '{event}': {e}")
        return {"status": "received_with_error", "event": event}

    return {"status": "ok", "event": event}


# ── ENDPOINT 3: Subscription Status ──────────────────────────────────────────

@router.get("/subscription-status")
async def get_subscription_status(
    current_user: models.User = Depends(security.get_current_user),
):
    return {
        "email":                current_user.email,
        "subscription_plan":    current_user.subscription_plan,
        "is_active":            current_user.is_active,
        "razorpay_customer_id": current_user.razorpay_customer_id,
    }


# ── ENDPOINT 4: Admin Downgrade ───────────────────────────────────────────────

@router.post("/downgrade/{user_email}")
async def downgrade_subscription(
    user_email: str,
    admin: models.User = Depends(security.require_admin),
):
    user = await models.User.find_one(models.User.email == user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    user.subscription_plan = "Free"
    await user.save()
    return {"message": f"{user.email} downgraded to Free", "plan": user.subscription_plan}
