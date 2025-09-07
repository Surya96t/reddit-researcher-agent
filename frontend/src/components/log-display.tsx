// frontend/src/components/log-display.tsx

"use-client";

import { useEffect, useRef } from 'react';
// --- CHANGE THIS IMPORT ---
import { TaskLog } from "@/lib/types";


interface LogDisplayProps {
  logs: TaskLog[];
}

export function LogDisplay({ logs }: LogDisplayProps) {
  const logContainerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to the bottom of the log container whenever new logs arrive
  useEffect(() => {
    if (logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
  }, [logs]);

  return (
    <div className="space-y-2">
      <h3 className="font-semibold text-sm">Agent Log Stream</h3>
      <div 
        ref={logContainerRef}
        className="h-64 overflow-y-auto rounded-md bg-muted p-4 font-mono text-sm"
      >
        {logs.length > 0 ? (
          logs.map((log) => (
            <p key={log.id} className="whitespace-pre-wrap break-words">
              {log.message}
            </p>
          ))
        ) : (
          <p className="text-muted-foreground">Waiting for agent to start...</p>
        )}
      </div>
    </div>
  );
}