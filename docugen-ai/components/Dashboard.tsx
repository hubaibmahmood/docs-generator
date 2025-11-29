import React from "react";
import { Plus, Settings, FileText, ExternalLink, Key } from "lucide-react";

interface DashboardProps {
  userName: string;
  onNavigate: (path: "input" | "settings") => void;
  onLogout: () => void;
}

const Dashboard: React.FC<DashboardProps> = ({
  userName,
  onNavigate,
  onLogout,
}) => {
  return (
    <div className="min-h-[calc(100vh-64px)] bg-slate-50 font-sans">
      {/* Main Content */}
      <div className="max-w-6xl mx-auto px-6 py-12">
        <header className="mb-12">
          <h1 className="text-3xl font-bold text-slate-900 mb-2">
            Workspace Dashboard
          </h1>
          <p className="text-slate-500">
            Manage your documentation projects and API configurations.
          </p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Action Card: Generate New Docs */}
          <div
            onClick={() => onNavigate("input")}
            className="group bg-white rounded-2xl p-8 border border-slate-200 shadow-sm hover:shadow-xl hover:border-blue-500/30 transition-all cursor-pointer relative overflow-hidden"
          >
            <div className="absolute top-0 right-0 p-6 opacity-10 group-hover:opacity-20 transition-opacity">
              <FileText
                size={120}
                className="text-blue-600 transform rotate-12"
              />
            </div>

            <div className="relative z-10">
              <div className="w-14 h-14 bg-blue-50 rounded-xl flex items-center justify-center mb-6 group-hover:bg-blue-600 transition-colors">
                <Plus className="w-8 h-8 text-blue-600 group-hover:text-white transition-colors" />
              </div>

              <h3 className="text-xl font-bold text-slate-900 mb-2">
                New Documentation
              </h3>
              <p className="text-slate-500 mb-6 max-w-sm">
                Analyze a GitHub repository and generate comprehensive
                documentation, architecture diagrams, and API references using
                Gemini AI.
              </p>

              <div className="flex items-center text-blue-600 font-semibold group-hover:translate-x-1 transition-transform">
                Start Analysis <ExternalLink className="w-4 h-4 ml-2" />
              </div>
            </div>
          </div>

          {/* Action Card: Settings / API Key */}
          <div
            onClick={() => onNavigate("settings")}
            className="group bg-white rounded-2xl p-8 border border-slate-200 shadow-sm hover:shadow-xl hover:border-indigo-500/30 transition-all cursor-pointer relative overflow-hidden"
          >
            <div className="absolute top-0 right-0 p-6 opacity-10 group-hover:opacity-20 transition-opacity">
              <Key
                size={120}
                className="text-indigo-600 transform -rotate-12"
              />
            </div>

            <div className="relative z-10">
              <div className="w-14 h-14 bg-indigo-50 rounded-xl flex items-center justify-center mb-6 group-hover:bg-indigo-600 transition-colors">
                <Settings className="w-8 h-8 text-indigo-600 group-hover:text-white transition-colors" />
              </div>

              <h3 className="text-xl font-bold text-slate-900 mb-2">
                Settings & API Keys
              </h3>
              <p className="text-slate-500 mb-6 max-w-sm">
                Configure your OpenAI or Gemini API keys, manage repository
                access tokens, and customize documentation output templates.
              </p>

              <div className="flex items-center text-indigo-600 font-semibold group-hover:translate-x-1 transition-transform">
                Manage Configuration <ExternalLink className="w-4 h-4 ml-2" />
              </div>
            </div>
          </div>
        </div>

        {/* Recent Activity Section */}
        <div className="mt-12">
          <h2 className="text-lg font-bold text-slate-900 mb-4">
            Recent Projects
          </h2>
          <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
            {[1, 2, 3].map((item) => (
              <div
                key={item}
                className="p-4 border-b border-slate-100 last:border-0 hover:bg-slate-50 transition-colors flex items-center justify-between group cursor-pointer"
              >
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-slate-100 rounded-lg flex items-center justify-center">
                    <FileText className="w-5 h-5 text-slate-500" />
                  </div>
                  <div>
                    <h4 className="font-medium text-slate-900 group-hover:text-blue-600 transition-colors">
                      demo-project-v{item}
                    </h4>
                    <p className="text-xs text-slate-500">
                      Updated 2 days ago • TypeScript
                    </p>
                  </div>
                </div>
                <div className="text-sm text-slate-400">View Docs &rarr;</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
