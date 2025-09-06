"use client";

import useSWR from 'swr';
import { StatusDisplay, Task } from "@/components/status-display";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { LogDisplay, LogEntry } from '@/components/log-display';

const fetcher = (url: string) => fetch(url).then(res => res.json());

interface TaskViewProps {
  taskId: string;
}

export default function TaskView({ taskId }: TaskViewProps) {
  // SWR hook for the main task status
  const { data: task, error: taskError } = useSWR<Task>(
    `/api/research/${taskId}`,
    fetcher,
    {
      refreshInterval: (latestData) => 
        latestData?.status === 'COMPLETED' || latestData?.status === 'FAILED' ? 0 : 2000
    }
  );

  // SWR hook for the task logs
  const { data: logs, error: logsError } = useSWR<LogEntry[]>(
    (task && (task.status === 'PENDING' || task.status === 'IN_PROGRESS'))
      ? `/api/research/${taskId}/logs`
      : null,
    fetcher,
    { 
      refreshInterval: 2000
    }
  );

  if (taskError) return <div>Failed to load task status.</div>;
  if (!task) {
    return (
      <StatusDisplay task={{ task_id: taskId, status: 'PENDING', query: "Loading task details..." }} />
    );
  }

  const isRunning = task.status === 'PENDING' || task.status === 'IN_PROGRESS';

  return (
    <div className="space-y-6">
      <StatusDisplay task={task} />
      
      {isRunning && (
        <>
          {/* --- ADD THIS ERROR HANDLING BLOCK --- */}
          {logsError && (
            <div className="text-red-500 text-sm">
              Could not load logs. Retrying...
            </div>
          )}
          <LogDisplay logs={logs || []} />
        </>
      )}
    
      {task.status === "COMPLETED" && (
        <div className="text-center">
          <Button asChild>
            <Link href={`/report/${taskId}`}>View Full Report</Link>
          </Button>
        </div>
      )}
      {task.status === "FAILED" && (
        <div className="text-center">
            <Button asChild variant="secondary">
                <Link href={`/`}>Start a New Research</Link>
            </Button>
        </div>
      )}
    </div>
  );
}