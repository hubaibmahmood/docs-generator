import React, { useState } from "react";
import { Github, ArrowRight, Loader2, AlertCircle } from "lucide-react";

interface InputSectionProps {
  onAnalyze: (url: string) => void;
  isAnalyzing: boolean;
  error?: string;
  hasApiKey: boolean;
}

const InputSection: React.FC<InputSectionProps> = ({
  onAnalyze,
  isAnalyzing,
  error: propError,
  hasApiKey,
}) => {
  const [url, setUrl] = useState("");
  const [localError, setLocalError] = useState<string | null>(null);

  const validateUrl = (inputUrl: string): string | null => {
    const trimmed = inputUrl.trim();
    if (!trimmed) return "URL is required";
    
    if (!hasApiKey) {
        return "API Key is missing. Please configure your Gemini API Key in Settings.";
    }
    
    // Block dangerous protocols
    const dangerousProtocols = ["javascript:", "data:", "vbscript:", "file:"];
    if (dangerousProtocols.some((p) => trimmed.toLowerCase().startsWith(p))) {
      return "Invalid protocol detected";
    }

    // Block path traversal
    if (trimmed.includes("..")) {
      return "Path traversal detected";
    }

    // Block embedded credentials (basic check)
    // Allow git@... but block user:pass@host...
    if (trimmed.includes("@")) {
      const isGitSsh =
        trimmed.startsWith("git@") || trimmed.startsWith("ssh://");
      if (!isGitSsh) {
        // If it's http/https and has @, it likely has credentials
        return "Embedded credentials are not allowed for security";
      }
    }

    // Block double slashes (except for protocol)
    // Split protocol first
    const protocolSplit = trimmed.split("://");
    const pathToCheck = protocolSplit.length > 1 ? protocolSplit[1] : trimmed;
    if (pathToCheck.includes("//")) {
      return "Invalid URL: Double slashes are not allowed";
    }

    if (trimmed.length > 2048) {
      return "URL is too long (max 2048 characters)";
    }

    // Block placeholders
    const placeholders = [
      "https://github.com/username/repository",
      "https://github.com/user/repo",
    ];
    if (placeholders.includes(trimmed.toLowerCase())) {
      return "Please replace the placeholder with a real repository URL";
    }

    // Basic URL format check
    try {
      const urlObj = new URL(trimmed);
      if (!["http:", "https:"].includes(urlObj.protocol)) {
        return "Only HTTP/HTTPS protocols are supported";
      }
    } catch (e) {
      return "Please enter a valid URL";
    }

    return null;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLocalError(null);

    const validationError = validateUrl(url);
    if (validationError) {
      setLocalError(validationError);
      return;
    }

    if (url.trim()) {
      onAnalyze(url);
    }
  };

  const handleSample = () => {
    setUrl("https://github.com/demo/mock-project");
    setLocalError(null);
    onAnalyze("https://github.com/demo/mock-project");
  };

  const displayError = localError || propError;

  return (
    <div className="w-full max-w-2xl px-4">
      <div className="text-center mb-10">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 rounded-2xl mb-6 shadow-lg shadow-blue-500/20">
          <Github className="text-white w-8 h-8" />
        </div>
        <h1 className="text-4xl font-bold text-slate-900 mb-4 tracking-tight">
          DocGen AI
        </h1>
        <p className="text-slate-500 text-lg max-w-md mx-auto">
          Transform any GitHub repository into beautiful, comprehensive
          documentation in seconds using DocGen AI.
        </p>
      </div>

      <div className="bg-white border border-slate-200 rounded-2xl p-8 shadow-xl shadow-slate-200/50">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="relative">
            <input
              type="text"
              value={url}
              onChange={(e) => {
                setUrl(e.target.value);
                setLocalError(null);
              }}
              placeholder="https://github.com/username/repository"
              className={`w-full pl-12 pr-4 py-4 bg-slate-50 border rounded-xl text-slate-900 placeholder-slate-500 focus:outline-none focus:ring-2 transition-all ${
                displayError
                  ? "border-red-300 focus:ring-red-200"
                  : "border-slate-200 focus:ring-blue-500/20 focus:border-blue-500"
              }`}
            />
            <Github className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-600 w-5 h-5" />
          </div>

          {displayError && (
            <div className="flex items-center gap-2 text-red-600 text-sm bg-red-50 p-3 rounded-lg border border-red-100 animate-in fade-in slide-in-from-top-1">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{displayError}</span>
            </div>
          )}

          <button
            type="button"
            onClick={handleSample}
            className="text-xs text-slate-700 hover:text-blue-600 underline cursor-pointer text-right w-full block mb-2 transition-colors"
          >
            Or try with a sample mock project
          </button>

          <button
            type="submit"
            disabled={isAnalyzing || !url}
            className="w-full py-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-blue-600/20 active:scale-[0.99]"
          >
            {isAnalyzing ? (
              <>
                <Loader2 className="animate-spin w-5 h-5" />
                Cloning & Analyzing...
              </>
            ) : (
              <>
                Generate Documentation
                <ArrowRight className="w-5 h-5" />
              </>
            )}
          </button>
        </form>
      </div>

      <div className="mt-12 grid grid-cols-3 gap-6 text-center">
        {[
          { label: "Smart Analysis", desc: "Parses project structure" },
          { label: "Gemini 2.5", desc: "Powered by Google AI" },
          { label: "Instant Docs", desc: "API & Code References" },
        ].map((item, i) => (
          <div key={i} className="p-2">
            <div className="text-slate-900 font-bold mb-1">{item.label}</div>
            <div className="text-slate-500 text-sm">{item.desc}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default InputSection;
