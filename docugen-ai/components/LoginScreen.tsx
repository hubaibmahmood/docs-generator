import React, { useState } from "react";
import {
  Mail,
  Lock,
  ArrowRight,
  Loader2,
  Github,
  ShieldCheck,
  User,
  Eye,
  EyeOff,
} from "lucide-react";
import { apiService } from "../services/apiService";

interface LoginScreenProps {
  onLoginSuccess: () => void;
}

const LoginScreen: React.FC<LoginScreenProps> = ({ onLoginSuccess }) => {
  const [isRegistering, setIsRegistering] = useState(false);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    // Validation Logic
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        setIsLoading(false);
        setError("Please enter a valid email address.");
        return;
    }

    if (password.length < 4) {
        setIsLoading(false);
        setError("Password must be at least 4 characters.");
        return;
    }

    if (isRegistering) {
        if (name.length < 2) {
            setIsLoading(false);
            setError("Please enter your name.");
            return;
        }
        if (password !== confirmPassword) {
            setIsLoading(false);
            setError("Passwords do not match.");
            return;
        }
        
        try {
             // Register
             await apiService.register(name, email, password);
             // Then Auto-Login
             await apiService.login(email, password);
             setIsLoading(false);
             onLoginSuccess();
        } catch (err: any) {
            setIsLoading(false);
            setError(err.message || "Registration failed.");
        }
        return;
    }

    try {
        // Backend expects 'username', we use email for now
        await apiService.login(email, password); 
        setIsLoading(false);
        onLoginSuccess();
    } catch (err: any) {
        setIsLoading(false);
        setError(err.message || "Authentication failed.");
    }
  };

  const handleSocialLogin = () => {
    setIsLoading(true);
    // Simulate social login delay
    setTimeout(() => {
      setIsLoading(false);
      onLoginSuccess();
    }, 1500);
  };

  const toggleMode = () => {
    setIsRegistering(!isRegistering);
    setError("");
    setPassword("");
    setConfirmPassword("");
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4 relative overflow-hidden font-sans">
      {/* Abstract Background Shapes */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-96 h-96 bg-blue-600/20 rounded-full blur-[100px]"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-96 h-96 bg-indigo-600/10 rounded-full blur-[100px]"></div>
      </div>

      <div className="w-full max-w-md bg-slate-800/40 backdrop-blur-xl border border-slate-700/50 rounded-2xl shadow-2xl relative z-10 overflow-hidden transition-all duration-500 ease-in-out">
        {/* Header Section */}
        <div className="p-8 pb-0 text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-tr from-blue-600 to-indigo-600 rounded-xl mb-6 shadow-lg shadow-blue-500/30 transform rotate-3">
            <ShieldCheck className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-white mb-2 tracking-tight transition-all">
            {isRegistering ? "Create Account" : "Welcome Back"}
          </h1>
          <p className="text-slate-400">
            {isRegistering
              ? "Join DocuGen to start documenting"
              : "Sign in to access your DocuGen workspace"}
          </p>
        </div>

        {/* Form Section */}
        <div className="p-8">
          <form onSubmit={handleAuth} className="space-y-5">
            {/* Name Field - Only for Registration */}
            {isRegistering && (
              <div className="space-y-1.5 animate-in fade-in slide-in-from-top-2 duration-300">
                <label className="text-xs font-bold text-slate-300 uppercase tracking-wider ml-1">
                  Full Name
                </label>
                <div className="relative group">
                  <User className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-blue-400 transition-colors w-5 h-5" />
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="w-full bg-slate-900/50 border border-slate-700/80 rounded-xl py-3.5 pl-12 pr-4 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-all"
                    placeholder="John Doe"
                  />
                </div>
              </div>
            )}

            <div className="space-y-1.5">
              <label className="text-xs font-bold text-slate-300 uppercase tracking-wider ml-1">
                Email Address / Username
              </label>
              <div className="relative group">
                <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-blue-400 transition-colors w-5 h-5" />
                <input
                  type="text"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-slate-900/50 border border-slate-700/80 rounded-xl py-3.5 pl-12 pr-4 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-all"
                  placeholder="admin"
                />
              </div>
            </div>

            <div className="space-y-1.5">
              <div className="flex justify-between items-center ml-1">
                <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                  Password
                </label>
                {!isRegistering && (
                  <button
                    type="button"
                    className="text-xs text-blue-400 hover:text-blue-300 transition-colors"
                  >
                    Forgot Password?
                  </button>
                )}
              </div>
              <div className="relative group">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-blue-400 transition-colors w-5 h-5" />
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-slate-900/50 border border-slate-700/80 rounded-xl py-3.5 pl-12 pr-12 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-all"
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300 transition-colors"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            {/* Confirm Password - Only for Registration */}
            {isRegistering && (
              <div className="space-y-1.5 animate-in fade-in slide-in-from-top-2 duration-300">
                <label className="text-xs font-bold text-slate-300 uppercase tracking-wider ml-1">
                  Confirm Password
                </label>
                <div className="relative group">
                  <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-blue-400 transition-colors w-5 h-5" />
                  <input
                    type={showConfirmPassword ? "text" : "password"}
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    className="w-full bg-slate-900/50 border border-slate-700/80 rounded-xl py-3.5 pl-12 pr-12 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-all"
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300 transition-colors"
                  >
                    {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>
            )}

            {error && (
              <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-red-400 text-sm flex items-center gap-2 animate-in fade-in slide-in-from-top-1">
                <span className="w-1.5 h-1.5 rounded-full bg-red-500"></span>
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3.5 rounded-xl transition-all shadow-lg shadow-blue-600/20 hover:shadow-blue-600/30 active:scale-[0.98] flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed mt-2"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  {isRegistering ? "Creating Account..." : "Authenticating..."}
                </>
              ) : (
                <>
                  {isRegistering ? "Create Account" : "Sign In to Workspace"}
                  <ArrowRight className="w-5 h-5" />
                </>
              )}
            </button>
          </form>

          <div className="my-6 flex items-center gap-4">
            <div className="h-px bg-slate-700 flex-1"></div>
            <span className="text-slate-500 text-xs font-medium">
              OR CONTINUE WITH
            </span>
            <div className="h-px bg-slate-700 flex-1"></div>
          </div>

          <button
            type="button"
            onClick={handleSocialLogin}
            disabled={isLoading}
            className="w-full bg-white text-slate-900 font-bold py-3 rounded-xl flex items-center justify-center gap-3 hover:bg-slate-50 transition-colors disabled:opacity-50"
          >
            <Github className="w-5 h-5" />
            GitHub
          </button>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-700/50 bg-slate-900/30 text-center">
          <p className="text-slate-500 text-sm">
            {isRegistering
              ? "Already have an account?"
              : "Don't have an account?"}{" "}
            <button
              type="button"
              onClick={toggleMode}
              className="text-blue-400 hover:text-blue-300 font-semibold transition-colors"
            >
              {isRegistering ? "Sign in" : "Create one"}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginScreen;
