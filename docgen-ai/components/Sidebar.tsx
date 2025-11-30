import React, { useState } from "react";
import JSZip from "jszip";
import { saveAs } from "file-saver";
import { FileNode, FileType, GeneratedDoc } from "../types";
import {
  Folder,
  FileCode,
  ChevronRight,
  ChevronDown,
  LayoutDashboard,
  Network,
  Search,
  FileText,
  Play,
  Code,
  Database,
  Download,
} from "lucide-react";

interface SidebarProps {
  files: FileNode[];
  generatedDocs: GeneratedDoc[];
  onSelectFile: (file: FileNode) => void;
  onSelectSpecial: (
    type: "overview" | "architecture" | "getting-started",
  ) => void;
  onSelectDoc: (doc: GeneratedDoc) => void;
  onBack: () => void;
  selectedId: string | null;
}

// Helper to get icon based on doc.id
const getDocIcon = (docId: string, size: number) => {
  switch (docId) {
    case "Project Overview":
      return <LayoutDashboard size={size} />;
    case "Getting Started":
      return <Play size={size} />;
    case "Architecture":
      return <Network size={size} />;
    case "API Reference":
      return <Code size={size} />;
    case "Data Models":
      return <Database size={size} />;
    default:
      return <FileText size={size} />;
  }
};

const FileTreeItem: React.FC<{
  node: FileNode;
  depth: number;
  onSelect: (node: FileNode) => void;
  selectedId: string | null;
}> = ({ node, depth, onSelect, selectedId }) => {
  const [isOpen, setIsOpen] = useState(true);
  const isSelected = selectedId === node.id;

  if (node.type === FileType.FOLDER) {
    return (
      <div>
        <div
          className="flex items-center gap-2 px-3 py-1.5 hover:bg-slate-800 text-slate-400 cursor-pointer text-sm transition-colors select-none"
          style={{ paddingLeft: `${depth * 12 + 12}px` }}
          onClick={() => setIsOpen(!isOpen)}
        >
          {isOpen ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
          <Folder size={14} className="text-blue-400" />
          <span className="truncate">{node.name}</span>
        </div>
        {isOpen && node.children && (
          <div>
            {node.children.map((child) => (
              <FileTreeItem
                key={child.id}
                node={child}
                depth={depth + 1}
                onSelect={onSelect}
                selectedId={selectedId}
              />
            ))}
          </div>
        )}
      </div>
    );
  }

  return (
    <div
      className={`
        flex items-center gap-2 px-3 py-1.5 cursor-pointer text-sm transition-colors
        ${isSelected ? "bg-blue-600 text-white" : "hover:bg-slate-800 text-slate-300"}
      `}
      style={{ paddingLeft: `${depth * 12 + 28}px` }}
      onClick={() => onSelect(node)}
    >
      <FileCode
        size={14}
        className={isSelected ? "text-blue-200" : "text-slate-500"}
      />
      <span className="truncate">{node.name}</span>
    </div>
  );
};

const Sidebar: React.FC<SidebarProps> = ({
  files,
  generatedDocs,
  onSelectFile,
  onSelectSpecial,
  onSelectDoc,
  onBack,
  selectedId,
}) => {
  const [search, setSearch] = useState("");

  const handleDownloadAll = async () => {
    const zip = new JSZip();

    if (generatedDocs.length === 0) {
      alert("No documentation generated yet.");
      return;
    }

    generatedDocs.forEach((doc) => {
      let filename = doc.id;
      if (!filename.endsWith(".md")) {
        filename += ".md";
      }
      zip.file(filename, doc.markdown);
    });

    try {
      const content = await zip.generateAsync({ type: "blob" });
      saveAs(content, "documentation.zip");
    } catch (error) {
      console.error("Failed to zip files", error);
      alert("Failed to create zip file.");
    }
  };

  const filterFiles = (nodes: FileNode[]): FileNode[] => {
    if (!search) return nodes;
    return nodes.reduce<FileNode[]>((acc, node) => {
      if (
        node.type === FileType.FILE &&
        node.name.toLowerCase().includes(search.toLowerCase())
      ) {
        acc.push(node);
      } else if (node.type === FileType.FOLDER && node.children) {
        const filteredChildren = filterFiles(node.children);
        if (filteredChildren.length > 0) {
          acc.push({ ...node, children: filteredChildren });
        }
      }
      return acc;
    }, []);
  };

  const displayedFiles = filterFiles(files);

  const getDocItem = (
    docId: string,
    label: string,
    handler: () => void,
    icon: React.ReactNode,
  ) => {
    const isSelected =
      selectedId === docId ||
      (docId === "Project Overview" && selectedId === "overview") ||
      (docId === "Architecture" && selectedId === "architecture") ||
      (docId === "Getting Started" && selectedId === "getting-started");
    return (
      <div
        key={docId}
        onClick={handler}
        className={`flex items-center gap-2 px-4 py-2 text-sm cursor-pointer ${
          isSelected
            ? "bg-blue-600 text-white"
            : "text-slate-300 hover:bg-slate-800"
        }`}
      >
        {icon}
        <span>{label}</span>
      </div>
    );
  };

  // Pre-defined order and handlers for fixed items
  const fixedDocItems = [
    {
      id: "Project Overview",
      label: "Project Overview",
      handler: () => onSelectSpecial("overview"),
      icon: getDocIcon("Project Overview", 16),
    },
    {
      id: "Getting Started",
      label: "Getting Started",
      handler: () => onSelectSpecial("getting-started"),
      icon: getDocIcon("Getting Started", 16),
    },
    {
      id: "Architecture",
      label: "Architecture",
      handler: () => onSelectSpecial("architecture"),
      icon: getDocIcon("Architecture", 16),
    },
  ];

  // Filter out any generatedDocs that match the fixedDocItems by ID
  const remainingGeneratedDocs = generatedDocs.filter(
    (doc) => !fixedDocItems.some((fixedItem) => fixedItem.id === doc.id),
  );

  return (
    <div className="w-72 bg-slate-900 h-screen flex flex-col border-r border-slate-800 flex-shrink-0">
      <div className="p-4 border-b border-slate-800">
        <div className="flex items-center gap-2 font-bold text-white mb-4">
          <span className="bg-blue-600 rounded p-1">
            <LayoutDashboard size={16} />
          </span>
          <span>DocGen</span>
        </div>
        <div className="relative">
          <input
            type="text"
            placeholder="Search files..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full bg-slate-800 border-none rounded-md py-1.5 pl-8 pr-2 text-sm text-slate-200 placeholder-slate-500 focus:ring-1 focus:ring-blue-500"
          />
          <Search
            size={14}
            className="absolute left-2.5 top-2 text-slate-500"
          />
        </div>
      </div>

      <div className="flex-1 overflow-y-auto py-2">
        <div className="mb-4">
          <div className="px-3 py-1 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
            General
          </div>

          {fixedDocItems.map((item) =>
            getDocItem(item.id, item.label, item.handler, item.icon),
          )}

          {remainingGeneratedDocs.map((doc) => (
            <div
              key={doc.id}
              onClick={() => onSelectDoc(doc)}
              className={`flex items-center gap-2 px-4 py-2 text-sm cursor-pointer ${
                selectedId === doc.id
                  ? "bg-blue-600 text-white"
                  : "text-slate-300 hover:bg-slate-800"
              }`}
            >
              {getDocIcon(doc.id, 16)}
              <span className="truncate">{doc.id}</span>
            </div>
          ))}
        </div>

        <div>
          <div className="px-3 py-1 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
            Explorer
          </div>
          {displayedFiles.map((node) => (
            <FileTreeItem
              key={node.id}
              node={node}
              depth={0}
              onSelect={onSelectFile}
              selectedId={selectedId}
            />
          ))}
        </div>
      </div>

      <div className="p-4 border-t border-slate-800 flex flex-col gap-2">
        <button
          onClick={handleDownloadAll}
          className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-sm transition-colors flex items-center justify-center gap-2 shadow-lg shadow-blue-900/20"
        >
          <Download size={16} />
          <span>Download Generated Documentation</span>
        </button>

        <button
          onClick={onBack}
          className="w-full py-2 px-4 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-sm transition-colors flex items-center justify-center gap-2"
        >
          <span>← New Analysis</span>
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
