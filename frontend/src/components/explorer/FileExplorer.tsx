'use client';

import React from 'react';
import { FolderTree, FileCode, ChevronDown, ChevronRight, Folder } from 'lucide-react';
import { useWorkbenchStore } from '@/store/workbench';
import { cn } from '@/lib/utils';

interface FileItemProps {
  node: any;
  depth: number;
}

const FileItem = ({ node, depth }: FileItemProps) => {
  const [isOpen, setIsOpen] = React.useState(true);
  const { activeFile, setActiveFile } = useWorkbenchStore();

  const isDirectory = node.type === 'directory';
  const isSelected = activeFile === node.path;

  const handleClick = () => {
    if (isDirectory) {
      setIsOpen(!isOpen);
    } else {
      setActiveFile(node.path);
    }
  };

  return (
    <div>
      <div 
        className={cn(
          "flex items-center gap-1.5 py-1 px-2 cursor-pointer text-sm transition-colors",
          isSelected ? "bg-[#37373d] text-white" : "text-gray-400 hover:bg-[#2a2d2e] hover:text-gray-200"
        )}
        style={{ paddingLeft: `${depth * 12 + 8}px` }}
        onClick={handleClick}
      >
        {isDirectory ? (
          <>
            {isOpen ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
            <Folder size={14} className="text-blue-400 fill-current opacity-70" />
          </>
        ) : (
          <>
            <div className="w-[14px]" />
            <FileCode size={14} className="text-blue-400" />
          </>
        )}
        <span className="truncate">{node.name}</span>
      </div>
      
      {isDirectory && isOpen && node.children && (
        <div>
          {node.children.map((child: any) => (
            <FileItem key={child.path} node={child} depth={depth + 1} />
          ))}
        </div>
      )}
    </div>
  );
};

export const FileExplorer = () => {
  const { files } = useWorkbenchStore();

  return (
    <div className="flex flex-col h-full bg-[#1e1e1e] border-r border-[#333] w-64 overflow-y-auto select-none">
      <div className="p-4 text-xs font-semibold text-gray-400 uppercase tracking-wider flex items-center gap-2">
        <FolderTree size={14} /> Explorer
      </div>
      <div className="flex-1 py-2">
        {files.length === 0 ? (
          <div className="px-4 text-sm text-gray-500 italic">No files loaded</div>
        ) : (
          files.map((file) => (
            <FileItem key={file.path} node={file} depth={0} />
          ))
        )}
      </div>
    </div>
  );
};
