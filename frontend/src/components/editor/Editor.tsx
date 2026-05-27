'use client';

import React from 'react';
import MonacoEditor from '@monaco-editor/react';
import { useWorkbenchStore } from '@/store/workbench';

export const Editor = () => {
  const { activeFile, files } = useWorkbenchStore();
  
  // Find the content of the active file
  const findFileContent = (nodes: any[], path: string): string | undefined => {
    for (const node of nodes) {
      if (node.path === path) return node.content;
      if (node.children) {
        const content = findFileContent(node.children, path);
        if (content !== undefined) return content;
      }
    }
    return undefined;
  };

  const content = activeFile ? findFileContent(files, activeFile) : '// Select a file to edit';
  const language = activeFile?.endsWith('.py') ? 'python' : 
                   activeFile?.endsWith('.js') || activeFile?.endsWith('.ts') ? 'javascript' : 
                   activeFile?.endsWith('.tsx') ? 'typescript' : 'plaintext';

  return (
    <div className="flex-1 h-full bg-[#1e1e1e] overflow-hidden">
      <MonacoEditor
        height="100%"
        language={language}
        theme="vs-dark"
        value={content}
        options={{
          fontSize: 14,
          minimap: { enabled: true },
          scrollBeyondLastLine: false,
          automaticLayout: true,
          padding: { top: 16 },
        }}
      />
    </div>
  );
};
