"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";

// Update the props interface
interface ResearchFormProps {
  onSubmit: (query: string, subreddits: string) => void;
  isSubmitting: boolean;
}

export function ResearchForm({ onSubmit, isSubmitting }: ResearchFormProps) {
  const [query, setQuery] = useState("");
  const [subreddits, setSubreddits] = useState("startups,saas,Entrepreneur"); // Add default value

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (query.trim() && subreddits.trim()) {
      // Pass both values to the onSubmit handler
      onSubmit(query.trim(), subreddits.trim());
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Start a New Research Task</CardTitle>
        <CardDescription>Enter a topic and the subreddits you want to search.</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
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
          
          {/* --- NEW SUBREDDIT INPUT FIELD --- */}
          <div className="flex flex-col space-y-2">
            <Label htmlFor="subreddits">Target Subreddits</Label>
            <Input
              id="subreddits"
              placeholder="e.g., startups,saas,webdev"
              value={subreddits}
              onChange={(e) => setSubreddits(e.target.value)}
              disabled={isSubmitting}
            />
             <p className="text-xs text-muted-foreground">
                Enter as comma-separated names, without the &quot;r/&quot;.
            </p>
          </div>

          <Button type="submit" disabled={isSubmitting || !query.trim() || !subreddits.trim()}>
            {isSubmitting ? "Starting Research..." : "Start Research"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}