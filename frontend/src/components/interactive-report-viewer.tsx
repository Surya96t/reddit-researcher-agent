"use client";

import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { SourcePost } from "@/lib/types";
import { ExternalLink, Link as LinkIcon } from "lucide-react";
import Link from "next/link";

interface InteractiveReportViewerProps {
  reportContent: string;
  sourcePosts: SourcePost[];
}

export function InteractiveReportViewer({ reportContent, sourcePosts }: InteractiveReportViewerProps) {
  // Use an effect to add links after the component mounts
  useEffect(() => {
    // Find all list items in the rendered Markdown
    const listItems = document.querySelectorAll("#report-content ul > li");

    listItems.forEach(item => {
      const itemText = item.textContent || "";
      // Check if this list item describes a solution idea
      if (itemText.toLowerCase().startsWith("solution idea:")) {
        // Find the corresponding source post in our data
        const sourcePost = sourcePosts.find(p => itemText.includes(p.title));
        
        // This is a simplified matching logic. A more robust way would be
        // to embed IDs in the markdown, but this works for many cases.
        // A better approach would be to match the solution idea text to the
        // idea object, then use the source_post_id to find the post.

        // Let's use a unique identifier for the link
        const linkId = `source-link-${sourcePost?.id}`;
        
        // Avoid adding duplicate links
        if (sourcePost && !document.getElementById(linkId)) {
          const linkElement = document.createElement("a");
          linkElement.id = linkId;
          linkElement.href = `#source-${sourcePost.id}`;
          linkElement.className = "text-primary hover:underline text-xs ml-2 font-sans";
          linkElement.innerHTML = `[Source]`;
          item.appendChild(linkElement);
        }
      }
    });
  }, [reportContent, sourcePosts]);

  return (
    <div className="space-y-8">
      {/* The main report card */}
      <Card>
        <CardHeader>
          <CardTitle>Research Report</CardTitle>
        </CardHeader>
        <CardContent>
          <div id="report-content" className="prose dark:prose-invert max-w-none">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {reportContent}
            </ReactMarkdown>
          </div>
        </CardContent>
      </Card>

      {/* The "Evidence" section at the bottom */}
      <Card>
        <CardHeader>
          <CardTitle>Evidence: Source Posts</CardTitle>
          <CardDescription>
            These are the original Reddit posts from which the ideas in the report were derived.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {sourcePosts.map((post) => (
              <div key={post.id} id={`source-${post.id}`} className="p-3 bg-secondary rounded-lg border">
                <Link href={post.url} target="_blank" className="font-semibold text-sm hover:underline flex items-center group">
                  {post.title}
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
    </div>
  );
}