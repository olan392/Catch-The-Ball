import pygame
import random

# 1. Setup - Use pygame.SCALED for better mobile compatibility
pygame.init()

# Add app icon
icon = pygame.image.load('icon.png')

pygame.display.set_icon(icon)

# Get the device screen size
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# If testing on Desktop, you might want a fixed size:
# SCREEN_WIDTH, SCREEN_HEIGHT = 400, 700 

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLUE = (50, 50, 255)

# Player setup (Scaling size based on screen width)
player_size = SCREEN_WIDTH // 6
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - (player_size * 2)]

# Target setup
target_size = SCREEN_WIDTH // 10
target_pos = [random.randint(0, SCREEN_WIDTH - target_size), 0]
speed = SCREEN_HEIGHT // 100  # Adjust speed based on screen height

score = 0
font = pygame.font.SysFont("Arial", SCREEN_WIDTH // 15)

running = True
while running:
    screen.fill(WHITE)

    # 2. Touch/Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # MOBILE TOUCH INPUT
        if event.type == pygame.FINGERMOTION or event.type == pygame.FINGERDOWN:
            # Finger coordinates are normalized (0.0 to 1.0), so we multiply by screen size
            player_pos[0] = event.x * SCREEN_WIDTH - (player_size // 2)

        # DESKTOP MOUSE INPUT (for testing)
        if event.type == pygame.MOUSEMOTION:
            player_pos[0] = event.pos[0] - (player_size // 2)

    # 3. Game Logic
    target_pos[1] += speed
    
    # Reset target if it falls off screen
    if target_pos[1] > SCREEN_HEIGHT:
        target_pos = [random.randint(0, SCREEN_WIDTH - target_size), 0]
        score -= 1 # Penalty for missing

    # Collision Detection
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    target_rect = pygame.Rect(target_pos[0], target_pos[1], target_size, target_size)

    if player_rect.colliderect(target_rect):
        score += 1
        target_pos = [random.randint(0, SCREEN_WIDTH - target_size), -target_size]
        speed += 0.2 # Get harder

    # 4. Drawing
    pygame.draw.rect(screen, BLUE, player_rect)
    pygame.draw.ellipse(screen, RED, target_rect)
    
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (20, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
