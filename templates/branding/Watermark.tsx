import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";

/** Totoversity channel mark: avatar + name, top-left, inside the Shorts safe area. Applied to every short from Root.tsx. */
export const Watermark: React.FC = () => (
  <AbsoluteFill style={{ pointerEvents: "none" }}>
    <div style={{ position: "absolute", left: 48, top: 150, display: "flex", alignItems: "center", gap: 16, opacity: 0.85 }}>
      <Img src={staticFile("totoversity/profile.png")} style={{ width: 84, height: 84, borderRadius: "50%" }} />
      <span style={{ fontFamily: "Arial Black, Impact, sans-serif", fontSize: 40, color: "#fff", textShadow: "0 3px 0 #0a1a6b, 0 0 12px rgba(0,0,0,.6)" }}>Totoversity</span>
    </div>
  </AbsoluteFill>
);

export const withWatermark = <P extends object>(C: React.ComponentType<P>): React.FC<P> => (props) => (
  <AbsoluteFill>
    <C {...props} />
    <Watermark />
  </AbsoluteFill>
);
