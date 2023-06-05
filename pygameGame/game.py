import math
import pygame
import os
# Initialize Pygame
pygame.init()


class Level():
    def __init__(self, image, collision, enemy_list, powerup_map):
        self.image = image
        self.collision = collision
        self.enemies = [Enemy(x[0], x[1], x[2]) for x in enemy_list]  # [[x, y, imgs]]
        self.powerup_map = powerup_map
        self.powerups = []
        # yellow = coin, more coming soon
        for x in range(self.powerup_map.get_width()):
            for y in range(self.powerup_map.get_height()):
                if self.powerup_map.get_at((x, y)) == (255, 255, 0):
                    is_colliding = False
                    for powerup in self.powerups:
                        if (abs(powerup.rect.x - x)) <= player.image.get_width() / 2 and (
                    abs(powerup.rect.y - y)) <= powerup.image.get_height() / 2:
                            is_colliding = True
                    if not is_colliding:
                        image_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "coin.png")
                        self.powerups.append(Powerup([image_name], "coin", x, y))


class Powerup(pygame.sprite.Sprite):
    def __init__(self, images, type, pos_x, pos_y):
        super().__init__()
        self.images = [pygame.image.load(image) for image in images]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.frame = 0
        self.type = type

    def update(self):
        self.image = self.images[self.frame]
        if self.frame < len(self.images) - 1:
            self.frame += 1
        else:
            self.frame = 0


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, images):
        super().__init__()
        self.images = [pygame.image.load(image) for image in images]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.frame = 0
        self.vel_x = 0
        self.vel_y = 0
        self.type = "enemy"

    def find_path(self, point_x, point_y):
        self.vel_x = (point_x - self.rect.x) * 0.025
        self.vel_y = (point_y - self.rect.y) * 0.025

    def update(self):
        self.find_path((player.rect.x + player.image.get_width() / 2), (player.rect.y + player.image.get_height() / 2))
        self.image = self.images[self.frame]
        if not self.check_collision(True):
            self.rect.x += self.vel_x
        if not self.check_collision(False):
            self.rect.y += self.vel_y

    def check_collision(self, direction):
        # true: horizontal, false: vertical
        # Check for collisions with obstacles
        map_width = level.collision.get_width()
        map_height = level.collision.get_height()
        scale_x = screen_width / map_width
        scale_y = screen_height / map_height
        if direction:
            sprite_rect = pygame.Rect(math.ceil(self.rect.x + self.vel_x), self.rect.y, sprite_width, sprite_height)
            collision = sprite_rect.collidelistall(
                [
                    pygame.Rect(x * scale_x, y * scale_y, 1, 1)
                    for x in range(math.ceil(screen_width / scale_x))
                    for y in range(math.ceil(screen_height / scale_y))
                    if level.collision.get_at((x, y)) == (0, 0, 0)
                ]
            )
            return collision
        else:
            sprite_rect = pygame.Rect(self.rect.x, math.ceil(self.rect.y + self.vel_y), sprite_width, sprite_height)
            collision = sprite_rect.collidelistall(
                [
                    pygame.Rect(x * scale_x, y * scale_y, 1, 1)
                    for x in range(math.ceil(screen_width / scale_x))
                    for y in range(math.ceil(screen_height / scale_y))
                    if level.collision.get_at((x, y)) == (0, 0, 0)
                ]
            )

            return collision


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        image_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "character.png")
        self.images = [pygame.image.load(image_name)]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.jump_count = 1
        self.frame = 0
        self.vel_x = 0
        self.vel_y = 0
        self.jump_speed = vertical_velocity
        self.coins = 0

    def check_collision(self, direction):
        # true: horizontal, false: vertical
        # Check for collisions with obstacles
        map_width = level.collision.get_width()
        map_height = level.collision.get_height()
        scale_x = screen_width / map_width
        scale_y = screen_height / map_height
        if direction:
            sprite_rect = pygame.Rect(math.ceil(self.rect.x + self.vel_x), self.rect.y, sprite_width, sprite_height)
            collision = sprite_rect.collidelistall(
                [
                    pygame.Rect(x * scale_x, y * scale_y, 1, 1)
                    for x in range(math.ceil(screen_width / scale_x))
                    for y in range(math.ceil(screen_height / scale_y))
                    if level.collision.get_at((x, y)) == (0, 0, 0)
                ]
            )
            return collision
        else:
            sprite_rect = pygame.Rect(self.rect.x, math.ceil(self.rect.y + self.vel_y), sprite_width, sprite_height)
            collision = sprite_rect.collidelistall(
                [
                    pygame.Rect(x * scale_x, y * scale_y, 1, 1)
                    for x in range(math.ceil(screen_width / scale_x))
                    for y in range(math.ceil(screen_height / scale_y))
                    if level.collision.get_at((x, y)) == (0, 0, 0)
                ]
            )

            return collision

    def get_colliding_powerups_and_enemies(self):
        collisions = []
        for enemy in level.enemies:
            if (abs(enemy.rect.x - player.rect.x)) <= player.image.get_width() / 2 and (
                    abs(enemy.rect.y - player.rect.y)) <= player.image.get_height() / 2:
                collisions.append(enemy)
        for powerup in level.powerups:
            if (abs(powerup.rect.x - player.rect.x)) <= powerup.image.get_width() / 2 and (
                    abs(powerup.rect.y - player.rect.y)) <= player.image.get_height() / 2:
                collisions.append(powerup)
        return collisions

    def update_char(self, left, right, jump):
        has_collected = False
        for collision in self.get_colliding_powerups_and_enemies():
            if collision.type == "coin":
                print(has_collected)
                level.powerups.remove(collision)
                if not has_collected:
                    self.coins += 1
                    has_collected = True
        # Jumping logic
        if jump:
            if self.jump_count <= max_jumps:
                self.vel_y = -self.jump_speed
                self.jump_count += 1
            elif self.check_collision(False):
                self.vel_y = -self.jump_speed
                self.jump_count = 1
        # ahh yes, python syntax
        if left:
            self.vel_x = -move_speed
        elif right:
            self.vel_x = move_speed
        else:
            self.vel_x = 0

        collision_h = self.check_collision(True)
        collision_v = self.check_collision(False)
        if collision_h:
            self.vel_x = 0
        else:
            self.rect.x += self.vel_x
        if collision_v:
            self.vel_y = 0
            self.jump_count = 1
        else:
            self.rect.y += self.vel_y
            self.vel_y += gravity
        self.image = self.images[self.frame]


# Set up the display
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Epic Python Game")

# Load sprite image and obstacle map
image_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "character.png")
sprite_image = pygame.image.load(image_name)
sprite_image = pygame.transform.scale(sprite_image, (32, 32))
image_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "obstacle_map.png")
obstacle_map = pygame.image.load(image_name)
image_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "map_img.png")
map_img = pygame.image.load(image_name)

# Get sprite and obstacle map dimensions
sprite_width, sprite_height = sprite_image.get_size()
obstacle_width, obstacle_height = obstacle_map.get_size()
image_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "obstacle_map.png")
downscaled_map = pygame.transform.scale(pygame.image.load(image_name), (32, 24))
# Scale the obstacle map to match the screen size
obstacle_map = pygame.transform.scale(obstacle_map, (screen_width, screen_height))
map_img = pygame.transform.scale(map_img, (screen_width, screen_height))
image_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "powerup_map.png")
powerup_map = pygame.transform.scale(pygame.image.load(image_name), (screen_width, screen_height))
# Set up initial sprite position
sprite_x = screen_width // 2 - sprite_width // 2
sprite_y = screen_height // 2 - sprite_height // 2 + 20

# Set up initial movement variables
move_left = False
move_right = False
is_jumping = False

# Set up physics variables
gravity = 0.2
vertical_velocity = 7.5
move_speed = 3
max_jumps = 2
# Game loop
running = True
player = Player(sprite_x, sprite_y)
image_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "enemy.png")
enemies = [[200, 200, [image_name]], [250, 250, [image_name]]]
level = Level(image=map_img, collision=downscaled_map, enemy_list=enemies, powerup_map=powerup_map)

while running:
    pass
    # Handle events

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move_left = True
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move_right = True
            elif event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
                is_jumping = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move_left = False
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move_right = False

    player.update_char(move_left, move_right, is_jumping)

    # Render the screen
    screen.fill((255, 255, 255))
    screen.blit(level.image, (0, 0))
    screen.blit(player.image, (player.rect.x, player.rect.y))
    for enemy in level.enemies:
        enemy.update()
        screen.blit(enemy.image, (enemy.rect.x, enemy.rect.y))
    for powerup in level.powerups:
        powerup.update()
        screen.blit(powerup.image, (powerup.rect.x, powerup.rect.y))
    coins_font = pygame.font.SysFont("system-ui", 24)
    cons_surface = coins_font.render("Coins: " + str(player.coins), False, (0, 0, 0))
    screen.blit(cons_surface, (10, 10))
    pygame.display.flip()
    is_jumping = False
# Quit the game
pygame.quit()
