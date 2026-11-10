import { NextResponse } from "next/server";

const MCP_URL =
  process.env.MCP_SERVER_URL ||
  "http://127.0.0.1:3480/mcp/VrW5q_4p8xqZNesWLPaymvH2iX-bL1NB";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const res = await fetch(MCP_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json, text/event-stream",
      },
      body: JSON.stringify(body),
    });
    const text = await res.text();
    return new NextResponse(text, {
      status: res.status,
      headers: { "Content-Type": "application/json" },
    });
  } catch (err: any) {
    return NextResponse.json(
      { jsonrpc: "2.0", error: { code: -32603, message: err?.message || "Internal error" }, id: null },
      { status: 500 },
    );
  }
}
