import pygame
import random
import time

# --- Setup ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neural Pulse: Memory & Logic")
font_main = pygame.font.SysFont("Arial", 28)
font_huge = pygame.font.SysFont("Arial", 60)

# Colors
BG_COLOR = (15, 15, 25)
TEXT_COLOR = (200, 200, 220)
ACCENT_COLOR = (0, 255, 200)
MEM_COLOR = (255, 200, 0) # Gold for memory sequence

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(x, y))
    screen.blit(img, rect)

def main_game():
    clock = pygame.time.Clock()
    state = "MENU"
    
    # Game Variables
    level = 1
    score = 0
    sequence = []
    user_step = 0
    show_index = 0
    last_flash_time = 0
    
    running = True
    while running:
        screen.fill(BG_COLOR)
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "MENU":
                    state = "START_LEVEL"
                
                elif state == "PLAYING":
                    # Check if user clicked the correct target
                    target_rect = sequence[user_step]
                    if target_rect.collidepoint(event.pos):
                        user_step += 1
                        score += 100
                        if user_step == len(sequence):
                            level += 1
                            state = "START_LEVEL"
                    else:
                        # Wrong click!
                        state = "RESULTS"

        # --- Game States ---
        if state == "MENU":
            draw_text("MEMORY CHALLENGE", font_huge, ACCENT_COLOR, WIDTH//2, HEIGHT//2 - 50)
            draw_text("Watch the sequence, then repeat it.", font_main, TEXT_COLOR, WIDTH//2, HEIGHT//2 + 20)
            draw_text("Click to Start", font_main, (100, 100, 100), WIDTH//2, HEIGHT//2 + 80)

        elif state == "START_LEVEL":
            # Generate a sequence of 3 random squares (increases with level)
            sequence = []
            num_targets = 2 + (level // 2)
            for _ in range(num_targets):
                rect = pygame.Rect(random.randint(50, 700), random.randint(100, 500), 60, 60)
                sequence.append(rect)
            
            show_index = 0
            user_step = 0
            last_flash_time = now
            state = "MEMORIZING"

        elif state == "MEMORIZING":
            draw_text(f"MEMORIZE: {show_index + 1}/{len(sequence)}", font_main, MEM_COLOR, WIDTH//2, 40)
            
            # Flash each square for 600ms
            if show_index < len(sequence):
                current_rect = sequence[show_index]
                pygame.draw.rect(screen, MEM_COLOR, current_rect, border_radius=8)
                
                if now - last_flash_time > 800 - (level * 20): # Speed up as levels go up
                    show_index += 1
                    last_flash_time = now
            else:
                state = "PLAYING"

        elif state == "PLAYING":
            draw_text(f"REPEAT THE PATTERN", font_main, ACCENT_COLOR, WIDTH//2, 40)
            draw_text(f"Level: {level}  Score: {score}", font_main, TEXT_COLOR, WIDTH//2, HEIGHT - 30)
            
            # In a real game, targets are invisible or faint
            for rect in sequence:
                pygame.draw.rect(screen, (40, 40, 60), rect, 2, border_radius=8)

        elif state == "RESULTS":
            draw_text("GAME OVER", font_huge, (255, 50, 50), WIDTH//2, HEIGHT//2 - 50)
            draw_text(f"Final Level: {level} | Score: {score}", font_main, TEXT_COLOR, WIDTH//2, HEIGHT//2 + 20)
            draw_text("Click to Retry", font_main, (100, 100, 100), WIDTH//2, HEIGHT//2 + 80)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main_game()