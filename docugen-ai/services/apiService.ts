import { FileNode, FileType, GeneratedDoc } from "../types";

const API_BASE = "http://localhost:8087";

export interface BackendProcessingResult {
  total_sections: number;
  processed: number;
  skipped: number;
  failed: number;
  results: {
    section_name: string;
    output_path: string;
    status: string;
    error?: string;
    markdown_content?: string;
  }[];
  source_analysis?: {
    file_tree: any;
    file_analysis: Record<string, any>;
  };
}

export const apiService = {
  startProcessing: async (repoUrl: string): Promise<string> => {
    const response = await fetch(`${API_BASE}/process`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: repoUrl }),
    });
    if (!response.ok) throw new Error("Failed to start analysis");
    const data = await response.json();
    return data.task_id;
  },

  getStatus: async (
    taskId: string,
  ): Promise<{ status: string; message?: string; errors?: { error: string }[] }> => {
    const response = await fetch(`${API_BASE}/status/${taskId}`);
    if (!response.ok) throw new Error("Failed to check status");
    return await response.json();
  },

  getResult: async (taskId: string): Promise<BackendProcessingResult> => {
    const response = await fetch(`${API_BASE}/result/${taskId}`);
    if (!response.ok) throw new Error("Failed to get results");
    return await response.json();
  },
};

export const transformFileTree = (
  backendTree: any,
  fileAnalysis: Record<string, any>,
): FileNode[] => {
  if (!backendTree || !backendTree.children) return [];

  const mapNode = (node: any): FileNode => {
    const isFolder = node.type === "dir";
    const analysis = fileAnalysis[node.path] || {};

    return {
      id: node.path,
      name: node.name,
      type: isFolder ? FileType.FOLDER : FileType.FILE,
      path: node.path,
      content: analysis.content || undefined, // Use content if available
      children: node.children ? node.children.map(mapNode) : undefined,
      language: analysis.language,
    };
  };

  return backendTree.children.map(mapNode);
};

export const transformGeneratedDocs = (results: any[]): GeneratedDoc[] => {
  return results
    .filter((r) => r.status === "success" && r.markdown_content)
    .map((r) => ({
      id: r.section_name,
      fileId: r.section_name,
      markdown: r.markdown_content!,
      type: "generated",
      lastUpdated: Date.now(),
    }));
};
