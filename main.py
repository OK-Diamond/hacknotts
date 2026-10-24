import pygame

from game.config import FPS, SCREEN_SIZE
import game.bird as bird

red_bird = bird.Bird(bird.BirdColour.RED)

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Flappy Face")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 30))
        
        red_bird.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
