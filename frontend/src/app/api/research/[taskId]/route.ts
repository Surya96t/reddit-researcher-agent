import { NextResponse } from "next/server";

export async function GET(
  request: Request,
  { params }: { params: { taskId: string } }
) {
  try {
    const { taskId } = await params;

    const apiResponse = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/research/${taskId}`);

    if (!apiResponse.ok) {
      return NextResponse.json({ error: "Failed to fetch task status" }, { status: apiResponse.status });
    }

    const data = await apiResponse.json();
    return NextResponse.json(data);

  } catch (error) {
    console.error("BFF Error:", error);
    return NextResponse.json(
      { error: "An internal server error occurred" },
      { status: 500 }
    );
  }
}