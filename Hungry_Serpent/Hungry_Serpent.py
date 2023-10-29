import pygame
import random

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
CELL_SIZE = 20
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# Snake initial position and properties
snake_pos = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
snake_direction = "RIGHT"
snake_length = 1

# Food initial position
food_pos = (random.randrange(1, SCREEN_WIDTH // CELL_SIZE) * CELL_SIZE,
            random.randrange(1, SCREEN_HEIGHT // CELL_SIZE) * CELL_SIZE)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Change snake direction based on arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and not snake_direction == "DOWN":
            snake_direction = "UP"
        if keys[pygame.K_DOWN] and not snake_direction == "UP":
            snake_direction = "DOWN"
        if keys[pygame.K_LEFT] and not snake_direction == "RIGHT":
            snake_direction = "LEFT"
        if keys[pygame.K_RIGHT] and not snake_direction == "LEFT":
            snake_direction = "RIGHT"

    # Move the snake
    head_x, head_y = snake_pos[0]
    if snake_direction == "UP":
        head_y -= CELL_SIZE
    if snake_direction == "DOWN":
        head_y += CELL_SIZE
    if snake_direction == "LEFT":
        head_x -= CELL_SIZE
    if snake_direction == "RIGHT":
        head_x += CELL_SIZE

    # Update snake position
    snake_pos.insert(0, (head_x, head_y))

    # Check if snake eats food
    if head_x == food_pos[0] and head_y == food_pos[1]:
        snake_length += 1
        food_pos = (random.randrange(1, SCREEN_WIDTH // CELL_SIZE) * CELL_SIZE,
                    random.randrange(1, SCREEN_HEIGHT // CELL_SIZE) * CELL_SIZE)

    # Check if snake collides with itself or the walls
    if (head_x < 0 or head_x >= SCREEN_WIDTH or
            head_y < 0 or head_y >= SCREEN_HEIGHT or
            len(snake_pos) != len(set(snake_pos))):
        running = False

    # Keep snake length
    if len(snake_pos) > snake_length:
        snake_pos.pop()

    # Draw everything
    screen.fill(WHITE)

    # Draw snake
    for pos in snake_pos:
        pygame.draw.rect(screen, GREEN, (pos[0], pos[1], CELL_SIZE, CELL_SIZE))

    # Draw food
    pygame.draw.rect(screen, RED, (food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))

    pygame.display.flip()

    # Limit frames per second
    clock.tick(10)

# Quit the game
pygame.quit()
