import pygame
from game.tracking import FaceTracker

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Blinky Bird")
font = pygame.font.SysFont(None, 48)
clock = pygame.time.Clock()

tracker = FaceTracker()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    face_seen = tracker.update()

    screen.fill((30, 30, 30))

    # show the webcam feed so you can check it's working
    if tracker.frame is not None:
        h, w, _ = tracker.frame.shape
        cam_surface = pygame.image.frombuffer(tracker.frame.tobytes(), (w, h), "RGB")
        screen.blit(pygame.transform.scale(cam_surface, (640, 480)), (0, 0))

    text = "I can see you!" if face_seen else "No face found"
    colour = (0, 255, 0) if face_seen else (255, 60, 60)
    screen.blit(font.render(text, True, colour), (20, 20))

    pygame.display.flip()
    clock.tick(30)

tracker.release()
pygame.quit()