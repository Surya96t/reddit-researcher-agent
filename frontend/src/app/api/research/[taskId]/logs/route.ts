import { NextResponse } from "next/server";

// Note the function signature now includes a 'logs' segment in the path
export async function GET(
  request: Request,
  { params }: { params: { taskId: string } }
) {
  try {
    const { taskId } = await params; // No await needed in Route Handlers

    const apiResponse = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/research/${taskId}/logs`);

    if (!apiResponse.ok) {
      return NextResponse.json({ error: "Failed to fetch task logs" }, { status: apiResponse.status });
    }

    const data = await apiResponse.json();
    return NextResponse.json(data);

  } catch (error) {
    console.error("BFF Error fetching logs:", error);
    return NextResponse.json(
      { error: "An internal server error occurred" },
      { status: 500 }
    );
  }
}