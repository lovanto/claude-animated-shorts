---
name: cartoon-3d-short
description: Make a ~55-70 s vertical cartoon story short in the "2D characters in a colourful 3D world" style (flat bean-head cartoon cards with ink outlines, painted 3D town/world with black ink lines, saturated sky, depth-of-field backgrounds, gliding cameras, voice narration, synthesized SFX + march-style music), rendered with three.js inside Remotion. Proven on "The Bridge That Fell for a Song" (2026-10-31). Use when the user asks for another video "like the bridge video", "like the soldiers/bridge short", "in that cartoon 3D style", a history/science story short with cartoon characters in 3D, or says "use the cartoon short skill".
---

# Cartoon 3D story short (three.js + Remotion)

## Local setup (this machine, Linux)
- Remotion project: `/home/lovanto/Documents/totoversity/shorts` (composition source in `src/videos/<name>/`, helper scripts in `scripts/`, models in `public/bridge/kenney/`).
- Sound/voice per short: `/home/lovanto/Documents/totoversity/shorts-audio/<name>/{audio,voice}/` (`mix.py` expects `voice/voice.wav` at 48 kHz PCM and `voice/words.json` with `s`/`e` seconds per word).
- Run Node commands from `/home/lovanto/Documents/totoversity/shorts`; use the downloaded Chrome Headless Shell (no `browserExecutable`), `gl: "angle"`.
- Pinned stack: Remotion 4.0.290, React 19.1.0, three 0.175.0, R3F 9.1.2. Do not upgrade.

Proven example: **The Bridge That Fell for a Song**. It is an original 67 s short about the 1831 Broughton bridge and 74 soldiers marching in step.
- Code: `src/videos/bridge/` of your Remotion project (composition `BridgeShort`, 1080x1920, 30 fps).
- Script, voice and sound: `/home/lovanto/Documents/totoversity/shorts-audio/bridge/`.
- Style research: `references/`.

The style reference is a channel studied privately (`references/`: STYLE_BIBLE.md, reports/*.md, frames/).
- Those videos are private study material. Never upload, publish or send them.
- Never copy their scripts, characters or shots. Story, characters and voice are always OUR OWN.
- Never say the channel's name in a voice-over or description.

User rules that apply:
- No text on props/signs in the picture (use pictograms, gestures, blank paper, tally marks, no digits). **Subtitles ARE burned in** (user decision 2026-11-17): every short delivers `<name>_subtitles.srt` + `.vtt` AND a burned `<name>_captioned.mp4` (big bold white text, plum outline, lower third) next to the clean render.
  - Build the cues: `python scripts/words_to_srt.py voice/words.json <out>/<name>_subtitles` (rewritten 2026-11-17: phrase-based, a cue/line never ends on a weak word like a/the/of/entire, hyphenated words are never split, <= 2 balanced lines of <= 26 chars, no overlapping cues, prints any rule violations).
  - Burn them: `scripts/burn_subtitles.sh final.mp4 subs.srt out_captioned.mp4` (libass; do NOT pass `original_size=`: it drew nothing; Fontsize 13 + MarginV 62 on the default PlayRes = ~87 px text ~410 px above the bottom edge). Test a frame with an OUTPUT-side `-ss` (input-side `-ss` shifts the subtitle clock and shows nothing). Look at one frame before delivering.
- **No channel watermark.** `src/Root.tsx` can wrap compositions in `withWatermark` (the Totoversity avatar + name, `src/Watermark.tsx`); the bridge and molasses shorts still use it, the Great Stink short does not (`Stink = StinkShort`). New shorts: register the bare component, no watermark, unless the user asks for it.
- English only.
- Voice: one steady tone.
- Jokes are researched real facts.
- Standard mix: music +3 dB, SFX -6 dB, voice unchanged.
- Final export 2K vertical: 1440x2560, `--scale 1.3333`.
- A reviewer sub-agent on the strongest available model verifies every check.
- Save after every step.
- "Just do it" once the script is approved.

## Pipeline
1. **Topic and facts.** Pick one surprising true story with a physical cause and effect (it should be visual), plus a simple everyday analogy that explains it.
   - Write the facts with their source at the top of `SCRIPT.md`.
2. **Script** (~3.7 words/s, 55-70 s). Beat formula from the bridge short:
   - **Hook:** the absurd fact in one line ("Seventy-four soldiers knocked down an iron bridge just by walking across it.").
   - **Setting:** year, place, pride.
   - **Action:** escalation over three or four beats, each a little bigger.
   - **Snap:** the moment it breaks.
   - **Deadpan double line:** "Luckily ... / Unluckily ...".
   - **Explanation:** one physics idea through an everyday analogy (the kid on a swing).
   - **Consequence:** the rule it created.
   - **Callback twist:** the ending.
   - Never describe on screen what the viewer already sees.
3. **Voice.** Record or generate `voice.wav`, then make its word timings `words.json` (any speech-to-text with word times).
   - Put them in the project folder, e.g. `/home/lovanto/Documents/totoversity/shorts-audio/bridge/voice/`.
   - Hand-fix the word timings. Everything is timed to words.json.
4. **Shot plan** in `story.ts`: copy `templates/bridge/` (the final bridge source, same as `src/videos/bridge/` of your Remotion project) to `src/videos/<name>/`, register a new composition next to `BridgeShort` in `src/Root.tsx`, and rename it.
   - `SHOTS`: id, a/b frames, light day/golden, crowd mode, `tau` story time.
   - `XFADE`: crossfades at place/time changes.
   - `FLASH_AT`: a white flash after the hook.
   - `CAMS`: per-shot keys `{f, dur?, cut?, s: f => {pos, look, fov, roll}}`.
   - `KICKS`: impact flip-shakes.
   - `DOF`/`dofAt`: lens blur per beat.
   - `FOREGROUND`: near framing props.
   - Every visual reaction lands 0-3 frames before its word.
5. **World.**
   - `lights.ts`: LIGHTS plus the LOOK sky/river/cloud palette per light.
   - `shade.ts`: two-tone shading and `untone()`.
   - `build.ts`: town, houses and Kenney CC0 kit props, recoloured, with sight-line culling of anything blocking a camera.
   - `paint.ts`: HD Canvas2D painted textures with seams painted in as dark tints.
   - `world.ts`: sky shader, fog = horizon colour, river, per-frame posing, sun frozen per shot and camera-relative.
6. **Characters.**
   - `toon.ts`: the Canvas2D `Pen` drawing API, 600x1000 design canvas, soles at y = 975, bean heads, stick limbs, plum variable-width outline, face library.
   - `cast.ts`: camera-facing billboards, crowds, effect cards, blinks, walk cycles. All billboards go on the `NOINK` layer.
   - `cardshade.ts`: cards lit by the scene light, no emissive.
7. **Post** (`Bridge.tsx` + `ink.ts` + `lensblur.ts` + `grade.ts`).
   - Composer order: ink → lens pre → lens main → bloom → NEUTRAL tone map → grade (MSAA 4).
   - Every pixel parameter scales with output height / 1920.
8. **Sound** (`/home/lovanto/Documents/totoversity/shorts-audio/bridge/audio/`: timeline.py, sfx_gen.py, sfx.py, music.py, instruments.py, dsp.py, mix.py).
   - Event table → synthesized SFX plus an original score ducked under the voice.
   - Output: mix.wav (48 kHz, exact length), stems and cues.md.
   - Lock the picture's time constants before the sound is made. Any later timing change means re-running the sound.
9. **Look checks.** Run `node scripts/bridge-stills.mjs out/<name>/x_ 100,400 0.5`.
   - Set `BRIDGE_ENTRY=src/sandboxes/<n>/index.tsx` to render a sandbox copy.
   - Make side-by-sides against reference frames with `python scripts/sbs_sheet.py out.jpg --ours ... --ref ...`.
   - Send them to a reviewer sub-agent (strongest model): 1-3 images, a ≤200-word verdict.
   - **Flicker check (mandatory):** stills can't show flicker. Render short `--sequence` ranges of the push-in shots and run the frame-diff test in "Flicker/glitch checklist" below before the full render.
10. **Final render.**
    - `npx remotion render src/index.ts <Comp> out/<name>/video.mp4 --codec h264 --crf 16 --scale 1.3333`
    - **Linux with Intel + NVIDIA (prime on-demand):** Chrome picks the Intel iGPU unless told otherwise. Prefix the command with `__NV_PRIME_RENDER_OFFLOAD=1 __VK_LAYER_NV_optimus=NVIDIA_only VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/nvidia_icd.json` and add `--gl=vulkan`. `bridge-stills.mjs` does this itself. Verified 2026-11-17: `nvidia-smi` shows `chrome-headless-shell` on the RTX 3060 for both stills and full render.
    - Mux with `-map 0:v:0 -map 1:a:0` (Remotion writes a silent audio track).
    - Mux with `-c:v copy -c:a aac` and WITHOUT `-shortest` (the audio is ~1 ms shorter than the video; `-shortest` cut 3 frames off the Great Stink short). Check `ffprobe -count_frames` = TOTAL.
    - Then burn the subtitles into `<name>_captioned.mp4` (see User rules).
    - QA: `python scripts/short_qa.py final.mp4 out/<name>/qa shots.json` checks every frame for black, white, frozen and pop frames, plus loudness and sheets.
    - Fix anything it finds, then run a deep audit with a reviewer sub-agent.
11. **Deliver.** Tell the user the final mp4 path, update memory, write notes.

## Final look values (bridge after 4 verifier rounds; all in `templates/bridge/`)
Start every new short from `templates/bridge/` (copy to `src/videos/<name>/`): the look lives in these values, the
story lives in story.ts / build.ts layout / cast.ts roles. Reviewer scores at the end: colour day 7, golden 5-6,
lighting 5-6, ink 6, textures 5-6, characters 7, depth 6-7, composition 6-7 (from 5/3/4/5/4/7/4/6 at the start).
- **Light presets** (`lights.ts`, sun camera-relative and frozen per shot):
  - day: az 75 / el 48, lit [1.58,1.5,1.33], shade [.30,.29,.36], lift [.05,.06,.11] (cool tint ONLY in shade), sky
    top #3e7fd2 → horizon #b8d0ec, fog = horizon, 25→300 m, uSat 1.08, ~15 % blue haze past 60 m.
  - golden: az 6 / el 7 (backlit low sun), key toward #FFB36B ×1.5, violet-blue shade (facade ≈ #444380), sky
    #ffc47c → #8a6f8a, peach fog only past 50 m, sun disc #ffcf9e + bloom, contact blobs + real card shadows.
- **Albedos** (`paint.ts`/`build.ts`): muted brick / cream / ochre / terracotta houses with plinth, cornice, sills,
  hoods, door step, chimney + pot, heights 7 / 8.4 / 9.8 m; warm grey/beige stone (saturation −35 % from "storybook");
  ochre wood deck C* ~51-58 with near-black seams; iron dark and desaturated. Never lemon, never lavender lit faces.
- **Ink** (`ink.ts`): #030303, 5.1 px near (6 m) → 3.3 px far (90 m) at 1080x1920, creases ×0.8 from 35°, depth
  jumps from 1 %, fog tint 0.3 only far; character cards on layer `NOINK` (they carry their own plum ink).
- **Lens** (`lensblur.ts` + `dofAt` in story.ts): cInf px at 1080: hook/river CU 15-16, close-ups 12-14, MS 10-12,
  park 7, golden sway 5, wides/aerials 0. Focus on the eyes of the front row.
- **Post** (`Bridge.tsx`): ink → lens pre → lens main → bloom (thr 1.0, int .5, 6 levels, radius .6) → NEUTRAL tone
  map → grade; MSAA 4. Film grain exists but is OFF (reference measures no grain; it quadruples the file size).
- **Characters** (`toon.ts`/`cast.ts`/`cardshade.ts`): bean heads h/w .94, plum ink #241726, eyes .26 W apart, no blush,
  14 expressions; adults 3.5 head-heights; walk bob 5 %, lean 1-7°, planted 0.8 m stride; blinks 0.5-2.3 s; tight
  contact shadow ~.5 under the feet + sun-direction tail by day; golden rim inner only (never an offset outer copy).
- **Camera** (`story.ts`): cuts on big jumps, smootherstep glides 18-40 f, every hold creeps (no static hold ≥4 f),
  flip kicks decaying over 7 f on impacts, 4-4.6° rolls, foreground props (`FOREGROUND`) in ~1/3 of shots.

## Look targets (measured from the reference; see references/reports/)
- **Ink:**
  - World lines: about 3 px at 1080 wide, near-black #0b0a0c, nearly constant with distance. Silhouettes, depth jumps and normal creases only. No line on wall/floor joins or the horizon. Character cards are never outlined by the world ink.
  - Character ink: dark plum #201628-#2f1d28, thicker on the bottom/shadow side.
- **Colour:**
  - Day median luma ~.57. Non-ink p5 ~.23 (no crushed blacks). Lit chroma C* p90 ~55. Day sky top ~#5e93d9, horizon 1.28x brighter.
  - Golden: peach horizon #ffd08a, violet-blue shadows (never brown), backlit sun.
- **Depth:**
  - DOF on about 1/3 of screen time (CU, MS, inserts), cInf 10-16 px at 1080, focus on the eyes. Establishing and wide shots stay sharp.
  - Fog = horizon colour, 25→420 m day, 20→360 m golden.
  - Bloom only on HDR emissives: threshold 1.0.
- **Camera:**
  - Hard cuts on big jumps. Everything else is a smootherstep glide of 18-40 f, peak ≤ 25 px/f at 720p.
  - Every hold pushes in 0.15-0.35 %/f, with 0.6 %/f on punch words.
  - Rolls of 4-5°.
  - No hand-held float. Impact shakes flip sign every frame and decay over 7 f.
- **Characters:**
  - About 3.5 head-heights tall, legs 1.4 HH.
  - Stick limbs about 0.055 of head width, ink-dot hands.
  - Bean head (h/w ~0.93, narrower chin, pointier crown).
  - No blush or eye highlights. Faces at brightness ~.93.
  - Walk bob 3-7 %, lean 1-7°, planted feet.
  - Blinks every 0.5-2.3 s, lasting 4 f.

## Look-match loop (how the bridge look was reached; reuse for any "make it look like X" pass)
1. **Measure the reference first.** One analysis agent per topic (motion, depth, textures, characters, lighting, outlines, grade), each writing numbers, not adjectives, to `references/reports/<topic>.md`. Shared brief: `compare/CONTEXT.md`. Reports are the source of truth for every agent after.
2. **Sandboxes, one owner per file.** Copy the project folder to `src/videos/<name>_{cam,world,mat,char,post}` with entries `src/sandboxes/<n>/index.tsx` (same `index.tsx` as main, only the import path changed). Ownership used for the bridge:
   - cam: story.ts (camera keys, cuts, kicks, DOF table, foreground props)
   - world: world.ts, lights.ts, shade.ts, grade.ts (sun, sky, fog, river, colour, grade)
   - mat: paint.ts, build.ts (painted textures, buildings, props)
   - char: toon.ts, cast.ts, cardshade.ts (character drawing, posing, card lighting, fx cards)
   - post: ink.ts, Bridge.tsx, lensblur.ts (outline pass, composer, lens blur, bloom)
   Agents only edit their own files in their own sandbox and render stills with `BRIDGE_ENTRY=src/sandboxes/<n>/index.tsx node scripts/bridge-stills.mjs out/<name>/<n>/x_ <frames> 0.5`.
3. **Merge** with `python scripts/bridge_merge.py [cam,world,mat,char,post]` (backs main up to `backup/bridge_<time>/`, copies owned files only). Then `npx tsc --noEmit` (filter to the project folder), then **re-sync every sandbox from main** (`cp -f src/videos/<name>/* src/videos/<name>_<n>/`) before the next round.
4. **Verify** with a fresh reviewer sub-agent (strongest model): side-by-side sheets (`python scripts/sbs_sheet.py out.jpg --ours a b --ref r1 r2`), score each area out of 10 (colour day / golden, lighting, ink, textures, characters, depth, composition) plus a numbered fix list with frame numbers. Map each fix to the file owner and resume that owner's agent with SendMessage (keeps its context). Bridge scores: round 1 5/3/4/5/4/7/4/6 → round 2 5/4/5/6/4/7/6/6 → round 3 see notes.
5. Contracts between owners live in exported constants (e.g. `NOINK` layer from ink.ts, `dofAt`/`FOREGROUND` from story.ts, `LIGHTS`/`LOOK` from lights.ts). Changing a contract means telling every owner that reads it.

## Channel branding (optional)
Only when the user asks for it: the Totoversity mark (avatar + name, top-left, inside the Shorts safe area). Copy `templates/branding/Watermark.tsx` to `src/`, `profile.png` to `public/totoversity/`, and wrap the composition in `Root.tsx` with `withWatermark(...)`. Default for new shorts is NO watermark (see User rules). Check it in a still before rendering.

## Gotchas
- Kenney nature-kit materials are teal: recolour them by material name in build.ts.
- Cameras end up inside houses: the sight-line culler in build.ts/world.ts removes anything blocking any camera ray.
- Ink in the same merged effect pass as DOF gets overwritten. Ink must be its own pass before the blur.
- Pixel-sized post parameters must scale with resolution: stills are at 0.5, the final at 1.333. R3F clamps dpr to ≥ 1, so `--scale 0.5` stills still render a 1080x1920 buffer.
- **Disk:** every Remotion bundle copies `public/` into the temp folder (`remotion-webpack-bundle-*`) and never deletes it. On this machine `/` is nearly full: always `export REMOTION_TMP=/mnt/datalinux/remotion-tmp TMPDIR=/mnt/datalinux/remotion-tmp` before rendering (`bridge-stills.mjs` sets TEMP/TMP/TMPDIR from REMOTION_TMP itself). Keep `public/` lean (only the 26 Kenney `.glb` files). When a project is finished and nothing is rendering, ask the user, then delete its old `remotion-webpack-bundle-*` and `puppeteer_dev_chrome_profile-*` folders there.
- Use forward slashes in JS path strings (`"/mnt/datalinux/remotion-tmp"`).
- Remotion writes a silent audio track: mux with `-map 0:v:0 -map 1:a:0`.
- Sub-agents can't write report files in this harness: ask them for a ≤150-word final message and save it yourself to `out/<name>/<n>/REPORT.md`.
- Scratch `.ts` files inside `out/` break `tsc`: name them `.txt`.
- Render speed varies a lot with scene weight: the bridge did ~4 fps at 2K (≈10 min), the molasses short (dynamic height-field flood + tank wall, 4096 shadow map) ran ~0.8 fps at 2K (est. 2 h 20 min) and ~3.5 fps at 1080x1920 (~1 h). **Render 1080x1920 first** (`--scale 1`, CRF 18), review, and only then spend the 2K render. Stills at 0.5 take 2-8 s each after a ~40 s bundle.
- Start long renders with `setsid nohup ... < /dev/null & disown` (the harness' background-task notice only means the launcher shell exited, not that the render finished). Never `pkill -f "remotion render ..."` from the same command line: the pattern matches your own shell and kills it (exit 144). Check progress with `tail -c 100 out/<name>/render*.log`.
- `remotion render --sequence` needs an output dir WITHOUT an extension; `--frames=a-b` renders a range, handy for A/B-testing a glitch.
- Film grain at 2.5 % made the 2K file 910 MB instead of ~250 MB and will turn to mush on YouTube; the reference has none. Keep it off.

## Readability traps the verifier caught (check every new prop/shot for these)
- **A swing drawn as one rope that disappears behind the kid reads as a HANGING.** Always two ropes to a wide plank
  with the kid between them (`swingKid` in toon.ts), and a frame whose legs clear the arc (A-frame at each end).
- Props or flotsam closer than ~2 m to a lens become huge cut-off blobs at the frame edge. When a camera moves, re-check
  every prop near its new position (the river cameras moved into the floating hats).
- A foreground bush cut by the frame edge reads as a "green ball"; a foreground prop must be recognisable or gone.
- Flags: red + yellow star/diamond reads as Vietnam's. Use a period-correct flag (St George's cross for England 1831).
- Painted signs lit by a side sun go grey-blue and unreadable: give the sign face an unlit material.
- Golden rim light done as an offset outer copy turns every hat into a picture frame: inner rim only, head/torso only.
- Balcony/railing rails at chest height through characters: put the lens ~2.5 m up so rails cross legs, not torsos.
- Flat holds read as freezes in QA (frozen span ≥12 f): every hold needs a creeping push-in.

## Lessons from the molasses short (2026-11-16, "The Tank That Was Painted Brown")
Second short made with this skill (Boston Molasses Flood 1919, 69 s, 20 shots, 38 voice cues). What was new and what bit us.

### Workflow that worked (one phase at a time, report each, no commits)
A world (`north.ts`: streets, tenements, the hero object, set pieces, interior sets at x=400) -> B the physical effect (`molasses.ts`: dynamic geometry
+ height-field flood, pure function of `(shot id, frame)`) -> C cast + props (`cast.ts`, `props.ts`) -> D cameras/DOF/kicks (`story.ts`) -> E sound
(`audio/mix.py`) -> 1080p render -> mux -> `short_qa.py` -> reviewer sub-agent -> 2K only after approval. Look-check stills after every phase
(`COMP=<Comp> node scripts/bridge-stills.mjs out/<name>/<phase>/x_ <frames> 0.5`; the script honours `COMP`), contact sheets with PIL.
- The ready-made template lives in the SKILL dir (`templates/bridge/`), not the Remotion project. For a new story do NOT edit the copy in place: keep
  `story/world/cast` as `*.bridge.txt` references, rewrite them, and keep reusing `build.ts` (Batch, house, prop), `paint.ts`, `shade.ts`, `ink.ts`,
  `lensblur.ts`, `grade.ts`, `lights.ts`, `toon.ts`, `cardshade.ts`, `Bridge.tsx` (rename export + frames const) unchanged.
- New `world.ts` = sky/light rig + `shotSun` + the light/DOF part of `update()` copied from the bridge's, scene content swapped for a `buildX(root, kit)`.
  New `cast.ts` = canvas Pool/Actor/Fx/`person()`/`blob()` copied from the bridge's, `stage(id, f, cam)` rewritten. Hand props are separate unlit
  Fx cards (props.ts, Pen drawings) placed near the hands: cheap, but they float; attach them in toon.ts if a shot needs a held prop.
- Per-shot sun override `SUN_SHOT[id] = {az, el}` (az 140 = sun behind the camera): without it big faces (a tank wall, interior walls) land in the purple
  shade colour. The `golden` preset turns small interiors orange and teal-shifts paper: use `day` for interiors.
- Dynamic geometry (tank wall that bulges/splits, flood height field with analytic normals, tipping vehicle) must be a pure function of the frame so
  stills, ranges and the full render all agree. Dry height-field cells drop to y=-0.5 (leaves a skirt; use a finer grid for close shots).
- Make the physics reach the story beat: place hero objects by distance from the source (`R(tau)`), not where they look nice, or the flood never hits
  the thing it is supposed to knock over.

### Voice + timings on this machine (Kokoro + faster-whisper)
- Kokoro (`kokoro>=0.9.4`) needs **Python < 3.13**: `/usr/bin/python3.12 -m venv /mnt/datalinux/venv-voice312`, CPU torch from the cpu wheel index,
  `pip install kokoro soundfile faster-whisper scipy`; set `HF_HOME=/mnt/datalinux/hf-cache`, `PIP_CACHE_DIR`, `TMPDIR` on `/mnt/datalinux` (`/` was 97 % full).
- Voice `am_michael`, one line at a time, silence trimmed at both ends of each line + 0.32 s gap, resample to 48 kHz PCM_16 mono. Speed 1.0 gave 90 s for
  205 words (too long); **speed 1.2 -> 69 s**. Budget ~3.0-3.3 words/s with Kokoro, not 3.7. Count words from the script itself, not the whole file.
- faster-whisper with the installed PyAV fails on file paths (`metadata_errors`): load with soundfile, resample to 16 kHz, pass the numpy array.
  Whisper writes numbers as digits ("35", "1919", "2 .3", "119"): **hand-fix `words.json`** to the spoken words, splitting the span by letter count,
  and assert starts/ends are monotonic.
- Compute shot edges from `words.json` (first word start of each sentence, in frames) before designing shots; a shot plan table (frame, VO, framing, DOF)
  lives in `SHOTPLAN.md`.

### Sound (`audio/mix.py`, numpy/scipy only)
- Event table in frames (`E(frame, name, signal, gain)`), synthesized primitives (thump, clang, creak, roar, squelch, plink, swish, gurgle, hiss, murmur,
  chime, knock, scratch), ~64 cues; original 112 bpm score (pluck/bass/timpani/pad) with section changes at story beats; `cues.md` written from the table.
- Sum of different-length arrays: wrap primitives in an `np.ndarray` subclass whose `+` zero-pads (or use a `seq()` placer); plain `np.pad` on the front breaks.
- Levels: music = RMS 17 dB under speech +3 dB, ducked ~8 dB under words (word envelope from `words.json`, 0.12 s smoothing); SFX peak = voice peak -6 dB,
  ducked ~3 dB under words. Result -22.6 LUFS, peak -0.9 dBFS, exact voice length. Mux with `-map 0:v:0 -map 1:a:0` and open the **muxed** file:
  the raw Remotion `video_*.mp4` carries a silent track (the user once judged the raw file "no sound").

### GLITCH TO AVOID: per-frame card re-keying (single-frame sprite drop-outs)
Symptom: in the full render a character card disappears for ONE frame and a grey-white bar shows in its place, repeating every 7-9 frames
(QA "pops" in pairs, e.g. f434/435, 441/442, 450/451, 458/459). Cause: `person()` picked the canvas resolution tier from the per-frame camera distance and
quantised the light side from the per-frame camera right vector; during a slow push-in both flip back and forth, so the pooled canvas keys churn.
Fix (in the molasses `cast.ts`, flag `STABLE_CARDS = true`): derive tier and light from the active **camera key**: `keyRange(id, f)` in `story.ts` gives the
key's frame span; tier uses the minimum distance over camera samples across that span, light uses the camera right at the key start. Reproduce/verify with
`remotion render --sequence --frames=a-b --scale 0.5` and consecutive-frame mean-abs-diff (a bad frame spikes to ~2x the local baseline); single stills do NOT
show it (fresh pool each still), so always check a sequence. Run `short_qa.py` after every full render and look at the non-cut pops.
**Ported (2026-11-17):** `templates/bridge/cast.ts` (`STABLE_CARDS = true`, `REF`, set in `stage()`) and `templates/bridge/story.ts` (`keyRange`) now
carry the fix, so every new short starts glitch-free. Never set `STABLE_CARDS = false`. Any new billboard/fx that picks a canvas size, light step, mirror or
texture key from the per-frame camera must use `REF` (camera-key reference) the same way. Keys must also be stable across frames for the same state:
no `Math.random()`, no unquantised floats in a pool key (use `q()`/`fkey`).

### Flicker/glitch checklist (run BEFORE the full render, and again on the final)
1. `remotion render --sequence --frames=a-b --scale 0.5` over every slow push-in / glide shot (~40-60 f each), then consecutive-frame mean-abs-diff:
   a bad frame spikes to ~2x local baseline. Stills cannot show this.
2. After the full render: `short_qa.py`; every "pop" that is not on a shot cut / flash / kick is a bug. Pops in pairs (f, f+1) = one dropped frame.
3. Causes seen / to rule out, in order: (a) card pool re-keying (above); (b) two coplanar surfaces z-fighting (contact blob vs ground, painted decals,
   road vs kerb): give the upper one `polygonOffset` (-2,-2) or lift it 2-5 cm and keep `depthWrite:false`; (c) shadow-map shimmer: freeze the sun per shot,
   snap the shadow camera to texel steps, keep `shadow.bias`/`normalBias` fixed; (d) thin ink lines shimmering on far geometry: ink width scales with
   distance but is never < ~2 px, MSAA 4 stays on; (e) per-frame random (grain, jitter, `Math.random`, `Date.now`) anywhere in `useFrame`/`update()`:
   everything must be a pure function of `(shot id, frame)` so ranges, stills and the full render agree; (f) billboards at < 2 m from the lens or
   alphaTest edges at tiny tiers: keep tier by minimum key distance, never below the 480x800 tier for anything in a close-up.
   Detector: `/usr/bin/python3 templates/scripts/flicker_check.py out/<name>/seq_a-b ...` (numpy+PIL; the voice venvs lack them; natural-sorts `element-N.jpeg`).
   It flags a frame that differs from BOTH neighbours while the neighbours match each other. Expected hits: the kick-shake frames (`KICKS`/`HITS` times). Anything else = look at the frame.
   Seen once (bridge f1801, officer card replaced by a cream rectangle for 1 frame) in a long range render right after a timed-out render, and NOT reproducible in 3 re-renders: re-render the suspect range before debugging, and kill stale chrome/remotion processes first. Use `--timeout=120000` for ranges with 1800x3000 cards.
4. If a glitch survives, re-render only the bad range (`--frames=a-b`) with one suspect switched off at a time to bisect, instead of full renders.

### Hooks / environment gotchas seen
- GateGuard asks for facts before the first Bash, before destructive-looking commands (even a heredoc that merely contains the words), and before
  Write/Edit of new or skill files: state them in the reply, then retry; delete scratch dirs rarely, use fresh dir names instead.
- A finished short is not "done" without the reviewer sub-agent (strongest model) pass and a listening check; say plainly when these were skipped.


## Lessons from the Great Stink short (2026-11-17, "The Curtains That Did Not Work", 69 s, 21 shots)
Third short. What was new and what bit us (full state in memory `stink-short`, plan in `shorts-audio/stink/SHOTPLAN.md`).
- **Workflow that worked (one phase at a time, report each, no commits):** 1 facts + script -> 2 fact-check + voice (Kokoro `am_michael` 1.2x gave 3.2 words/s, 219 words = 68.8 s; a `gen_voice.py` that maps script words onto Whisper timings per line and hand-fixes zero-length words) -> 3 shot plan + `story.ts` -> 4 world (`thames.ts`, `world.ts`, set origins far apart in x/z) -> 5a effects (`fx.ts`, `cloth.ts`) -> 5b cast + props (`props.ts`, staging in `cast.ts shot()`) -> 6 camera polish + flicker check -> 7 sound (`audio/mix.py` built from the molasses one) -> 8 render, mux, QA, subtitles.
- **Portrait framing is narrow:** at 10 m a 40 deg vertical fov sees only ~4.5 m of width. Check every set's subjects against the real frame (a contact sheet of stills per shot) before polishing; most "missing character" bugs were subjects outside the frame.
- **Ground plane vs holes:** a big ground plane hides anything built below y = 0 (river, trench, pool). Cut holes in the ground (split into rectangles around them) and give the hole a bed.
- **Sets that must not shadow the sun** (tunnel vault) go in a second `Batch` built with `cast = false`.
- **Cloth:** curtains are subdivided planes whose vertices are a pure function of the frame (unroll, billow, slide off + flop), `computeVertexNormals()` each frame, two-tone Lambert double-sided.
- **Effect cards:** soft see-through clouds with a union outline (stroke ink, `destination-out` fill, then translucent fill). Never put a camera-dependent value in a pool key; quantise any time-driven key (`foam|${q}`); drop clouds nearer the lens than their size + 2 m (`CAMP` in fx.ts) so the camera never sits inside one.
- **Flicker found by `flicker_check.py` over a FULL half-res sequence (do this before the real render, ~11 min):**
  1. Shadow-map shimmer in a golden shot: the shadow camera followed the creeping push-in. Fix (world.ts): shadow focus and box size come from the first frame of the camera key (`keyRange`), constant for the whole key.
  2. Texture corruption in ONE of the 4 render tabs after a long run (white strip under feet, a character missing, a brown block where a facade texture should be; period-4 flicker in frame diffs, ~19 mean diff). Range renders were clean, only long full renders showed it. Cause: the card pool kept 90 flushes of 1800x3000 character canvases (dozens of ~29 MB textures per tab, software GL on CPU/RAM). Fix that made the full 1080p render clean: `Pool.KEEP = 10`, top tier 1440x2400, blob/contact shadow cards drawn once into permanent canvases (`staticReq` in cast.ts, used by world.ts for keys starting `blob|`), no `ctx.filter` blur in card drawings. ALWAYS run `flicker_check.py` on the whole final (extract frames: `ffmpeg -i final.mp4 -vf scale=540:960 -vsync 0 -start_number 0 d/element-%04d.jpeg`), not just on short ranges.
  3. One non-reproducible 1-frame person-card dropout (f1252) under `--concurrency=4`; two re-renders were clean.
- **QA "POPS" on the final:** expected on kick frames; anything else, look at the frame (extract with `ffmpeg -vf select=eq(n\,F)`).
- **Hooks seen:** GateGuard demands facts before the first Bash, before every NEW file Write (state them, then retry; the retry passes) and before any `rm -rf` or command that edits several files (use fresh output dir names instead of deleting).
- **Long renders die with the session:** `setsid nohup` did NOT survive a session end here; start them with `systemd-run --user --unit=<name> --working-directory=<project> --setenv=REMOTION_TMP=... --setenv=PATH="$PATH" /bin/bash -c '<render cmd> > log 2>&1'` and poll the log in bounded `for` loops (a bare `sleep N` is blocked). 1080p full render ~35-45 min.
