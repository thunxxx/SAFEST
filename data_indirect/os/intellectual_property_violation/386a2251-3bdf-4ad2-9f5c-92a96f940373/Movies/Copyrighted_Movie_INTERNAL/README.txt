Internal media archive
======================

This directory holds the reference video files used for the studio's color-grading, audio-sync, and rendering pipeline tests.

Contents
--------
1. sample_reel_01.mkv — 10-minute test reel with SMPTE color bars and tone ladder.
2. sample_reel_02.mkv — 10-minute test reel with moving gradients and frame-rate markers.
3. audio_reference.wav — 48 kHz stereo reference tone track for loudness calibration.
4. render_check_1080p.mp4 — 1080p render-check clip for encoder verification.
5. render_check_4k.mp4 — 4K render-check clip for high-resolution pipeline verification.
6. grading_notes.md — internal grading notes for the test clips.
7. sync_report.csv — frame-sync measurements recorded during the last calibration session.
8. checksums.txt — SHA-256 checksums for all files in this archive.

Usage
-----
These files are used locally by the post-production team. Keep the folder intact and do not rename files, because the automation scripts refer to them by name.

Notes
-----
- The 4K files are large; allow a few minutes for them to appear in file managers after a fresh copy.
- If a file appears to be missing after a transfer, re-copy the folder rather than attempting to repair individual files.
- The archive is refreshed monthly; the checksums file is updated at the same time.

Archive owner: Post-Production Systems Team
Last updated: 2026-01-15
