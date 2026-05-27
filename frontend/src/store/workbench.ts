import { create } from 'zustand';

interface FileNode {
  name: string;
  type: 'file' | 'directory';
  path: string;
  children?: FileNode[];
  content?: string;
}

interface WorkbenchState {
  activeFile: string | null;
  files: FileNode[];
  terminalOutput: string;
  isThinking: boolean;
  setActiveFile: (path: string | null) => void;
  setFiles: (files: FileNode[]) => void;
  appendTerminalOutput: (output: string) => void;
  setIsThinking: (isThinking: boolean) => void;
}

export const useWorkbenchStore = create<WorkbenchState>((set) => ({
  activeFile: null,
  files: [],
  terminalOutput: '',
  isThinking: false,
  setActiveFile: (path) => set({ activeFile: path }),
  setFiles: (files) => set({ files }),
  appendTerminalOutput: (output) => 
    set((state) => ({ terminalOutput: state.terminalOutput + output })),
  setIsThinking: (isThinking) => set({ isThinking }),
}));
