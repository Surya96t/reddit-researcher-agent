import { ReportViewer } from "@/components/report-viewer";
import { ThemeToggle } from "@/components/theme-toggle";
import { Button } from "@/components/ui/button";
import Link from "next/link";

// Define a type for the expected API response
interface TaskWithReport {
    task_id: string;
    status: string;
    query: string;
    report: {
        id: string;
        content: string;
        created_at: string;
    } | null;
}

// Function to fetch data server-side
async function getReport(taskId: string): Promise<TaskWithReport | null> {
    try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/research/${taskId}`, {
            // Revalidate every 60 seconds, or on-demand
            next: { revalidate: 60 }
        });

        if (!res.ok) {
            return null;
        }
        return res.json();
    } catch (error) {
        console.error("Failed to fetch report:", error);
        return null;
    }
}



export default async function ReportPage({ params }: { params: { taskId: string } }) {
  const { taskId } = await params;
  const taskData = await getReport(taskId);

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
        <ReportViewer content={taskData.report.content} />
      </main>
    </>
  );
}
