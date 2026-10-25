"""Bird position, movement, and collision behavior."""
from collections.abc import Iterable
from enum import Enum, IntEnum
from functools import cache

import pygame
from pygame import Surface, Rect
from pygame.mixer import Sound
from pygame.transform import rotate

from game.assets import ImageAsset as Img
from game.config import GRAVITY, SCREEN_SIZE, FLAP_STRENGTH, MAX_FALL_SPEED, FRAMES_PER_WING, MAX_TILT_UP, MAX_TILT_DOWN, TILT_PER_SPEED, SOUND_VOLUME

@cache
def load_sounds() -> dict[str, Sound]:
    """Load the bird's sounds

    Returns an empty dict if there's no audio device
    """
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        sounds = {name: Sound(f'./assets/sounds/{name}.ogg') for name in ('wing', 'hit', 'die')}
    except pygame.error:
        return {}
    for sound in sounds.values():
        sound.set_volume(SOUND_VOLUME)
    return sounds


class BirdColour(Enum):
    """Enum for bird colours"""
    RED = 0
    YELLOW = 1
    BLUE = 2


class BirdWing(IntEnum):
    "Bird wing positions"
    UP = 0
    MID = 1
    DOWN = 2


# Order the wings cycle through when flapping
WING_CYCLE = (BirdWing.UP, BirdWing.MID, BirdWing.DOWN, BirdWing.MID)


class Bird:
    """Bird object"""
    def __init__(self, colour: BirdColour, x: float = 100, y: float = 100) -> None:
        name = colour.name.lower()
        self.frames = [
            Img(f'./assets/images/{name}bird-upflap.png'),
            Img(f'./assets/images/{name}bird-midflap.png'),
            Img(f'./assets/images/{name}bird-downflap.png')
        ]
        self.x = x
        self.y = y
        self.velocity = 0.0 # px/frame, positive is downwards
        self.angle = 0.0 # degrees, positive is nose-up
        self.tick = 0 # frames since creation, drives the wing animation
        self.sounds = load_sounds()
        self.crashed = False

    def play_sound(self, name: str) -> pygame.mixer.Channel | None:
        """Play one of the bird's sounds (does nothing if audio isn't available)"""
        sound = self.sounds.get(name)
        return sound.play() if sound else None

    @property
    def wing(self) -> BirdWing:
        """Current wing position"""
        return WING_CYCLE[(self.tick // FRAMES_PER_WING) % len(WING_CYCLE)]

    @property
    def rect(self) -> Rect:
        """Hitbox"""
        width, height = self.frames[BirdWing.MID].img.get_size()
        return Rect(round(self.x), round(self.y), width, height)

    def flap(self) -> None:
        """Give the bird upwards velocity"""
        self.velocity = -FLAP_STRENGTH
        self.play_sound('wing')

    def crash(self) -> None:
        """Play the hit sound followed by the die sound. Only plays once per bird."""
        if self.crashed:
            return
        self.crashed = True
        channel = self.play_sound('hit')
        if channel and 'die' in self.sounds:
            channel.queue(self.sounds['die'])

    def update(self) -> None:
        """Update position & increase tick"""
        self.velocity = min(self.velocity + GRAVITY, MAX_FALL_SPEED)
        self.y += self.velocity

        # Keep the bird on screen
        top = 0
        bottom = SCREEN_SIZE[1] - self.rect.height
        if self.y < top:
            self.y = top
            self.velocity = 0
        elif self.y > bottom:
            self.y = bottom
            self.velocity = 0

        self.tick += 1

        tilt = -self.velocity * TILT_PER_SPEED
        self.angle = max(MAX_TILT_DOWN, min(MAX_TILT_UP, tilt))

    def draw(self, surface: Surface, rect: Rect | None = None, wing: BirdWing | None = None) -> None:
        """Updates the bird, then draws it to the surface.

        Args:
            surface (Surface): surface to draw on
            rect (Rect | None, optional): where to draw. Defaults to the bird's own pos.
            wing (BirdWing | None, optional): Frame to show. Defaults to the flapping animation.
        """
        self.update()
        # Compare with None: BirdWing.UP is 0 and a zero-size Rect is falsy, so `or` would skip them
        wing = self.wing if wing is None else wing
        rect = self.rect if rect is None else rect
        image = rotate(self.frames[wing].img, self.angle)
        centre = rect.center
        surface.blit(image, image.get_rect(center=centre))

    def hits_ceiling(self) -> bool:
        """True if the bird is at the top of the screen"""
        return self.rect.top <= 0

    def hits_ground(self, ground_y: int) -> bool:
        """True if the bird has is at the bottom of the screen

        Args:
            ground_y (int): y position of the top of the ground
        """
        return self.rect.bottom >= ground_y

    def collides_with(self, obstacles: Iterable[Rect]) -> bool:
        """True if the bird overlaps any of the given rects"""
        return self.rect.collidelist(list(obstacles)) != -1
