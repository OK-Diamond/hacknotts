import pygame
from game.tracking import FaceTracker
from game.bird import Bird, BirdColour
from game.pipes import PipeManager
from game.config import SCREEN_SIZE
from game.scenes import draw_background, draw_game_over

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
pygame.display.set_caption("Flappy Bird Eye Cam")
font = pygame.font.SysFont(None, 48)
clock = pygame.time.Clock()
pipe_manager = PipeManager()
tracker = FaceTracker()
running = True
game_over = False # for game over screen need to know this!
blink_count = 0
blink_flash_frames = 0  # how long to keep showing "BLINK!"

bird = Bird(BirdColour.RED)

game_over_font = pygame.font.SysFont(None, 64)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and game_over: 
                    # Reset game state
                    bird = Bird(BirdColour.RED)
                    pipe_manager = PipeManager()
                    blink_count = 0
                    blink_flash_frames = 0
                    game_over = False

    face_seen = tracker.update()

    # register a blink
    if not game_over and tracker.blinked:
        blink_count += 1
        blink_flash_frames = 15  # about half a second at 30 FPS
        bird.flap()              # flap once per blink
        print(f"Blink detected! Total: {blink_count}")
    if not game_over and blink_flash_frames > 0:
        blink_flash_frames -= 1

    # 1. background
    draw_background(screen, speed=0 if game_over else 5)
    
    if not game_over:
        # 2. pipes
        pipe_manager.update()
        pipe_manager.draw(screen)

        # 3. bird
        bird.draw(screen)

        # end game if the bird collides with a pipe
        if pipe_manager.collision_check(bird.rect):
            game_over = True

        # 4. webcam preview in the top-right corner
        if tracker.frame is not None:
            h, w, _ = tracker.frame.shape
            cam_surface = pygame.image.frombuffer(tracker.frame.tobytes(), (w, h), "RGB")
            screen.blit(pygame.transform.scale(cam_surface, (200, 150)), (SCREEN_SIZE[0] - 210, 10))

        # 5. text
        text = "I can see you!" if face_seen else "No face found"
        colour = (0, 255, 0) if face_seen else (255, 60, 60)
        screen.blit(font.render(text, True, colour), (20, 20))

        if face_seen:
            state = "Eyes open" if tracker.eyes_open else "Eyes closed"
            screen.blit(font.render(state, True, (255, 255, 255)), (20, 60))

        screen.blit(font.render(f"Blinks: {blink_count}", True, (255, 255, 255)), (20, 100))
        if blink_flash_frames > 0:
            screen.blit(font.render("BLINK!", True, (255, 220, 0)), (20, 140))

        
    else:
        # Game over screen
        pipe_manager.draw(screen) # freezes pipes, as no longer updating them

        frozen_bird_image = pygame.transform.rotate( # create a frozen image of the bird at its current angle
            bird.frames[bird.wing].img,
            bird.angle,
        )
        screen.blit( # draw the frozen bird image at its current position
            frozen_bird_image,
            frozen_bird_image.get_rect(center=bird.rect.center),
        )

        draw_game_over(screen, game_over_font, font) 

    pygame.display.flip()
    clock.tick(30)

tracker.release()
pygame.quit()