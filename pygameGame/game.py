import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Physics-based Game")

# Load sprite image and obstacle map
sprite_image = pygame.image.load("thecircle.jpg")
sprite_image = pygame.transform.scale(sprite_image, (30, 30))
obstacle_map = pygame.image.load("obstacle_map.png")

# Get sprite and obstacle map dimensions
sprite_width, sprite_height = sprite_image.get_size()
obstacle_width, obstacle_height = obstacle_map.get_size()

# Scale the obstacle map to match the screen size
obstacle_map = pygame.transform.scale(obstacle_map, (screen_width, screen_height))

# Set up initial sprite position
sprite_x = screen_width // 2 - sprite_width // 2
sprite_y = screen_height // 2 - sprite_height // 2 + 20

# Set up initial movement variables
move_left = False
move_right = False
is_jumping = False
jump_count = 10

# Set up physics variables
gravity = 6
vertical_velocity = 60
move_speed = 20
max_jumps = 2
# Game loop
running = True
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [pygame.image.load("thecircle.jpg")]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.jump_count = 0
        self.frame = 0
        self.vel_x = 0
        self.vel_y = 0
        self.jump_speed = vertical_velocity

    def check_collision(self, direction):
        # true: horizontal, false: vertical
        # Check for collisions with obstacles
        if direction:
            sprite_rect = pygame.Rect(self.rect.x + self.vel_x, self.rect.y, sprite_width, sprite_height)
            collision = sprite_rect.collidelistall(
                [
                    pygame.Rect(x, y, 1, 1)
                    for x in range(screen_width)
                    for y in range(screen_height)
                    if obstacle_map.get_at((x, y)) == (0, 0, 0)
                ]
            )

            return collision
        else:
            sprite_rect = pygame.Rect(self.rect.x, self.rect.y + self.vel_y, sprite_width, sprite_height)
            collision = sprite_rect.collidelistall(
                [
                    pygame.Rect(x, y, 1, 1)
                    for x in range(screen_width)
                    for y in range(screen_height)
                    if obstacle_map.get_at((x, y)) == (0, 0, 0)
                ]
            )

            return collision

    def update_char(self, left, right, jump):
        # Jumping logic
        if jump:
            if self.jump_count <= max_jumps:
                self.vel_y = -self.jump_speed
                self.jump_count += 1
            elif self.vel_y == 0:
                self.vel_y = -self.jump_speed
                self.jump_count = 1
        if self.vel_y < 0:
            self.vel_y *= 0.88
        else:
            self.vel_y *= 1.01
        self.vel_y += gravity

        collision_h = self.check_collision(True)
        collision_v = self.check_collision(False)
        # ahh yes, python syntax
        if left:
            self.vel_x = -move_speed
        elif right:
            self.vel_x = move_speed
        else:
            self.vel_x = 0
        if collision_h:
            self.vel_x = 0
        else:
            self.rect.x += self.vel_x
        if collision_v:
            self.vel_y = 0
        else:
            self.rect.y += self.vel_y

        print(self.vel_x, self.vel_y, self.rect.x, self.rect.y)


player = Player(200, 200)

while running:
    # Handle events
    is_jumping = False
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            elif event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_SPACE and not is_jumping:
                is_jumping = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False
    print(move_left, move_right, is_jumping)
    player.update_char(move_left, move_right, is_jumping)

    # Render the screen
    screen.fill((255, 255, 255))
    screen.blit(obstacle_map, (0, 0))
    screen.blit(sprite_image, (player.rect.x, player.rect.y))

    pygame.display.flip()

# Quit the game
pygame.quit()
