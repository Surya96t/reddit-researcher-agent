// src/app/api/research/[taskId]/route.ts

import { NextRequest, NextResponse } from "next/server";

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ taskId: string }> }
) {
  try {
    const { taskId } = await params;

    const apiResponse = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/research/${taskId}`);

    if (!apiResponse.ok) {
      return NextResponse.json({ error: "Failed to fetch task data" }, { status: apiResponse.status });
    }

    const data = await apiResponse.json();
    return NextResponse.json(data);

  } catch (error) {
    console.error("BFF Error fetching task data:", error);
    return NextResponse.json(
      { error: "An internal server error occurred" },
      { status: 500 }
    );
  }
}