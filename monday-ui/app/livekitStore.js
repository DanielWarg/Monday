"use client";
import { createContext, useContext, useEffect, useRef, useState } from "react";
import { Room, RoomEvent } from "livekit-client";

const LKContext = createContext(null);
export function useLiveKit() { const ctx = useContext(LKContext); if (!ctx) throw new Error("useLiveKit must be inside provider"); return ctx; }

export function LiveKitProvider({ children, tokenUrl = "/api/token", wsUrl = process.env.NEXT_PUBLIC_LIVEKIT_URL || "" }){
  const roomRef = useRef(null);
  const [status, setStatus] = useState("idle");
  const [partials, setPartials] = useState("");
  const [finals, setFinals] = useState([]);
  const [showPartials, setShowPartials] = useState(true);
  const [listening, setListening] = useState(false);

  useEffect(()=>{
    let mounted = true; let room;
    async function start(){
      setStatus("connecting");
      try{
        const r = await fetch(tokenUrl);
        const j = await r.json();
        if (!j || !j.ok || !j.token){ setStatus("error"); return; }
        room = new Room();
        await room.connect(wsUrl, j.token);
        roomRef.current = room;
        setStatus("connected");
        room.on(RoomEvent.DataReceived, (payload, participant, kind)=>{
          try{
            const obj = JSON.parse(new TextDecoder().decode(payload));
            if (obj && obj.type === 'transcript_partial'){
              setListening(true);
              if (showPartials) setPartials(obj.text);
            } else if (obj && obj.type === 'transcript_final'){
              setFinals(f=> [{ id: `${obj.ts||Date.now()}`, text: obj.text }, ...f].slice(0,50));
              setPartials("");
              setListening(false);
            }
          }catch(_){ }
        });
      }catch(_){ setStatus("error"); }
    }
    if (wsUrl){ start(); }
    return ()=>{ mounted=false; try{ room && room.disconnect(); }catch(_){} };
  }, [tokenUrl, wsUrl, showPartials]);

  return (
    <LKContext.Provider value={{ status, partials, finals, setShowPartials, showPartials, listening }}>
      {children}
    </LKContext.Provider>
  );
}
