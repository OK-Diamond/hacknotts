"""Load and cache assets"""
from dataclasses import dataclass
from pygame.image import load
from pygame import Surface, Rect

@dataclass
class ImageAsset:
    """Dataclass for pygame images"""
    def __init__(self, path: str) -> None:
        self.img: Surface = load(path)
        self.rect: Rect = self.img.get_rect()
