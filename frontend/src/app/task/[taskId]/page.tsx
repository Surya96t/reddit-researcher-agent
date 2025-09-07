// src/app/task/[taskId]/page.tsx

import { ThemeToggle } from "@/components/theme-toggle";
import TaskView from "./task-view";

// This is the parent Server Component
export default async function TaskPage({ params }: { params: Promise<{ taskId: string }> }) {
  const { taskId } = await params;

  return (
    <>
      <header className="py-4">
        <nav className="container mx-auto flex justify-end">
          <ThemeToggle />
        </nav>
      </header>
      <main className="container mx-auto max-w-2xl py-12">
        {/* Render the Client Component and pass the resolved taskId */}
        <TaskView taskId={taskId} />
      </main>
    </>
  );
}