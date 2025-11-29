import React, { useState, useEffect } from "react";
import { Save, Key, CheckCircle, Eye, EyeOff } from "lucide-react";

interface SettingsScreenProps {
  apiKey: string;
  onSave: (key: string) => void;
}

const SettingsScreen: React.FC<SettingsScreenProps> = ({ apiKey: initialKey, onSave }) => {
  const [localKey, setLocalKey] = useState(initialKey);
  const [isEditing, setIsEditing] = useState(false);
  const [saved, setSaved] = useState(false);
  const [showApiKey, setShowApiKey] = useState(false);
  const [persistKey, setPersistKey] = useState(!!localStorage.getItem("docugen_gemini_api_key"));

  useEffect(() => {
      setLocalKey(initialKey);
  }, [initialKey]);

  const handleSave = () => {
    onSave(localKey);
    
    if (persistKey) {
        localStorage.setItem("docugen_gemini_api_key", localKey);
    } else {
        localStorage.removeItem("docugen_gemini_api_key");
    }

    setSaved(true);
    setIsEditing(false);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="font-sans w-full">
      <div className="max-w-4xl mx-auto px-6 py-12">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">
          Settings & Configuration
        </h1>
        <p className="text-slate-500 mb-8">
          Manage your API keys and application preferences.
        </p>

        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <div className="p-6 border-b border-slate-100 bg-slate-50/50">
            <h2 className="text-lg font-semibold text-slate-800 flex items-center gap-2">
              <Key className="w-5 h-5 text-blue-600" />
              API Configuration
            </h2>
          </div>

          <div className="p-8 space-y-8">
            {/* Gemini API Key */}
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">
                Google Gemini API Key
              </label>
              <p className="text-sm text-slate-500 mb-4">
                Required for generating documentation and analysis.
              </p>
              
              {!persistKey && localKey && (
                 <div className="mb-4 p-3 bg-amber-50 text-amber-700 text-sm rounded-lg border border-amber-200 flex items-start gap-2">
                    <span className="font-bold text-amber-600">Security Note:</span>
                    Key is currently stored in memory only and will be lost on refresh.
                 </div>
              )}

              <div className="flex gap-4 mb-4">
                <div className="relative flex-1">
                  <input
                    type={isEditing ? (showApiKey ? "text" : "password") : "password"}
                    value={localKey}
                    onChange={(e) => setLocalKey(e.target.value)}
                    disabled={!isEditing}
                    className="w-full bg-slate-50 border border-slate-300 text-slate-900 text-sm rounded-xl focus:ring-blue-500 focus:border-blue-500 block p-3.5 disabled:opacity-75 disabled:bg-slate-100 transition-colors pr-10"
                    placeholder={isEditing ? "Enter your Gemini API Key" : "**********************"}
                  />
                  
                  {isEditing && (
                    <button
                      type="button"
                      onClick={() => setShowApiKey(!showApiKey)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-700 transition-colors"
                    >
                      {showApiKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  )}

                  {saved && (
                    <div className="absolute right-3 top-1/2 -translate-y-1/2 text-green-600 flex items-center text-sm font-medium animate-in fade-in">
                      <CheckCircle className="w-4 h-4 mr-1" /> Saved
                    </div>
                  )}
                </div>
                {isEditing ? (
                  <button
                    onClick={handleSave}
                    className="bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-xl px-6 py-2.5 transition-colors flex items-center gap-2"
                  >
                    <Save className="w-4 h-4" /> Save
                  </button>
                ) : (
                  <button
                    onClick={() => {
                      setIsEditing(true);
                      setShowApiKey(false);
                    }}
                    className="bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 font-medium rounded-xl px-6 py-2.5 transition-colors"
                  >
                    Edit Key
                  </button>
                )}
              </div>

              {isEditing && (
                  <div className="flex items-center gap-2">
                      <input 
                        type="checkbox" 
                        id="persistKey" 
                        checked={persistKey} 
                        onChange={(e) => setPersistKey(e.target.checked)}
                        className="w-4 h-4 text-blue-600 bg-slate-100 border-slate-300 rounded focus:ring-blue-500"
                      />
                      <label htmlFor="persistKey" className="text-sm text-slate-600 select-none cursor-pointer">
                          Remember this key in this browser (Warning: Uses localStorage, accessible to scripts)
                      </label>
                  </div>
              )}
            </div>

            <div className="h-px bg-slate-100"></div>

            {/* GitHub Token */}
            <div className="opacity-75">
              <div className="flex items-center justify-between mb-2">
                <label className="block text-sm font-semibold text-slate-700">
                  GitHub Access Token (Optional)
                </label>
                <span className="text-xs font-medium bg-slate-100 text-slate-500 px-2 py-1 rounded">
                  Coming Soon
                </span>
              </div>
              <p className="text-sm text-slate-500 mb-4">
                Required for accessing private repositories.
              </p>
              <input
                type="text"
                disabled
                placeholder="ghp_xxxxxxxxxxxx"
                className="w-full bg-slate-50 border border-slate-200 text-slate-400 text-sm rounded-xl block p-3.5 cursor-not-allowed"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsScreen;
