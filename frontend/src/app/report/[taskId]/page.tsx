// frontend/src/app/report/[taskId]/page.tsx

import { ThemeToggle } from "@/components/theme-toggle";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { InteractiveReportViewer } from "@/components/interactive-report-viewer";
// --- CHANGE THIS IMPORT ---
import { FullTaskData } from "@/lib/types";


// Function to fetch all data for the report page
async function getReportData(taskId: string): Promise<FullTaskData | null> {
    try {
        const res = await fetch(`${process.env.API_BASE_URL}/api/v1/research/${taskId}`, {
            cache: 'no-store' // Always fetch the latest data for the report
        });

        if (!res.ok) { return null; }
        const data = await res.json();
        return data;

    } catch (error) {
        console.error("Failed to fetch report data:", error);
        return null;
    }
}

export default async function ReportPage({ params }: { params: Promise<{ taskId: string }> }) {
  const { taskId } = await params;
  const taskData = await getReportData(taskId);

  if (!taskData || !taskData.report) {
    return (
        <main className="container mx-auto max-w-4xl py-12 space-y-6 text-center">
            <h1 className="text-2xl font-bold">Report Not Found</h1>
            <p>The report for this task could not be loaded or is not yet available.</p>
            <Button asChild variant="outline">
                <Link href="/">← Start New Research</Link>
            </Button>
        </main>
    );
  }

  return (
    <>
      <header className="py-4">
        <nav className="container mx-auto flex justify-end">
          <ThemeToggle />
        </nav>
      </header>
      <main className="container mx-auto max-w-4xl py-12 space-y-6">
        <Button asChild variant="outline">
          <Link href="/">← Start New Research</Link>
        </Button>
        {/* --- Use the new interactive component --- */}
        <InteractiveReportViewer
          reportContent={taskData.report.content}
          sourcePosts={taskData.source_posts}
        />
      </main>
    </>
  );
}