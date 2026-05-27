'use client';

import React, { useEffect, useRef } from 'react';
import { Terminal as XTerm } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import 'xterm/css/xterm.css';
import { Terminal as TerminalIcon } from 'lucide-react';

export const Terminal = () => {
  const terminalRef = useRef<HTMLDivElement>(null);
  const xtermRef = useRef<XTerm | null>(null);
  const fitAddonRef = useRef<FitAddon | null>(null);

  useEffect(() => {
    if (!terminalRef.current) return;

    const term = new XTerm({
      cursorBlink: true,
      fontSize: 14,
      fontFamily: 'Menlo, Monaco, "Courier New", monospace',
      theme: {
        background: '#000000',
        foreground: '#ffffff',
      },
    });

    const fitAddon = new FitAddon();
    term.loadAddon(fitAddon);
    term.open(terminalRef.current);
    
    xtermRef.current = term;
    fitAddonRef.current = fitAddon;

    // Helper to fit terminal with safety checks
    const safeFit = () => {
      try {
        if (terminalRef.current && terminalRef.current.clientWidth > 0) {
          fitAddon.fit();
        }
      } catch (err) {
        console.warn('Terminal fit failed:', err);
      }
    };

    // Initial fit with a small delay
    const timer = setTimeout(safeFit, 100);

    term.writeln('\x1b[32mWelcome to MasterBlack AI Terminal\x1b[0m');
    term.write('\x1b[34m$ \x1b[0m');

    const handleResize = () => safeFit();
    window.addEventListener('resize', handleResize);

    return () => {
      clearTimeout(timer);
      window.removeEventListener('resize', handleResize);
      term.dispose();
    };
  }, []);

  return (
    <div className="h-64 bg-black border-t border-[#333] flex flex-col">
      <div className="flex items-center gap-2 px-4 py-2 bg-[#252526] text-xs font-semibold text-gray-400 border-b border-[#333]">
        <TerminalIcon size={14} /> Terminal
      </div>
      <div ref={terminalRef} className="flex-1 overflow-hidden p-2" />
    </div>
  );
};
