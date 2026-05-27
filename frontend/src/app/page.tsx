'use client';

import React, { useEffect } from 'react';
import { 
  MessageSquare, 
  FolderTree, 
  Play, 
  Settings
} from 'lucide-react';
import { FileExplorer } from '@/components/explorer/FileExplorer';
import { Editor } from '@/components/editor/Editor';
import { ChatInterface } from '@/components/chat/ChatInterface';
import { useWorkbenchStore } from '@/store/workbench';
import dynamic from 'next/dynamic';

const Terminal = dynamic(() => import('@/components/terminal/Terminal').then(mod => mod.Terminal), {
  ssr: false,
});

export default function Workbench() {
  const { setFiles } = useWorkbenchStore();

  // Initialize with some dummy files for now
  useEffect(() => {
    setFiles([
      {
        name: 'src',
        type: 'directory',
        path: 'src',
        children: [
          {
            name: 'main.py',
            type: 'file',
            path: 'src/main.py',
            content: 'def hello():\n    print("Hello from MasterBlack AI!")\n\nif __name__ == "__main__":\n    hello()'
          },
          {
            name: 'utils.py',
            type: 'file',
            path: 'src/utils.py',
            content: 'def add(a, b):\n    return a + b'
          }
        ]
      },
      {
        name: 'requirements.txt',
        type: 'file',
        path: 'requirements.txt',
        content: 'fastapi\nuvicorn'
      }
    ]);
  }, [setFiles]);

  return (
    <main className="flex h-screen w-screen bg-[#1e1e1e] text-gray-200 overflow-hidden font-sans">
      {/* Sidebar Navigation (Slim) */}
      <div className="w-12 bg-[#333333] flex flex-col items-center py-4 space-y-4 border-r border-[#1e1e1e]">
        <div className="p-2 text-blue-500 hover:text-white cursor-pointer transition-colors">
          <FolderTree size={24} />
        </div>
        <div className="p-2 text-gray-400 hover:text-white cursor-pointer transition-colors">
          <MessageSquare size={24} />
        </div>
        <div className="p-2 text-gray-400 hover:text-white cursor-pointer transition-colors">
          <Play size={24} />
        </div>
        <div className="mt-auto p-2 text-gray-400 hover:text-white cursor-pointer transition-colors">
          <Settings size={24} />
        </div>
      </div>

      {/* Main Workspace */}
      <div className="flex-1 flex flex-col h-full overflow-hidden">
        <div className="flex-1 flex h-full overflow-hidden">
          <FileExplorer />
          <div className="flex-1 flex flex-col h-full overflow-hidden">
            <Editor />
            <Terminal />
          </div>
        </div>
      </div>

      {/* Chat Interface */}
      <ChatInterface />
    </main>
  );
}
