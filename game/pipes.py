"""Pipe generation, movement, and collision behavior."""
import pygame

from game.assets import ImageAsset as Img
from game.config import SCREEN_SIZE

class PipePair:
    def __init__(self, x: int, gap_y: int) -> None:
        # Store position, gap, width, and speed.
        self.x = x
        self.gap_y = gap_y
        self.width = 80
        self.speed = 5
        self.gap_height = 150  # Height of the gap between pipes
        # Create one Rect for the top pipe and one for the bottom.
        self.top_pipe = pygame.Rect(self.x, 0, self.width, self.gap_y - self.gap_height // 2)
        self.bottom_pipe = pygame.Rect(
            self.x,
            self.gap_y + self.gap_height // 2,
            self.width,
            SCREEN_SIZE[1] - (self.gap_y + self.gap_height // 2),
        )
        pipe_image = Img("./assets/images/pipe-green.png")
        self.top_image = pygame.transform.scale(
            pygame.transform.flip(pipe_image.img, False, True),
            self.top_pipe.size,
        )
        self.bottom_image = pygame.transform.scale(pipe_image.img, self.bottom_pipe.size)

    def update(self) -> None:
        # Move both pipe rectangles to the left.
        self.top_pipe.x -= self.speed
        self.bottom_pipe.x -= self.speed
        

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.top_image, self.top_pipe)
        screen.blit(self.bottom_image, self.bottom_pipe)

    def collides_with(self, bird_rect: pygame.Rect) -> bool:
        # Return True if the bird overlaps either pipe.
        return self.top_pipe.colliderect(bird_rect) or self.bottom_pipe.colliderect(bird_rect)
