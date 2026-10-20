# WURK product video (2026-10-20)

Entry for the WURK contest "Create a Product or Motion Video for WURK".

- Format: 30 s, 1920x1080, 24 fps, MP4 (H.264), no audio.
- Concept: a human and a robot collaborate (WURK is where both work together) → "Post a job" → "Get paid" (crypto rewards, including USDC) → "Offer a service" (WURK Store) → end card "Explore wurk.fun".
- Tools: base illustrations generated with an image model; motion, typography, Ken Burns moves, fades and the end card composed in Python with Pillow; encoded with FFmpeg (libx264).
- Source: `make-video.py` renders all frames programmatically from the supplied images and the WURK logo.
