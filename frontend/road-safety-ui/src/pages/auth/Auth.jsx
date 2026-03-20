import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ShieldAlert, ArrowRight, Github, Lock, Mail, User } from "lucide-react";
import { api } from "../../api";

export default function Auth() {
    const [isLogin, setIsLogin] = useState(true);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [fullname, setFullname] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        try {
            if (isLogin) {
                const data = await api.login(email, password);
                localStorage.setItem("token", data.access_token);
                navigate("/");
            } else {
                await api.register(fullname, email, password);
                const data = await api.login(email, password);
                localStorage.setItem("token", data.access_token);
                navigate("/");
            }
        } catch (err) {
            setError(err.message || "An error occurred");
        }
    };

    return (
        <div className="min-h-screen w-full flex bg-[#09090b] text-zinc-100 overflow-hidden relative">

            {/* Dynamic Background Elements */}
            <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-zinc-800/20 blur-[120px] pointer-events-none animate-pulse" style={{ animationDuration: '4s' }} />
            <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-zinc-700/10 blur-[100px] pointer-events-none animate-pulse" style={{ animationDuration: '6s', animationDelay: '2s' }} />

            {/* Left/Top Branding Panel */}
            <div className="hidden lg:flex flex-col justify-between w-[45%] p-12 relative z-10 border-r border-white/5 bg-zinc-950/50 backdrop-blur-3xl">
                <div className="flex items-center gap-3 text-white">
                    <div className="bg-gradient-to-br from-zinc-700 to-zinc-900 p-2.5 rounded-xl shadow-lg border border-white/10">
                        <ShieldAlert className="h-6 w-6 text-white" />
                    </div>
                    <span className="text-2xl font-black tracking-tight text-gradient">Road Safety AI</span>
                </div>

                <div className="space-y-6 max-w-md animate-in slide-in-from-left-8 duration-1000">
                    <h1 className="text-5xl font-black tracking-tighter leading-tight bg-clip-text text-transparent bg-gradient-to-br from-white via-zinc-200 to-zinc-600 drop-shadow-sm">
                        Intelligent Transport Infrastructure.
                    </h1>
                    <p className="text-lg font-medium text-zinc-400">
                        Authenticate to construct and scale advanced YOLOv8 spatial inference models across your sensory network.
                    </p>
                </div>

                <div className="flex items-center gap-4 text-sm font-semibold text-zinc-500 uppercase tracking-widest">
                    <span>Capstone Project</span>
                    <span className="w-1.5 h-1.5 rounded-full bg-zinc-700"></span>
                    <span>Semester VI</span>
                </div>
            </div>

            {/* Right/Auth Panel */}
            <div className="flex-1 flex items-center justify-center p-6 relative z-10">
                <div className="w-full max-w-md animate-in slide-in-from-right-8 fade-in duration-700">

                    <div className="lg:hidden flex justify-center items-center gap-3 mb-10 text-white">
                        <div className="bg-gradient-to-br from-zinc-700 to-zinc-900 p-2.5 rounded-xl shadow-lg border border-white/10">
                            <ShieldAlert className="h-6 w-6 text-white" />
                        </div>
                        <span className="text-2xl font-black tracking-tight text-gradient">Road Safety AI</span>
                    </div>

                    <Card className="glass-card border-none shadow-2xl p-8 backdrop-blur-2xl">
                        <div className="mb-8">
                            <h2 className="text-3xl font-extrabold tracking-tight text-white mb-2">
                                {isLogin ? "Welcome back" : "Create account"}
                            </h2>
                            <p className="text-zinc-400 font-medium">
                                {isLogin ? "Enter your credentials to access the nexus." : "Register an admin profile to scale your network."}
                            </p>
                        </div>

                        <form onSubmit={handleSubmit} className="space-y-5">
                            {error && (
                                <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-red-500 text-sm font-semibold text-center shadow-[0_0_10px_rgba(239,68,68,0.2)]">
                                    {error}
                                </div>
                            )}
                            {!isLogin && (
                                <div className="space-y-2 group">
                                    <div className="relative">
                                        <User className="absolute left-3.5 top-1/2 -translate-y-1/2 h-5 w-5 text-zinc-500 group-focus-within:text-white transition-colors" />
                                        <Input
                                            placeholder="Full Name"
                                            required
                                            value={fullname}
                                            onChange={(e) => setFullname(e.target.value)}
                                            className="pl-11 bg-zinc-900/50 border-white/10 text-white placeholder:text-zinc-600 h-12 rounded-xl focus-visible:ring-1 focus-visible:ring-white/30 focus-visible:border-white/30 transition-all font-medium"
                                        />
                                    </div>
                                </div>
                            )}

                            <div className="space-y-2 group">
                                <div className="relative">
                                    <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 h-5 w-5 text-zinc-500 group-focus-within:text-white transition-colors" />
                                    <Input
                                        type="email"
                                        placeholder="name@organization.com"
                                        required
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        className="pl-11 bg-zinc-900/50 border-white/10 text-white placeholder:text-zinc-600 h-12 rounded-xl focus-visible:ring-1 focus-visible:ring-white/30 focus-visible:border-white/30 transition-all font-medium"
                                    />
                                </div>
                            </div>

                            <div className="space-y-2 group">
                                <div className="relative">
                                    <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 h-5 w-5 text-zinc-500 group-focus-within:text-white transition-colors" />
                                    <Input
                                        type="password"
                                        placeholder="••••••••"
                                        required
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        className="pl-11 bg-zinc-900/50 border-white/10 text-white placeholder:text-zinc-600 h-12 rounded-xl focus-visible:ring-1 focus-visible:ring-white/30 focus-visible:border-white/30 transition-all font-medium"
                                    />
                                </div>
                            </div>

                            <Button type="submit" className="w-full h-12 rounded-xl bg-white hover:bg-zinc-200 text-zinc-950 font-bold text-base shadow-[0_0_20px_rgba(255,255,255,0.1)] transition-all transform hover:scale-[1.02]">
                                {isLogin ? "Initialize Session" : "Create Hub Profile"} <ArrowRight className="w-5 h-5 ml-2 opacity-50" />
                            </Button>
                        </form>

                        <div className="mt-8 flex items-center gap-4">
                            <div className="flex-1 h-px bg-white/10"></div>
                            <span className="text-xs font-semibold uppercase tracking-widest text-zinc-500">Or continue with</span>
                            <div className="flex-1 h-px bg-white/10"></div>
                        </div>

                        <div className="mt-6 flex gap-3">
                            <Button type="button" variant="outline" className="flex-1 h-12 bg-transparent border-white/10 hover:bg-white/5 text-white font-semibold rounded-xl transition-all">
                                <Github className="w-5 h-5 mr-2" /> GitHub
                            </Button>
                        </div>

                        <p className="mt-8 text-center text-sm font-medium text-zinc-400">
                            {isLogin ? "Don't have access?" : "Already part of the network?"}{" "}
                            <button
                                onClick={() => setIsLogin(!isLogin)}
                                className="text-white hover:text-zinc-300 font-bold underline decoration-white/30 underline-offset-4 transition-colors"
                            >
                                {isLogin ? "Request access" : "Sign in"}
                            </button>
                        </p>
                    </Card>
                </div>
            </div>
        </div>
    );
}
