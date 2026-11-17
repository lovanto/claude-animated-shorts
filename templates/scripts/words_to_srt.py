"""words.json (s/e seconds per word) -> .srt and .vtt subtitle cues for a vertical short.
Usage: python scripts/words_to_srt.py <words.json> <out_basename>   (writes <out>.srt and <out>.vtt)
Rules: a cue is one phrase (breaks at . ? ! : ; and commas); phrases of < 3 words merge into the next one; a phrase longer than
2 lines x 26 chars splits near its middle; a cue or a line NEVER ends on a weak word (a, the, of, to, and, his ...) and hyphenated
words ("fifty-eight") are never split; each cue wraps to <= 2 balanced lines of <= 26 chars. Cue starts at the first word,
ends 0.2 s after the last word (never into the next cue)."""
import json, sys
WEAK = {"a", "an", "the", "of", "at", "to", "in", "on", "off", "and", "or", "but", "for", "with", "from", "as", "by", "his", "her", "their", "its", "our", "your", "my", "is", "was", "that", "it", "this", "than", "into", "over", "up", "entire", "whole", "every", "any", "some", "no", "this", "these", "those", "another", "great", "brand", "new", "same", "hottest"}
PREF = {"out", "into", "from", "and", "then", "but", "with", "while", "that", "who", "over", "in", "on", "after", "when", "because", "then", "as"}
MAXL, MAXC = 26, 48
words = json.load(open(sys.argv[1])); out = sys.argv[2]
weak = lambda t: t.lower().strip(",.?!:;\"'") in WEAK
txt = lambda ws: " ".join(w["w"] for w in ws)
# 1. phrases
phr, cur = [], []
for w in words:
    cur.append(w)
    if w["w"][-1] in ".?!:;,": phr.append(cur); cur = []
if cur: phr.append(cur)
def fits(ws):
    if len(txt(ws)) <= MAXL: return True
    return any(len(txt(ws[:k])) <= MAXL and len(txt(ws[k:])) <= MAXL and not weak(ws[k - 1]["w"]) for k in range(1, len(ws)))
# 2. merge tiny phrases into the next one
i = 0
while i < len(phr) - 1:
    if len(phr[i]) < 3 and fits(phr[i] + phr[i + 1]) and phr[i][-1]["w"][-1] not in ".?!": phr[i + 1] = phr[i] + phr[i + 1]; del phr[i]
    else: i += 1
# 3. split long phrases near the middle, never after a weak word
def split(ws):
    if fits(ws): return [ws]
    best, bs = None, 1e9
    for k in range(1, len(ws)):
        a, b = txt(ws[:k]), txt(ws[k:])
        if weak(ws[k - 1]["w"]): continue
        sc = abs(len(a) - len(b)) + (100 if max(len(a), len(b)) > MAXC else 0) - (8 if ws[k]["w"].lower() in PREF else 0)
        if sc < bs: best, bs = k, sc
    if best is None: best = len(ws) // 2
    return split(ws[:best]) + split(ws[best:])
cues = [c for p in phr for c in split(p)]
# 4. line wrapping: one line if it fits, else the most balanced split that does not end the first line on a weak word
def wrap(ws):
    t = txt(ws)
    if len(t) <= MAXL: return t
    best, bs = None, 1e9
    for k in range(1, len(ws)):
        a, b = txt(ws[:k]), txt(ws[k:])
        if len(a) > MAXL or len(b) > MAXL or weak(ws[k - 1]["w"]): continue
        sc = abs(len(a) - len(b)) - (6 if ws[k]["w"].lower() in PREF else 0)
        if sc < bs: best, bs = k, sc
    if best is None:
        for k in range(1, len(ws)):
            a, b = txt(ws[:k]), txt(ws[k:])
            if len(a) <= MAXL and len(b) <= MAXL: best = k; break
    return txt(ws[:best]) + "\n" + txt(ws[best:]) if best else t
def ts(t, sep):
    h, r = divmod(t, 3600); m, s = divmod(r, 60); return f"{int(h):02d}:{int(m):02d}:{int(s):02d}{sep}{int(round((s % 1) * 1000)):03d}"
rows = []
for k, c in enumerate(cues):
    a = c[0]["s"]; nxt = cues[k + 1][0]["s"] if k + 1 < len(cues) else c[-1]["e"] + 1
    b = min(max(a + 0.5, c[-1]["e"] + 0.2), nxt - 0.02)
    rows.append((a, b, wrap(c)))
open(out + ".srt", "w").write("\n".join(f"{i + 1}\n{ts(a, ',')} --> {ts(b, ',')}\n{t}\n" for i, (a, b, t) in enumerate(rows)))
open(out + ".vtt", "w").write("WEBVTT\n\n" + "\n".join(f"{ts(a, '.')} --> {ts(b, '.')}\n{t}\n" for a, b, t in rows))
bad = [t for _, _, t in rows if any(len(l) > MAXL for l in t.split("\n")) or (t[-1] not in ".?!" and t.split()[-1].lower().strip(",:;") in WEAK) or any(l.split()[-1].lower() in WEAK for l in t.split("\n")[:-1])]
print(len(rows), "cues;", "weak/overlong line endings:", bad)
