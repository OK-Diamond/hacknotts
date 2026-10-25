"""Pipe generation, movement, and collision behavior."""
import random

import pygame

from game.assets import ImageAsset as Img
from game.config import SCREEN_SIZE


class PipePair:
    GAP_HEIGHT = 150

    def __init__(self, x: int, gap_y: int) -> None:
        # Store position, gap, width, and speed.
        self.x = x
        self.gap_y = gap_y
        self.width = 80
        self.speed = 5
        self.gap_height = self.GAP_HEIGHT
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
        self.x -= self.speed
        self.top_pipe.x = self.x
        self.bottom_pipe.x = self.x

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.top_image, self.top_pipe)
        screen.blit(self.bottom_image, self.bottom_pipe)

    def collides_with(self, bird_rect: pygame.Rect) -> bool:
        # Return True if the bird overlaps either pipe.
        return self.top_pipe.colliderect(bird_rect) or self.bottom_pipe.colliderect(bird_rect)

    def cross_pipe(self, bird_rect: pygame.Rect) -> bool:
        """Return True if the bird has just crossed the pipe pair."""
        pipe_right_after_move = self.x + self.width
        pipe_right_before_move = pipe_right_after_move + self.speed

        crossed_bird = (
            pipe_right_before_move >= bird_rect.left
            and pipe_right_after_move < bird_rect.left
        )
        return crossed_bird

class PipeManager:
    """Create, update, draw, and remove the active pipe pairs."""

    def __init__(self) -> None:
        self.spacing = 250
        self.pipes = [self._create_pipe(SCREEN_SIZE[0])]

    def _create_pipe(self, x: int) -> PipePair:
        gap_margin = 40
        min_gap_y = PipePair.GAP_HEIGHT // 2 + gap_margin
        max_gap_y = SCREEN_SIZE[1] - PipePair.GAP_HEIGHT // 2 - gap_margin
        gap_y = random.randint(min_gap_y, max_gap_y)
        return PipePair(x, gap_y)

    def update(self) -> None:
        for pipe in self.pipes:
            pipe.update()

        self.pipes = [
            pipe for pipe in self.pipes
            if pipe.top_pipe.right > 0
        ]

        if not self.pipes or self.pipes[-1].x <= SCREEN_SIZE[0] - self.spacing:
            self.pipes.append(self._create_pipe(SCREEN_SIZE[0]))

    def draw(self, screen: pygame.Surface) -> None:
        for pipe in self.pipes:
            pipe.draw(screen)

    def collision_check(self, bird_rect: pygame.Rect) -> bool:
        """Return True if the bird collides with any pipe."""
        return any(pipe.collides_with(bird_rect) for pipe in self.pipes)

    def increment_score(self, bird_rect: pygame.Rect) -> int:
        """Increment the score for each pipe the bird has crossed."""
        for pipe in self.pipes:
            if pipe.cross_pipe(bird_rect):
                return 1  # Return 1 if pipe crossed
        return 0