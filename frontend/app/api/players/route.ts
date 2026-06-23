import { NextResponse } from "next/server";

export async function GET() {
  const res = await fetch(`${process.env.BACKEND_URL}/players`);
  const data = await res.json();
  return NextResponse.json(data);
}
