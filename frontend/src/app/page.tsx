"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ThemeToggle } from "@/components/theme-toggle";
import { ResearchForm } from "@/components/research-form";

export default function HomePage() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const router = useRouter();

  const handleFormSubmit = async (query: string) => {
    setIsSubmitting(true);
    
    try {
      // --- Call our new BFF API route ---
      const response = await fetch('/api/research', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        // Handle API errors (e.g., show a toast notification)
        console.error("Failed to start task");
        // We could add user-facing error handling here
        setIsSubmitting(false);
        return;
      }

      const result = await response.json();
      const { task_id } = result;

      // Redirect to the task page with the real task ID
      router.push(`/task/${task_id}`);

    } catch (error) {
      console.error("Submission error:", error);
      setIsSubmitting(false);
      // Handle fetch errors (e.g., network issues)
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