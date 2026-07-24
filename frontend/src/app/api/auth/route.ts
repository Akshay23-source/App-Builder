import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    return NextResponse.json({ status: "success", received: body });
  } catch (error) {
    return NextResponse.json({ error: "Invalid request payload" }, { status: 400 });
  }
}
