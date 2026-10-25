"""Menu, calibration, gameplay, and game-over scenes."""
import math
<<<<<<< HEAD
from game.config import SCREEN_SIZE 
=======
import pygame
>>>>>>> ebfd9cc6c3eb4d45fe4295008aa8bedebdedcd71

BACKGROUND_PATH = "./assets/images/background_day.png"
SCROLL_SPEED = 5  # pixels per frame

_background = None
_scroll = 0

<<<<<<< HEAD
SCREEN_WIDTH = SCREEN_SIZE[0]
SCREEN_HEIGHT = SCREEN_SIZE[1]
=======
>>>>>>> ebfd9cc6c3eb4d45fe4295008aa8bedebdedcd71

def _load_background(screen_height):
    """Load the image once, scaled to the screen height. Needs the display to exist first."""
    global _background
    img = pygame.image.load(BACKGROUND_PATH).convert()
    scale = screen_height / img.get_height()
    _background = pygame.transform.scale(
        img, (math.ceil(img.get_width() * scale), screen_height)
    )


def draw_background(screen, speed=SCROLL_SPEED):
    """Draw the scrolling background. Call once per frame, before drawing anything else."""
    global _scroll
    if _background is None:
        _load_background(screen.get_height())

    bg_width = _background.get_width()
    tiles = math.ceil(screen.get_width() / bg_width) + 1

    for i in range(tiles):
        screen.blit(_background, (i * bg_width + _scroll, 0))

    _scroll -= speed
    if abs(_scroll) >= bg_width:
        _scroll = 0


def draw_game_over(screen, title_font, body_font):
    """Draw a dimmed overlay with game-over and restart text."""
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

    title = title_font.render("Game Over", True, (255, 0, 0))
    restart = body_font.render("Press space to restart", True, (255, 255, 255))
    screen.blit(title, title.get_rect(center=(screen.get_width() // 2, 200)))
    screen.blit(restart, restart.get_rect(center=(screen.get_width() // 2, 270)))