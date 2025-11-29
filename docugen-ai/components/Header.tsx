import React from "react";
import { Shield, ArrowLeft } from "lucide-react";

interface HeaderProps {
  userName: string;
  onLogout: () => void;
  onBack?: () => void;
}

const Header: React.FC<HeaderProps> = ({ userName, onLogout, onBack }) => {
  return (
    <nav className="bg-white border-b border-slate-200 px-6 py-4 flex justify-between items-center sticky top-0 z-50 h-16 shrink-0 shadow-sm">
      <div className="flex items-center gap-4">
        {onBack && (
          <button
            onClick={onBack}
            className="p-2 -ml-2 rounded-lg hover:bg-slate-100 text-slate-500 hover:text-slate-800 transition-colors group"
            title="Back to Dashboard"
          >
            <ArrowLeft className="w-5 h-5 group-hover:-translate-x-0.5 transition-transform" />
          </button>
        )}
        <div
          className={`flex items-center gap-2 ${onBack ? "cursor-pointer hover:opacity-80 transition-opacity" : ""}`}
          onClick={onBack}
        >
          <div className="bg-blue-600 rounded-lg p-1.5 shadow-sm shadow-blue-500/30">
            <Shield className="w-5 h-5 text-white" />
          </div>
          <span className="font-bold text-slate-800 text-lg tracking-tight">
            DocGen AI
          </span>
        </div>
      </div>
      <div className="flex items-center gap-4">
        <span className="text-sm text-slate-500 hidden sm:inline">
          Signed in as{" "}
          <span className="font-semibold text-slate-700">{userName}</span>
        </span>
        <div className="h-8 w-[1px] bg-slate-200 mx-2 hidden sm:block"></div>
        <button
          onClick={onLogout}
          className="text-sm font-medium text-slate-500 hover:text-slate-800 transition-colors"
        >
          Sign Out
        </button>
        <div className="w-8 h-8 bg-gradient-to-tr from-blue-500 to-indigo-500 rounded-full flex items-center justify-center text-white font-bold text-sm shadow-md cursor-pointer hover:shadow-lg transition-shadow border border-white">
          {userName.charAt(0).toUpperCase()}
        </div>
      </div>
    </nav>
  );
};

export default Header;
