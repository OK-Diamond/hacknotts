import pygame

from game.config import FPS, SCREEN_SIZE
import game.bird as bird

from game.pipes import PipePair

red_bird = bird.Bird(bird.BirdColour.RED)
pipe = PipePair(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)

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

        pipe.update()
        pipe.draw(screen)
        red_bird.draw(screen)
        
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
