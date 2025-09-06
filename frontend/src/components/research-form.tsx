"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";

// Define the props interface for the component
interface ResearchFormProps {
  onSubmit: (query: string) => void;
  isSubmitting: boolean;
}

export function ResearchForm({ onSubmit, isSubmitting }: ResearchFormProps) {
  const [query, setQuery] = useState("");

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault(); // Prevent the default form submission
    if (query.trim()) {
      onSubmit(query.trim());
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Start a New Research Task</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit}>
          <div className="grid w-full items-center gap-4">
            <div className="flex flex-col space-y-2">
              <Label htmlFor="query">Research Topic</Label>
              <Input
                id="query"
                placeholder="e.g., AI tools for small business owners"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                disabled={isSubmitting}
              />
            </div>
            <Button type="submit" disabled={isSubmitting || !query.trim()}>
              {isSubmitting ? "Starting Research..." : "Start Research"}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}