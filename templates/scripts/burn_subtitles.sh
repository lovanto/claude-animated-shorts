#!/usr/bin/env bash
# Burn the sidecar SRT into a vertical short: big bold white text with a plum outline in the lower third.
# Usage: scripts/burn_subtitles.sh <final.mp4> <subs.srt> <out_captioned.mp4>
# Notes: do NOT pass original_size= (it made libass draw nothing); the default PlayRes (384x288) scales Fontsize 13 to ~87 px at 1080x1920,
# MarginV 62 puts the baseline ~410 px above the bottom edge (above the Shorts UI). Output-side -ss is needed to test a frame.
set -euo pipefail
in="$1"; srt="$2"; out="$3"
tmp=$(mktemp --suffix=.srt); cp "$srt" "$tmp"
ffmpeg -hide_banner -loglevel error -y -i "$in" \
  -vf "subtitles=${tmp}:force_style='FontName=Noto Sans,Bold=1,Fontsize=13,PrimaryColour=&H00FFFFFF,OutlineColour=&H00241726,BorderStyle=1,Outline=2.2,Shadow=0,Alignment=2,MarginV=62'" \
  -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a copy "$out"
rm -f "$tmp"
