"""Bird position, movement, and collision behavior."""
from enum import Enum, IntEnum
from pygame import Surface, Rect

from game.assets import ImageAsset as Img

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

class Bird:
    """Bird object"""
    def __init__(self, colour: BirdColour) -> None:
        name = colour.name.lower()
        self.frames = [
            Img(f'./assets/images/{name}bird-upflap.png'),
            Img(f'./assets/images/{name}bird-midflap.png'),
            Img(f'./assets/images/{name}bird-downflap.png')
        ]

    def draw(self, surface: Surface, rect: Rect|None = None, wing_pos: BirdWing = BirdWing.UP) -> None:
        """Draws the bird to the surface.

        Args:
            surface (Surface): surface to draw on
            rect (Rect | None, optional): rect to draw - image asset's rect if none. Defaults to None.
            wing_pos (BirdWing, optional): Frame to show. Defaults to BirdWing.UP.
        """
        if rect:
            surface.blit(self.frames[wing_pos].img, rect)
        surface.blit(self.frames[wing_pos].img, self.frames[wing_pos].rect)
