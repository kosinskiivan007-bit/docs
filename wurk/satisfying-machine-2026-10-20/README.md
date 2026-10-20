# The Orbital Machine (2026-10-20)

Entry for the WURK contest "Build the Most Satisfying Machine".

- Format: 20 s seamless loop, 1920x1080, 24 fps, MP4 (H.264), no audio.
- Mechanism: three meshing gears (26/16/11 teeth) whose rotations are locked by tooth ratio; three golden balls rolling on an outer ring with short trails; a synchronized pendulum; a piston pumping twice per cycle.
- Seamless by construction: every motion completes an integer number of cycles per 20 s, so the end state equals the start state.
- Tools: rendered programmatically in Python (Pillow, 2x supersampling), encoded with FFmpeg (libx264). No video-generation model for the motion.
- Source: `make-machine.py`.
