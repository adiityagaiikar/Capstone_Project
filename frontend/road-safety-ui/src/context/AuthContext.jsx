import React, { createContext, useContext, useEffect, useMemo, useState } from "react";
import { api } from "../api";

const TOKEN_KEY = "token";
const AuthContext = createContext(null);

function decodeTokenPayload(token) {
  try {
    const payloadPart = token.split(".")[1];
    const normalized = payloadPart.replace(/-/g, "+").replace(/_/g, "/");
    const json = atob(normalized);
    return JSON.parse(json);
  } catch {
    return null;
  }
}

function mapRole(user, payloadRole) {
  if (typeof user?.is_admin === "boolean") {
    return user.is_admin ? "admin" : "user";
  }
  return payloadRole || "user";
}

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem(TOKEN_KEY));
  const [user, setUser] = useState(null);
  const [role, setRole] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const bootstrap = async () => {
      if (!token) {
        setLoading(false);
        return;
      }

      const payload = decodeTokenPayload(token);
      try {
        const me = await api.getCurrentUser(token);
        setUser(me);
        setRole(mapRole(me, payload?.role));
      } catch {
        localStorage.removeItem(TOKEN_KEY);
        setToken(null);
        setUser(null);
        setRole(null);
      } finally {
        setLoading(false);
      }
    };

    bootstrap();
  }, [token]);

  const login = async ({ email, password, selectedRole }) => {
    const auth = await api.login(email, password, selectedRole || "user");
    localStorage.setItem(TOKEN_KEY, auth.access_token);
    setToken(auth.access_token);

    const payload = decodeTokenPayload(auth.access_token);
    const me = await api.getCurrentUser(auth.access_token);
    const resolvedRole = mapRole(me, payload?.role);

    setUser(me);
    setRole(resolvedRole);
    return { user: me, role: resolvedRole };
  };

  const signup = async ({ fullname, email, password }) => {
    await api.register(fullname, email, password);
    return login({ email, password, selectedRole: "user" });
  };

  // Mock helper for local demos; still stores a JWT-like token key.
  const mockLogin = ({ selectedRole = "user" }) => {
    const mockToken = `mock.${btoa(JSON.stringify({ sub: `${selectedRole}@local.dev`, role: selectedRole }))}.sig`;
    const mockUser = {
      id: selectedRole === "admin" ? 1 : 2,
      fullname: selectedRole === "admin" ? "Mock Admin" : "Mock User",
      email: `${selectedRole}@local.dev`,
      is_admin: selectedRole === "admin",
      is_active: true,
      subscription_plan: "Free",
      razorpay_customer_id: null,
    };

    localStorage.setItem(TOKEN_KEY, mockToken);
    setToken(mockToken);
    setUser(mockUser);
    setRole(selectedRole);
    return { user: mockUser, role: selectedRole };
  };

  const logout = () => {
    localStorage.removeItem(TOKEN_KEY);
    setToken(null);
    setUser(null);
    setRole(null);
    api.logout().catch(() => null);
  };

  const value = useMemo(
    () => ({
      token,
      user,
      role,
      loading,
      isAuthenticated: Boolean(token),
      login,
      signup,
      mockLogin,
      logout,
    }),
    [token, user, role, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
