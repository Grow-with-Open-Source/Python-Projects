import pygame
import random
pygame.init()

GRID_SIZE = 40
GRID_WIDTH = 17  
GRID_HEIGHT = 17  
SCREEN_WIDTH = GRID_SIZE * GRID_WIDTH
SCREEN_HEIGHT = GRID_SIZE * GRID_HEIGHT
BG_COLOR = (30, 30, 30)  
PLAYER_COLOR = (0, 255, 0)
COIN_COLOR = (255, 215, 0)
POISON_COLOR = (255, 0, 0)
FPS = 15

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("coin&poison")

font = pygame.font.Font(None, 36)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.score = 0

    def move(self, dx, dy):
        new_rect = self.rect.move(dx * GRID_SIZE, dy * GRID_SIZE)
        if 0 <= new_rect.left < SCREEN_WIDTH and 0 <= new_rect.top < SCREEN_HEIGHT: # within limits
            self.rect = new_rect
        else:
            self.score -= 1 # hit the boundary

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(COIN_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * GRID_SIZE, y * GRID_SIZE)

class Poison(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(POISON_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * GRID_SIZE, y * GRID_SIZE)

# to spawn coin and poison blocks without overlapping with each other and player
def spawn_objects(num_objects, avoid_positions):
    objects = []
    while len(objects) < num_objects:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if (x, y) not in avoid_positions:
            objects.append((x, y))
            avoid_positions.add((x, y))
    return objects

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# total no of coins and poison blocks
num_coins = 20  
num_poisons = 10  

avoid_positions = {(player.rect.x // GRID_SIZE, player.rect.y // GRID_SIZE)}

poison_positions = spawn_objects(num_poisons, avoid_positions)
poisons = pygame.sprite.Group()
for pos in poison_positions:
    poison = Poison(*pos)
    poisons.add(poison)
    all_sprites.add(poison)

coin_positions = spawn_objects(num_coins, avoid_positions)
coins = pygame.sprite.Group()
for pos in coin_positions:
    coin = Coin(*pos)
    coins.add(coin)
    all_sprites.add(coin)

clock = pygame.time.Clock()

running = True
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

    collected_coins = pygame.sprite.spritecollide(player, coins, True)
    player.score += len(collected_coins)

    if pygame.sprite.spritecollideany(player, poisons):
        print(f"collided with poison block! score: {player.score}")
        running = False

    # if all coins collected, won
    if len(coins) == 0:
        print(f"collected all coins! score: {player.score}")
        running = False

    screen.fill(BG_COLOR)
    all_sprites.draw(screen)

    score_text = font.render(f"score: {player.score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10)) 

    pygame.display.flip()

pygame.quit()