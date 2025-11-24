export enum FileType {
  FILE = 'FILE',
  FOLDER = 'FOLDER'
}

export interface FileNode {
  id: string;
  name: string;
  type: FileType;
  path: string;
  content?: string; // In a real app, this might be fetched on demand
  children?: FileNode[];
  language?: string;
}

export interface GeneratedDoc {
  id: string;
  fileId: string;
  markdown: string;
  type: 'overview' | 'api' | 'code' | 'architecture' | 'generated';
  lastUpdated: number;
}

export interface AnalysisStatus {
  step: 'idle' | 'scanning' | 'analyzing' | 'complete' | 'error';
  message: string;
  progress: number;
}

export interface RepoContext {
  url: string;
  name: string;
  files: FileNode[];
}
