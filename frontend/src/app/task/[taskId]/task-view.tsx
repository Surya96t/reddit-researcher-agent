// frontend/src/app/task/[taskId]/task-view.tsx

"use client";

import useSWR from 'swr';
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { StatusDisplay } from '@/components/status-display';
import { LogDisplay } from '@/components/log-display';
import { SourcePostsDisplay } from '@/components/source-posts-display';
import { ExtractedIdeasDisplay } from '@/components/extracted-ideas-display';
import { TaskViewSkeleton } from '@/components/task-view-skeleton';
import { FullTaskData } from '@/lib/types';
import { useEffect, useRef } from 'react'; // <-- Add useEffect and useRef

interface FetchError extends Error {
    info?: string;
    status?: number;
}

const fetcher = (url: string) => fetch(url).then(res => {
    if (!res.ok) {
        const error: FetchError = new Error('An error occurred while fetching the data.');
        error.info = res.statusText;
        error.status = res.status;
        throw error;
    }
    return res.json()
});

interface TaskViewProps {
  taskId: string;
}

export default function TaskView({ taskId }: TaskViewProps) {
  const { data, error, isLoading } = useSWR<FullTaskData>(
    `/api/research/${taskId}`,
    fetcher,
    {
      refreshInterval: (latestData) => 
        latestData?.status === 'COMPLETED' || latestData?.status === 'FAILED' ? 0 : 2000,
      onError: (err) => {
        // This toast is for NETWORK errors
        toast.error(`Network Error: ${err.status || 'Failed to fetch'}`);
      }
    }
  );

  // --- THIS IS THE NEW LOGIC ---
  // Use a ref to track the previous status to avoid showing toasts on initial load
  const prevStatusRef = useRef<string | undefined>(undefined);

  useEffect(() => {
    if (data?.status && data.status !== prevStatusRef.current) {
      if (data.status === 'FAILED') {
        // This toast is for TASK failures
        toast.error("The research agent encountered a critical error.");
      }
      if (data.status === 'COMPLETED') {
        // Optional: Show a success toast
        toast.success("Research complete! Your report is ready.");
      }
    }
    // Update the ref with the current status for the next render
    prevStatusRef.current = data?.status;
  }, [data?.status]); // This effect runs only when the status changes


  // --- The rest of the render logic is the same ---
  if (error) {
    return (
      <div className="text-center text-red-500 ...">
        <h2 className="text-2xl font-bold mb-4">Error Loading Task</h2>
        <p className="mb-4">There was an error loading your research task. Please try again later.</p>
        <p className="text-sm text-muted-foreground mb-6">
          {error.message} {error.info ? `- ${error.info}` : ''}
        </p>
      </div>
    );
  }

  if (isLoading) {
    return <TaskViewSkeleton />;
  }
  
  const taskData = data!;
  const isRunning = taskData.status === 'PENDING' || taskData.status === 'IN_PROGRESS';
  
  return (
    <div className="space-y-8">
      <StatusDisplay task={taskData} />
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <SourcePostsDisplay posts={taskData.source_posts || []} />
        <ExtractedIdeasDisplay ideas={taskData.extracted_ideas || []} />
      </div>

      {isRunning && <LogDisplay logs={taskData.logs || []} />}
    
      {taskData.status === "COMPLETED" && (
        <div className="text-center py-8">
          <Button asChild size="lg">
            <Link href={`/report/${taskData.id}`}>View Full Report</Link>
          </Button>
        </div>
      )}
      {taskData.status === "FAILED" && (
        <div className="text-center py-8">
          <Button asChild variant="secondary">
              <Link href={`/`}>Start a New Research</Link>
          </Button>
        </div>
      )}
    </div>
  );
}