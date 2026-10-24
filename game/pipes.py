"""Pipe generation, movement, and collision behavior."""
import random
import pygame
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
        self.bottom_pipe = pygame.Rect(self.x, self.gap_y + self.gap_height // 2, self.width, SCREEN_SIZE[1] - (self.gap_y + self.gap_height // 2))

    def update(self) -> None:
        # Move both pipe rectangles to the left.
        self.top_pipe.x -= self.speed
        self.bottom_pipe.x -= self.speed
        

    def draw(self, screen: pygame.Surface) -> None:
        # Draw both rectangles.
        pygame.draw.rect(screen, (0, 255, 0), self.top_pipe)
        pygame.draw.rect(screen, (0, 255, 0), self.bottom_pipe)
        

    def collides_with(self, bird_rect: pygame.Rect) -> bool:
        # Return True if the bird overlaps either pipe.
        return self.top_pipe.colliderect(bird_rect) or self.bottom_pipe.colliderect(bird_rect)
