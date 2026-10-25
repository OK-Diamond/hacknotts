"""Menu, calibration, gameplay, and game-over scenes."""
import math
import pygame

BACKGROUND_PATH = "./assets/images/background_day.png"
SCROLL_SPEED = 5  # pixels per frame

_background = None
_scroll = 0
_game_over_image = None


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
    global _game_over_image

    if _game_over_image is None:
        _game_over_image = pygame.image.load(
            "./assets/images/gameover.png"
        ).convert_alpha()

    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

    restart = body_font.render("Press space to restart", True, (255, 255, 255))
    screen.blit(
        _game_over_image,
        _game_over_image.get_rect(center=(screen.get_width() // 2, 200)),
    )
    screen.blit(restart, restart.get_rect(center=(screen.get_width() // 2, 270)))
