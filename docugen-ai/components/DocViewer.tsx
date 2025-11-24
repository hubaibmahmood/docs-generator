import React from 'react';
import ReactMarkdown from 'react-markdown';
import { GeneratedDoc } from '../types';
import { Copy, Check, Download } from 'lucide-react';

interface DocViewerProps {
  doc: GeneratedDoc | null;
  isLoading: boolean;
}

const DocViewer: React.FC<DocViewerProps> = ({ doc, isLoading }) => {
  const [copied, setCopied] = React.useState(false);

  const handleCopy = () => {
    if (doc) {
      navigator.clipboard.writeText(doc.markdown);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleDownload = () => {
    if (doc) {
      const blob = new Blob([doc.markdown], { type: 'text/markdown' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${doc.type}-docs.md`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }
  };

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-slate-400 animate-pulse">
        <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-4"></div>
        <p>Generating AI Documentation...</p>
        <p className="text-xs mt-2 opacity-70">Consulting Gemini Models</p>
      </div>
    );
  }

  if (!doc) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-slate-400">
        <svg className="w-16 h-16 mb-4 opacity-20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
        <p>Select a file to view documentation</p>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col bg-white">
      <div className="border-b border-slate-200 px-8 py-4 flex justify-between items-center bg-slate-50 sticky top-0 z-10">
        <h2 className="text-xl font-semibold text-slate-800 capitalize">{doc.type} Documentation</h2>
        <div className="flex gap-2">
          <button
            onClick={handleCopy}
            className="p-2 text-slate-500 hover:text-blue-600 transition-colors rounded-md hover:bg-slate-200"
            title="Copy Markdown"
          >
            {copied ? <Check size={18} /> : <Copy size={18} />}
          </button>
          <button
             onClick={handleDownload}
             className="p-2 text-slate-500 hover:text-blue-600 transition-colors rounded-md hover:bg-slate-200"
             title="Download Markdown"
          >
            <Download size={18} />
          </button>
        </div>
      </div>
      <div className="flex-1 overflow-y-auto px-8 py-8 prose prose-slate max-w-none">
        <ReactMarkdown
          components={{
            code({ node, inline, className, children, ...props }: any) {
              return inline ? (
                <code className="bg-slate-100 text-slate-800 px-1 py-0.5 rounded text-sm font-mono" {...props}>
                  {children}
                </code>
              ) : (
                // For block code, let the 'pre' component handle the wrapping
                <code className={className} {...props}>{children}</code>
              );
            },
            pre({ children }: any) {
                // This is where the block code (pre + code) gets wrapped
                // Apply the styling and copy button here
                return (
                    <div className="relative group">
                        <pre className="bg-slate-900 text-slate-50 p-4 rounded-lg overflow-x-auto my-4">
                            {children}
                        </pre>
                        <button
                            onClick={handleCopy}
                            className="absolute top-2 right-2 p-1.5 text-slate-400 hover:text-white hover:bg-slate-700 rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200"
                            title="Copy code"
                        >
                            {copied ? <Check size={16} /> : <Copy size={16} />}
                        </button>
                    </div>
                );
            }
          }}
        >
          {doc.markdown}
        </ReactMarkdown>
      </div>
    </div>
  );
};

export default DocViewer;
