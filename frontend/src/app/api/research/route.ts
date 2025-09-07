// frontend/src/app/api/research/route.ts

import { NextResponse } from "next/server";

export async function POST(request: Request) {
    try {
        const body = await request.json();
        const { query, subreddits } = body;

        if (!query || !subreddits) {
            return NextResponse.json(
                { error: "Query and subreddits are required" },
                { status: 400 }
            );
        }

        // This is the server-to-server call to our FastAPI backend
        const apiResponse = await fetch(
            `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/research`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ query, subreddits }),
            }
        );

        if (!apiResponse.ok) {
            // Log the error and forward a generic error message
            const errorBody = await apiResponse.text();
            console.error("FastAPI error:", errorBody);
            return NextResponse.json(
                { error: "Failed to start research task" },
                { status: apiResponse.status }
            );
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