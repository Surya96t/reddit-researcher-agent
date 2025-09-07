"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Lightbulb } from "lucide-react";
// --- CHANGE THIS IMPORT ---
import { ExtractedIdea } from "@/lib/types";

// The ExtractedIdea interface is now imported, not defined here.

interface ExtractedIdeasDisplayProps {
  ideas: ExtractedIdea[];
}

export function ExtractedIdeasDisplay({ ideas }: ExtractedIdeasDisplayProps) {
  if (ideas.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Emerging Ideas</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            The agent is analyzing posts for business ideas...
          </p>
        </CardContent>
      </Card>
    );
  }
  
  return (
    <Card>
      <CardHeader>
        <CardTitle>Emerging Ideas</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {ideas.map((idea) => (
            // --- ADD HOVER AND TRANSITION CLASSES ---
            <div key={idea.id} className="p-3 bg-secondary rounded-lg border hover:border-primary transition-all hover:shadow-sm">
              <div className="flex items-start space-x-3">
                  <Lightbulb className="h-5 w-5 mt-1 text-yellow-500 flex-shrink-0" />
                  <div>
                      {/* --- ADD STYLING FOR VISUAL HIERARCHY --- */}
                      <p className="font-semibold text-sm text-primary">{idea.solution_idea}</p>
                      <p className="text-xs text-muted-foreground mt-1">
                          <strong className="font-medium text-foreground">Pain Point:</strong> {idea.pain_point}
                      </p>
                  </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}