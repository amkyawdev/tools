import { NextResponse } from "next/server";

export async function GET(request: Request, { params }: { params: { path: string[] } }) {
  const backendUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const path = params.path.join("/");
  const url = new URL(request.url);
  const query = url.search;
  const response = await fetch(`${backendUrl}/${path}${query}`, { headers: { "Content-Type": "application/json" } });
  const data = await response.json();
  return NextResponse.json(data, { status: response.status });
}

export async function POST(request: Request, { params }: { params: { path: string[] } }) {
  const backendUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const path = params.path.join("/");
  const body = await request.json();
  const response = await fetch(`${backendUrl}/${path}`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  const data = await response.json();
  return NextResponse.json(data, { status: response.status });
}
