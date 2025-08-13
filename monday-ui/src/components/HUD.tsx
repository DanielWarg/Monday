import React, { useState, useRef } from "react";
import type { Room } from "livekit-client";

export default function HUD(){
  const [status, setStatus] = useState<string>("Disconnected");
  const [bargeIn, setBargeIn] = useState<boolean>(false);
  const roomRef = useRef<Room | null>(null);
  const connectingRef = useRef(false);

  async function connect(){
    if (connectingRef.current) return;
    connectingRef.current = true;
    try {
      setStatus("Fetching token…");
      const r = await fetch("/api/token");
      const j = await r.json();
      const { token, url } = j || {};
      if (!token || !url){ setStatus("Token/url saknas"); return; }
      setStatus("Connecting LiveKit…");
      const { Room } = await import("livekit-client");
      const room = new Room();
      await room.connect(url, token);
      roomRef.current = room;
      setStatus("Connected");
      // TODO: lyssna på metadata-events: transcript_partial, transcript_final, assistant_speaking, tool_called, tool_result
      // room.on(dataReceived, ...)\n    } catch (e:any) {\n      setStatus(`Error: ${e?.message||String(e)}`);\n    } finally { connectingRef.current = false; }\n  }\n\n  async function disconnect(){\n    try { roomRef.current?.disconnect(); } catch {}\n    roomRef.current = null;\n    setStatus("Disconnected");\n  }\n\n  return (\n    <div className="rounded-xl border border-cyan-400/20 p-4 bg-cyan-900/20">\n      <div className="flex items-center gap-3">\n        <div className={`h-2 w-2 rounded-full ${status==="Connected"?"bg-green-400":"bg-cyan-400"}`} title={status} />\n        <div className="text-cyan-100 text-sm">{status}</div>\n        <div className="ml-auto flex items-center gap-2">\n          <button onClick={connect} className="rounded-xl border border-cyan-400/30 px-3 py-1 text-xs hover:bg-cyan-400/10">Connect</button>\n          <button onClick={disconnect} className="rounded-xl border border-cyan-400/30 px-3 py-1 text-xs hover:bg-cyan-400/10">Disconnect</button>\n        </div>\n      </div>\n      <div className="mt-3 text-xs text-cyan-300/80">\n        Barge-in: <span className={`inline-block h-2 w-2 rounded-full ${bargeIn?"bg-amber-400":"bg-cyan-400/40"}`} title={bargeIn?"User speaking":"Idle"} />\n      </div>\n      <div className="mt-3 grid gap-3 md:grid-cols-2">\n        <div className="rounded-lg border border-cyan-400/10 p-2">\n          <div className="text-[11px] text-cyan-300/60 mb-1">Transkript</div>\n          <div className="text-cyan-100 text-sm min-h-[60px]">{/* TODO: fyll med transcript_partial/final */}</div>\n        </div>\n        <div className="rounded-lg border border-cyan-400/10 p-2">\n          <div className="text-[11px] text-cyan-300/60 mb-1">Tool-logg</div>\n          <div className="text-cyan-100 text-sm min-h-[60px]">{/* TODO: fyll med tool_called/tool_result */}</div>\n        </div>\n      </div>\n    </div>\n  );\n}\n