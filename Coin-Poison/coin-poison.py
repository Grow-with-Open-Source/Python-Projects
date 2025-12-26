import pygame
import random

pygame.init()

# ================== CONFIG ==================
GRID_SIZE = 40
GRID_WIDTH = 17
GRID_HEIGHT = 17
SCREEN_WIDTH = GRID_SIZE * GRID_WIDTH
SCREEN_HEIGHT = GRID_SIZE * GRID_HEIGHT

BG_COLOR = (30, 30, 30)
PLAYER_COLOR = (0, 255, 0)
COIN_COLOR = (255, 215, 0)
POISON_COLOR = (255, 0, 0)
SHIELD_COLOR = (0, 191, 255)

FPS = 15

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Coin & Poison Adventure")

font = pygame.font.Font(None, 36)

# ================== CLASSES ==================

class Player(pygame.sprite.Sprite):
    """Player controlled by arrow keys"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.score = 0
        self.lives = 3
        self.shield = False

    def move(self, dx, dy):
        new_rect = self.rect.move(dx * GRID_SIZE, dy * GRID_SIZE)
        if 0 <= new_rect.left < SCREEN_WIDTH and 0 <= new_rect.top < SCREEN_HEIGHT:
            self.rect = new_rect
        else:
            self.score -= 1  # penalize hitting boundary

class Coin(pygame.sprite.Sprite):
    """Collectible coin"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(COIN_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * GRID_SIZE, y * GRID_SIZE)

class Poison(pygame.sprite.Sprite):
    """Poison block that reduces life"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(POISON_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * GRID_SIZE, y * GRID_SIZE)

class Shield(pygame.sprite.Sprite):
    """Power-up shield to protect from poison"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(SHIELD_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * GRID_SIZE, y * GRID_SIZE)

# ================== HELPER FUNCTIONS ==================

def spawn_objects(num_objects, avoid_positions):
    """Spawn objects without overlapping"""
    objects = []
    while len(objects) < num_objects:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if (x, y) not in avoid_positions:
            objects.append((x, y))
            avoid_positions.add((x, y))
    return objects

def reset_level():
    """Reset coins, poisons, and optionally add shield"""
    global coins, poisons, shield_powerups, all_sprites, avoid_positions, FPS, level
    level += 1
    FPS += 1  # increase speed for next level
    num_coins = 10 + level * 2
    num_poisons = 5 + level

    # Clear old objects
    for sprite in coins.sprites() + poisons.sprites() + shield_powerups.sprites():
        all_sprites.remove(sprite)
    
    # Reset positions
    avoid_positions = {(player.rect.x // GRID_SIZE, player.rect.y // GRID_SIZE)}
    
    # Spawn coins
    coin_positions = spawn_objects(num_coins, avoid_positions)
    coins = pygame.sprite.Group()
    for pos in coin_positions:
        coin = Coin(*pos)
        coins.add(coin)
        all_sprites.add(coin)

    # Spawn poisons
    poison_positions = spawn_objects(num_poisons, avoid_positions)
    poisons = pygame.sprite.Group()
    for pos in poison_positions:
        poison = Poison(*pos)
        poisons.add(poison)
        all_sprites.add(poison)

    # Spawn shield occasionally
    shield_positions = spawn_objects(1, avoid_positions)
    shield_powerups = pygame.sprite.Group()
    for pos in shield_positions:
        shield = Shield(*pos)
        shield_powerups.add(shield)
        all_sprites.add(shield)

# ================== GAME INIT ==================

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

coins = pygame.sprite.Group()
poisons = pygame.sprite.Group()
shield_powerups = pygame.sprite.Group()
avoid_positions = {(player.rect.x // GRID_SIZE, player.rect.y // GRID_SIZE)}

level = 1
reset_level()

clock = pygame.time.Clock()
running = True

# ================== GAME LOOP ==================

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-1, 0)
    if keys[pygame.K_RIGHT]:
        player.move(1, 0)
    if keys[pygame.K_UP]:
        player.move(0, -1)
    if keys[pygame.K_DOWN]:
        player.move(0, 1)

    # Collect coins
    collected_coins = pygame.sprite.spritecollide(player, coins, True)
    player.score += len(collected_coins)

    # Collect shield
    if pygame.sprite.spritecollide(player, shield_powerups, True):
        player.shield = True
        print("Shield activated! Next poison hit will be ignored.")

    # Poison collision
    if pygame.sprite.spritecollideany(player, poisons):
        if player.shield:
            player.shield = False
            print("Shield protected you from poison!")
        else:
            player.lives -= 1
            if player.lives == 0:
                print(f"Game Over! Final Score: {player.score}")
                running = False
            else:
                print(f"Hit poison! Lives left: {player.lives}")

    # Level completed
    if len(coins) == 0:
        print(f"Level {level} cleared! Moving to next level...")
        reset_level()

    # Draw everything
    screen.fill(BG_COLOR)
    all_sprites.draw(screen)
    score_text = font.render(f"Score: {player.score} | Coins left: {len(coins)} | Lives: {player.lives} | Level: {level}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
