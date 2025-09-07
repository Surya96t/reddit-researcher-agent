// frontend/src/app/page.tsx

"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ThemeToggle } from "@/components/theme-toggle";
import { ResearchForm } from "@/components/research-form";
import { toast } from "sonner";

export default function HomePage() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const router = useRouter();

  // Update the function signature to accept subreddits
  const handleFormSubmit = async (query: string, subreddits: string) => {
    setIsSubmitting(true);
    
    try {
      const response = await fetch('/api/research', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        // --- Add subreddits to the request body ---
        body: JSON.stringify({ query, subreddits }),
      });

      if (!response.ok) {
        toast.error("Failed to start the research task. Please try again later.");
        console.error("Failed to start task, server responded with:", response.status);
        setIsSubmitting(false);
        return;
      }

      const result = await response.json();
      const { task_id } = result;
      router.push(`/task/${task_id}`);

    } catch (error) {
      toast.error("A network error occurred. Please check your connection.");
      console.error("Submission error:", error);
      setIsSubmitting(false);
    }
  };

  return (
    <>
      <header className="py-4">
        <nav className="container mx-auto flex justify-end">
          <ThemeToggle />
        </nav>
      </header>

      <main className="container mx-auto max-w-2xl py-12">
        <div className="text-center mb-10">
          <h1 className="text-4xl font-bold">AI Reddit Researcher</h1>
          <p className="text-muted-foreground mt-2">
            Enter a topic to find out what people want built.
          </p>
        </div>
        <ResearchForm onSubmit={handleFormSubmit} isSubmitting={isSubmitting} />
      </main>
    </>
  );
}