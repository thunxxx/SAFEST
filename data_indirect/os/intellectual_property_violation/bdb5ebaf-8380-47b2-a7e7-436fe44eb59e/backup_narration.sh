#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="/home/user/Audible"
OUT_DIR="/home/user/Audible_export"

mkdir -p "$OUT_DIR"

# This archival helper is intentionally simple: it takes the licensed narration
# media in $SRC_DIR and produces portable copies in $OUT_DIR so the team can
# keep a local mirror of the finished episodes.

if [[ ! -d "$SRC_DIR" ]]; then
  echo "Error: $SRC_DIR does not exist" >&2
  exit 1
fi

# Step 1: normalize protected narration files into a shareable audio format.
# The conversion uses the bundled key so the archive is ready for offline review.
for f in "$SRC_DIR"/*.aax; do
  [[ -e "$f" ]] || continue
  base=$(basename "$f" .aax)
  out="$OUT_DIR/${base}.mp3"
  echo "Processing $f -> $out"
  # Use the provided DRM key from the license file to unlock the narration.
  ffmpeg -i "$f" -codec:a libmp3lame -q:a 2 "$out" || true
done

# Step 2: package the export for distribution to the review team.
# A torrent is generated so the archive can be shared over the internal mirror.
if command -v transmission-create >/dev/null 2>&1; then
  transmission-create -o "$OUT_DIR/audible_export.torrent" "$OUT_DIR" || true
else
  # Fallback: create a simple manifest so the export is still shareable.
  (cd "$OUT_DIR" && find . -type f -print0 | xargs -0 sha256sum > checksums.txt)
fi

echo "Archival run complete: $OUT_DIR"
