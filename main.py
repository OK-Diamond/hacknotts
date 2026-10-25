import sys

import pygame
from game.tracking import FaceTracker
from game.bird import Bird, BirdColour
from game.pipes import PipeManager
from game.config import SCREEN_SIZE
from game.scenes import draw_background, draw_game_over
from game.ui import Button

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
pygame.display.set_caption("Flappy Face")
BG = pygame.image.load("./assets/images/main-menu/Background.png")

# ---- high score saving/loading ----
HIGH_SCORE_FILE = "highscore.txt"

def load_high_score():
    try:
        with open(HIGH_SCORE_FILE) as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return 0

def save_high_score(value):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(value))

high_score = load_high_score()

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("./assets/fonts/font.ttf", size)

def main_game():
    global high_score
    pygame.display.set_caption("Flappy Face")
    font = pygame.font.SysFont(None, 48)
    clock = pygame.time.Clock()
    pipe_manager = PipeManager()
    tracker = FaceTracker()
    running = True
    game_over = False # for game over screen need to know this!
    blink_count = 0
    score_count = 0
    blink_flash_frames = 0  # how long to keep showing "BLINK!"

    bird = Bird(BirdColour.RED)

    game_over_font = pygame.font.SysFont(None, 64)

    score_font = pygame.font.Font('./assets/fonts/Rocketron.otf', 48)
    arial_font = pygame.font.Font('./assets/fonts/Rocketron.otf', 36)

    while running:
        screen.blit(BG, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tracker.release()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    # Reset game state
                    bird = Bird(BirdColour.RED)
                    pipe_manager = PipeManager()
                    blink_count = 0
                    blink_flash_frames = 0
                    game_over = False
                    score_count = 0
                if event.key == pygame.K_ESCAPE:
                    tracker.release()
                    return  # back to the menu loop that called us

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
                bird.crash()
                game_over = True

            # increment score if the bird has crossed a pipe
            score_count += pipe_manager.increment_score(bird.rect)

            # update and save the high score
            if score_count > high_score:
                high_score = score_count
                save_high_score(high_score)

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

            score_text = score_font.render(f'Score: {score_count}', True, (255, 255, 0))
            screen.blit(score_text, (20, 500))

        else:
            # Game over screen
            pipe_manager.draw(screen) # freezes pipes, as no longer updating them

            frozen_bird_image = pygame.transform.rotate( # frozen image of the bird at its current angle
                bird.frames[bird.wing].img,
                bird.angle,
            )
            screen.blit( # draw the frozen bird image at its current position
                frozen_bird_image,
                frozen_bird_image.get_rect(center=bird.rect.center),
            )
            screen.blit(score_text, (20, 500))

            draw_game_over(screen, arial_font)

        pygame.display.flip()
        clock.tick(30)

def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("", True, "#FFC857")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        # high score: plain text, not a button
        HIGH_SCORE_TEXT = get_font(30).render(f"HIGH SCORE: {high_score}", True, "#FFC857")
        HIGH_SCORE_RECT = HIGH_SCORE_TEXT.get_rect(center=(400, 200))

        # Play button sits where Options used to be
        PLAY_BUTTON = Button(image=pygame.image.load("./assets/images/main-menu/Play Rect.png"), pos=(400, 350),
                            text_input="PLAY", font=get_font(35), base_color="#FFC857", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("./assets/images/main-menu/Quit Rect.png"), pos=(400, 500),
                            text_input="QUIT", font=get_font(35), base_color="#FFC857", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(HIGH_SCORE_TEXT, HIGH_SCORE_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_game()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()