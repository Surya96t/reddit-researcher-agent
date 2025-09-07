"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ExternalLink } from "lucide-react";
import Link from "next/link";
// --- CHANGE THIS IMPORT ---
import { SourcePost } from "@/lib/types";

// The SourcePost interface is now imported, not defined here.

interface SourcePostsDisplayProps {
  posts: SourcePost[];
}

export function SourcePostsDisplay({ posts }: SourcePostsDisplayProps) {
  if (posts.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Relevant Source Posts</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            The agent is searching for relevant posts...
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Relevant Source Posts</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {posts.map((post) => (
            // --- ADD HOVER AND TRANSITION CLASSES ---
            <div key={post.id} className="p-3 bg-secondary rounded-lg border hover:border-primary transition-all hover:shadow-sm">
              <Link href={post.url} target="_blank" className="font-semibold text-sm hover:underline flex items-center group">
                {post.title}
                {/* --- ADD GROUP-HOVER EFFECT --- */}
                <ExternalLink className="h-4 w-4 ml-2 text-muted-foreground group-hover:text-primary transition-colors" />
              </Link>
              <p className="text-xs text-muted-foreground mt-1">
                Score: {post.score} | Comments: {post.num_comments}
              </p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}