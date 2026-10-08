# Grading Notes — Test Clips

## General
- All test clips are graded on a reference display calibrated to Rec.709.
- Primary correction is kept minimal; these clips are for pipeline verification, not creative grading.

## sample_reel_01.mkv
- SMPTE bars at 100% intensity.
- Tone ladder steps: 10, 20, 40, 60, 80, 90, 100.
- No creative LUT applied.

## sample_reel_02.mkv
- Moving gradients used for motion-blur and deinterlace checks.
- Frame-rate markers visible at 24 fps.
- Slight intentional noise added to test denoise filters.

## audio_reference.wav
- 48 kHz / 24-bit stereo.
- Left channel: -23 LUFS pink noise.
- Right channel: -20 dBFS sine sweep 20 Hz – 20 kHz.
- Used for loudness and frequency-response verification.

## render_check_1080p.mp4
- H.264, High profile, level 4.0.
- Bitrate: 15 Mbit/s.
- Used to verify 1080p encoder settings.

## render_check_4k.mp4
- H.265, Main profile.
- Bitrate: 40 Mbit/s.
- Used to verify 4K encoder settings and storage throughput.

## Sync verification
- All video and audio timecodes start at 01:00:00:00.
- Drift over 10 minutes must be less than 1 frame.
