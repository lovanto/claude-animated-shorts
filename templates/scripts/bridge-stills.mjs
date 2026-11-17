// usage: node scripts/bridge-stills.mjs <outPrefix> <frame,frame,...> [scale]  (bundles once, GPU via ANGLE, jpeg)
// BRIDGE_ENTRY=src/sandboxes/<name>/index.tsx renders a sandbox copy instead of the main project entry.
import fs from "node:fs";
// each bundle copies public/ (~1.3 GB) into the temp dir; C: is full, so keep bundles on D:
// Remotion bundles fill the temp folder (~1.3 GB each): set REMOTION_TMP to a folder on a big drive
if (process.env.REMOTION_TMP) { fs.mkdirSync(process.env.REMOTION_TMP, { recursive: true }); process.env.TEMP = process.env.TMP = process.env.REMOTION_TMP; }
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import path from "node:path";
const [prefix, frames, scale = "0.5"] = process.argv.slice(2);
// Linux hybrid laptops (Intel + NVIDIA, prime-select on-demand) render on the Intel iGPU by default. Force the NVIDIA Vulkan ICD
// before Chrome is spawned, and use ANGLE's Vulkan backend. Override with BRIDGE_GL / BROWSER; BRIDGE_GL=angle keeps the old path.
const isLinux = process.platform === "linux";
if (isLinux && !process.env.BRIDGE_NO_NVIDIA) {
  Object.assign(process.env, { __NV_PRIME_RENDER_OFFLOAD: "1", __VK_LAYER_NV_optimus: "NVIDIA_only", VK_ICD_FILENAMES: "/usr/share/vulkan/icd.d/nvidia_icd.json" });
}
const browserExecutable = process.env.BROWSER || (isLinux ? "/usr/bin/google-chrome" : "C:/Program Files/Google/Chrome/Application/chrome.exe");
const chromiumOptions = { gl: process.env.BRIDGE_GL || (isLinux ? "vulkan" : "angle") };
const serveUrl = await bundle({ entryPoint: path.resolve(process.env.BRIDGE_ENTRY || "src/index.ts"), publicDir: path.resolve("public") });
const composition = await selectComposition({ serveUrl, id: "BridgeShort", browserExecutable, chromiumOptions });
const onBrowserLog = (l) => { if (l.type === "error" || l.type === "warning") console.log(`[${l.type}]`, l.text.slice(0, 300)); };
for (const f of frames.split(",").map(Number)) {
  const t0 = Date.now();
  await renderStill({ composition, serveUrl, frame: f, output: `${prefix}${f}.jpg`, imageFormat: "jpeg", jpegQuality: 88, scale: Number(scale),
    browserExecutable, chromiumOptions, timeoutInMilliseconds: 180000, onBrowserLog });
  console.log("still", f, ((Date.now() - t0) / 1000).toFixed(1) + "s");
}
