"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CheckCircle, CircleDashed, AlertCircle } from "lucide-react";

// Define a type for our task object for type safety
export interface Task {
  id: string;
  status: "PENDING" | "IN_PROGRESS" | "COMPLETED" | "FAILED";
  query: string;
}

interface StatusDisplayProps {
  task: Task;
}

const statusConfig = {
  PENDING: {
    icon: <CircleDashed className="h-6 w-6 animate-spin text-muted-foreground" />,
    text: "Your research task is pending and will start shortly.",
  },
  IN_PROGRESS: {
    icon: <CircleDashed className="h-6 w-6 animate-spin text-blue-500" />,
    text: "The AI agent is currently researching... This may take a few minutes.",
  },
  COMPLETED: {
    icon: <CheckCircle className="h-6 w-6 text-green-500" />,
    text: "Research complete! Your report is ready.",
  },
  FAILED: {
    icon: <AlertCircle className="h-6 w-6 text-red-500" />,
    text: "An error occurred during research. Please try again.",
  },
};

export function StatusDisplay({ task }: StatusDisplayProps) {
  const { icon, text } = statusConfig[task.status] || statusConfig.PENDING;

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Research in Progress</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="flex items-center space-x-4 p-4 bg-secondary rounded-lg">
            <div className="flex-shrink-0">{icon}</div>
            <div>
              <p className="font-semibold">Status: {task.status}</p>
              <p className="text-muted-foreground text-sm">{text}</p>
            </div>
          </div>
          <div>
            <h3 className="font-semibold text-sm">Your Query:</h3>
            <p className="text-muted-foreground p-2 border rounded-md text-sm">
              {task.query}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}