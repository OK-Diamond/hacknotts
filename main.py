import pygame
from game.tracking import FaceTracker
from game.bird import Bird, BirdColour
from game.pipes import PipePair
from game.config import SCREEN_SIZE

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
pygame.display.set_caption("Flappy Bird Eye Cam")
font = pygame.font.SysFont(None, 48)
clock = pygame.time.Clock()
pipe_manager = PipeManager()
tracker = FaceTracker()
running = True

blink_count = 0
blink_flash_frames = 0  # how long to keep showing "BLINK!"

bird = Bird(BirdColour.RED)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    face_seen = tracker.update()

    # register a blink
    if tracker.blinked:
        blink_count += 1
        blink_flash_frames = 15  # about half a second at 30 FPS
        print(f"Blink detected! Total: {blink_count}")
    if blink_flash_frames > 0:
        blink_flash_frames -= 1

    screen.fill((30, 30, 30))

    # show the webcam feed so you can check it's working
    if tracker.frame is not None:
        h, w, _ = tracker.frame.shape
        cam_surface = pygame.image.frombuffer(tracker.frame.tobytes(), (w, h), "RGB")
        screen.blit(pygame.transform.scale(cam_surface, SCREEN_SIZE), (0, 0))

    text = "I can see you!" if face_seen else "No face found"
    colour = (0, 255, 0) if face_seen else (255, 60, 60)
    screen.blit(font.render(text, True, colour), (20, 20))
    pipe_manager.update()
    pipe_manager.draw(screen)

    if face_seen:
        state = "Eyes open" if tracker.eyes_open else "Eyes closed"
        screen.blit(font.render(state, True, (255, 255, 255)), (20, 60))

    screen.blit(font.render(f"Blinks: {blink_count}", True, (255, 255, 255)), (20, 100))
    if blink_flash_frames > 0:
        screen.blit(font.render("BLINK!", True, (255, 220, 0)), (20, 140))
    
    # Bird
    bird.draw(screen)

    pygame.display.flip()
    clock.tick(30)

tracker.release()
pygame.quit()