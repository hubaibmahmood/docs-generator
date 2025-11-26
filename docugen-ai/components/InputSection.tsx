import React, { useState } from "react";
import { Github, ArrowRight, Loader2 } from "lucide-react";

interface InputSectionProps {
  onAnalyze: (url: string) => void;
  isAnalyzing: boolean;
}

const InputSection: React.FC<InputSectionProps> = ({
  onAnalyze,
  isAnalyzing,
}) => {
  const [url, setUrl] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (url.trim()) {
      onAnalyze(url);
    }
  };

  const handleSample = () => {
    setUrl("https://github.com/demo/mock-project");
    onAnalyze("https://github.com/demo/mock-project");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 rounded-xl mb-6 shadow-lg shadow-blue-500/20">
            <Github className="text-white w-8 h-8" />
          </div>
          <h1 className="text-4xl font-bold text-white mb-4 tracking-tight">
            DocGen AI
          </h1>
          <p className="text-slate-400 text-lg max-w-md mx-auto">
            Transform any GitHub repository into beautiful, comprehensive
            documentation in seconds using DocGen AI.
          </p>
        </div>

        <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-8 shadow-2xl">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="relative">
              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://github.com/username/repository"
                className="w-full pl-12 pr-4 py-4 bg-slate-900/50 border border-slate-700 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              />
              <Github className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 w-5 h-5" />
            </div>

            <button
              type="button"
              onClick={handleSample}
              className="text-xs text-slate-500 hover:text-blue-400 underline cursor-pointer text-right w-full block mb-2"
            >
              Or try with a sample mock project
            </button>

            <button
              type="submit"
              disabled={isAnalyzing || !url}
              className="w-full py-4 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-xl transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-blue-600/20"
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
            <div key={i} className="p-4">
              <div className="text-white font-semibold mb-1">{item.label}</div>
              <div className="text-slate-500 text-sm">{item.desc}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default InputSection;
