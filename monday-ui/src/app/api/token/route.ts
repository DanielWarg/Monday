import { NextResponse } from "next/server";

export async function GET() {
  const url = process.env.NEXT_PUBLIC_LIVEKIT_URL || "";
  const tokenUrl = process.env.NEXT_PUBLIC_TOKEN_URL || "";
  try {
    if (tokenUrl) {
      const r = await fetch(tokenUrl);
      if (r.ok) {
        const data = await r.json();
        return NextResponse.json({ token: data.token || "mock-token", url: data.url || url });
      }
    }
  } catch {}
  return NextResponse.json({ token: "mock-token", url });
}
