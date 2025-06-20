import pygame
import settings
from sounds import gameover_song, mainmenu_song, game_win_song

def main_menu(screen,clock):
    mainmenu_song()
    menu_running = True
    font = pygame.font.SysFont(None, 72)
    play_button = pygame.Rect(settings.WIDTH//2 - 100, settings.HEIGHT//2 - 60, 200, 60)
    quit_button = pygame.Rect(settings.WIDTH//2 - 100, settings.HEIGHT//2 + 20, 200, 60)

    while menu_running:
        screen.fill((30, 30, 30))
        title = font.render("Top Down Shooter", True, (255, 255, 255))
        screen.blit(title, (settings.WIDTH//2 - title.get_width()//2, 100))

        pygame.draw.rect(screen, (70, 130, 180), play_button)
        pygame.draw.rect(screen, (220, 50, 50), quit_button)

        mtc_logo = pygame.transform.scale(pygame.image.load(settings.MTC_LOGO).convert_alpha(), (settings.MTC_WIDTH, settings.MTC_HEIGHT))


        play_text = font.render("Play", True, (255,255,255))
        quit_text = font.render("Quit", True, (255,255,255))

        screen.blit(play_text, (play_button.x + 50, play_button.y + 10))
        screen.blit(quit_text, (quit_button.x + 40, quit_button.y + 10))
        
        screen.blit(mtc_logo, (20,600))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    menu_running = False 
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        pygame.display.update()
        clock.tick(60)

def show_game_over_screen(screen):
    gameover_song()
    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 36)
    screen.fill((30, 0, 0))  # Dark Red background

    # Game Over text
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(game_over_text, (settings.WIDTH//2 - game_over_text.get_width()//2, settings.HEIGHT//2 - 100))

    # Restart prompt
    restart_text = small_font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
    screen.blit(restart_text, (settings.WIDTH//2 - restart_text.get_width()//2, settings.HEIGHT//2))

    pygame.display.update()

    # Wait for user input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False  # Will restart the game
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit()
                    exit()
        pygame.time.Clock().tick(15)

def show_win_screen(screen, elapsed_seconds, lives_left):
    game_win_song()
    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 36)
    screen.fill((0, 30, 0))  # Dark green background

    # Win text
    win_text = font.render("You Win!", True, (0, 255, 0))
    screen.blit(win_text, (settings.WIDTH//2 - win_text.get_width()//2, settings.HEIGHT//2 - 120))

    # Score details
    minutes = elapsed_seconds // 60
    seconds = elapsed_seconds % 60
    time_text = small_font.render(f"Time: {minutes:02}:{seconds:02}", True, (255, 255, 255))
    lives_text = small_font.render(f"Lives Left: {lives_left}", True, (255, 255, 255))
    screen.blit(time_text, (settings.WIDTH//2 - time_text.get_width()//2, settings.HEIGHT//2 - 40))
    screen.blit(lives_text, (settings.WIDTH//2 - lives_text.get_width()//2, settings.HEIGHT//2))

    time_score = 3000 if elapsed_seconds < 240 else (2000 if elapsed_seconds < 300 else (1000 if elapsed_seconds < 360 else 0))

    score = lives_left * 1000 + time_score
    score_text = small_font.render(f"Score: {score}", True, (255, 255, 0))
    screen.blit(score_text, (settings.WIDTH//2 - score_text.get_width()//2, settings.HEIGHT//2 + 30))
    
    # Restart button
    restart_text = small_font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
    screen.blit(restart_text, (settings.WIDTH//2 - restart_text.get_width()//2, settings.HEIGHT//2 + 60))

    pygame.display.update()

    #waiting for user input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False  # Will restart the game
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit()
                    exit()
        pygame.time.Clock().tick(15)
