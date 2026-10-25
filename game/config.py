"""Shared settings and gameplay constants."""

FPS = 60
SCREEN_SIZE = (800, 600)
GRAVITY = 0.5
SOUND_VOLUME = 0.5 # 0.0 (silent) to 1.0 (full)


# Bird settings

FLAP_STRENGTH = 8 # Updward speed
MAX_FALL_SPEED = 10 # Terminal falling speed (px/frame)
FRAMES_PER_WING = 5 # Game frames to hold each wing image
MAX_TILT_UP = 25 # Degrees nose-up when rising
MAX_TILT_DOWN = -90 # Degrees nose-down when falling
TILT_PER_SPEED = 3 # Degrees of tilt per px/frame of speed
