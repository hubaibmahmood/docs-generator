import React, { useState } from 'react';
import InputSection from './components/InputSection';
import Sidebar from './components/Sidebar';
import DocViewer from './components/DocViewer';
import { FileNode, GeneratedDoc, AnalysisStatus, FileType } from './types';
import { apiService, transformFileTree, transformGeneratedDocs } from './services/apiService';

function App() {
  // App State
  const [step, setStep] = useState<'input' | 'workspace'>('input');
  const [status, setStatus] = useState<AnalysisStatus>({ step: 'idle', message: '', progress: 0 });
  const [files, setFiles] = useState<FileNode[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  
  // Cache for generated docs
  const [docsCache, setDocsCache] = useState<Record<string, GeneratedDoc>>({});
  const [isLoadingDoc, setIsLoadingDoc] = useState(false);

  // --- Actions ---

  const handleAnalyze = async (url: string) => {
    try {
      setStatus({ step: 'scanning', message: 'Connecting to API...', progress: 10 });
      
      const taskId = await apiService.startProcessing(url);
      
      setStatus({ step: 'analyzing', message: 'Processing Repository...', progress: 30 });

      // Poll for completion
      const pollInterval = setInterval(async () => {
        try {
          const taskStatus = await apiService.getStatus(taskId);
          
          if (taskStatus.status === 'SUCCESS') {
            clearInterval(pollInterval);
            setStatus({ step: 'complete', message: 'Processing Complete', progress: 100 });
            
            const result = await apiService.getResult(taskId);
            
            // 1. Process Source Files
            if (result.source_analysis) {
                const tree = transformFileTree(result.source_analysis.file_tree, result.source_analysis.file_analysis);
                setFiles(tree);
            }

            // 2. Process Generated Docs
            const genDocs = transformGeneratedDocs(result.results);
            const newCache = { ...docsCache };
            genDocs.forEach(doc => {
                newCache[doc.id] = doc;
            });
            setDocsCache(newCache);

            setStep('workspace');
            // Select first generated doc if available
            if (genDocs.length > 0) {
                setSelectedId(genDocs[0].id);
            }
            
          } else if (taskStatus.status === 'FAILED') {
            clearInterval(pollInterval);
            const errorMessage = taskStatus.errors && taskStatus.errors.length > 0 
              ? taskStatus.errors[0].error 
              : 'Analysis Failed';
            setStatus({ step: 'error', message: errorMessage, progress: 0 });
          } else {
            // Still pending/in_progress
             setStatus(prev => ({ ...prev, progress: prev.progress < 90 ? prev.progress + 5 : 90 }));
          }
        } catch (e) {
          clearInterval(pollInterval);
          setStatus({ step: 'error', message: 'Connection Lost', progress: 0 });
        }
      }, 2000);

    } catch (error) {
       setStatus({ step: 'error', message: 'Failed to start analysis', progress: 0 });
    }
  };

  const loadSpecialDoc = async (type: 'overview' | 'architecture' | 'getting-started') => {
    // Map internal IDs to backend section names
    const map: Record<string, string> = {
        'overview': 'Project Overview',
        'getting-started': 'Getting Started',
        'architecture': 'Architecture'
    };
    
    const targetId = map[type] || type;
    setSelectedId(targetId);
  };

  const handleFileSelect = async (file: FileNode) => {
    if (file.type === FileType.FOLDER) return;
    
    setSelectedId(file.id);

    // If it's a source file, we create a "Doc" wrapper for it to display
    if (file.content) {
        setDocsCache(prev => ({
            ...prev,
            [file.id]: {
                id: file.id,
                fileId: file.id,
                markdown: `\`\`\`${file.language || ''}\n${file.content}\n\`\`\``,
                type: 'code',
                lastUpdated: Date.now()
            }
        }));
    }
  };

  const handleDocSelect = (doc: GeneratedDoc) => {
     setSelectedId(doc.id);
  };

  const handleBackToInput = () => {
    setStep('input');
    setFiles([]);
    setDocsCache({});
    setSelectedId(null);
    setStatus({ step: 'idle', message: '', progress: 0 });
    window.location.hash = ''; // Clear the URL hash
  };

  // --- Render ---

  if (step === 'input') {
    return (
      <InputSection 
        onAnalyze={handleAnalyze} 
        isAnalyzing={status.step !== 'idle' && status.step !== 'error'}
        error={status.step === 'error' ? status.message : undefined}
      />
    );
  }

  const currentDoc = selectedId ? docsCache[selectedId] : null;
  
  // Get all generated docs for Sidebar
  // Filter to only show ACTUAL generated docs, not source files viewed as code
  const generatedDocs = Object.values(docsCache).filter(d => d.type === 'generated');

  return (
    <div className="flex h-screen overflow-hidden bg-slate-50">
      <Sidebar 
        files={files} 
        generatedDocs={generatedDocs}
        onSelectFile={handleFileSelect} 
        onSelectSpecial={loadSpecialDoc}
        onSelectDoc={handleDocSelect}
        onBack={handleBackToInput}
        selectedId={selectedId}
      />
      
      <main className="flex-1 flex flex-col h-screen overflow-hidden relative">
        <DocViewer 
          doc={currentDoc || null} 
          isLoading={isLoadingDoc} 
        />
      </main>
    </div>
  );
}

export default App;
