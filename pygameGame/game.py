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
sprite_y = screen_height // 2 - sprite_height // 2

# Set up initial movement variables
move_left = False
move_right = False
is_jumping = False
jump_count = 10

# Set up physics variables
gravity = 0.5
vertical_velocity = 0

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
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

    # Apply gravity
    vertical_velocity += gravity

    # Update sprite position based on movement
    if move_left:
        sprite_x -= 5
    elif move_right:
        sprite_x += 5

    # Jumping logic
    if is_jumping:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            sprite_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = 10

    # Check for collisions with obstacles
    sprite_rect = pygame.Rect(sprite_x, sprite_y, sprite_width, sprite_height)
    collision = sprite_rect.collidelistall(
        [
            pygame.Rect(x, y, 1, 1)
            for x in range(screen_width)
            for y in range(screen_height)
            if obstacle_map.get_at((x, y)) == (0, 0, 0)
        ]
    )

    # Handle collisions
    if collision:
        # Handle collision with obstacles
        sprite_x, sprite_y = sprite_rect.x, sprite_rect.y
        vertical_velocity = 0

    # Update sprite position vertically
    sprite_y += vertical_velocity

    # Render the screen
    screen.fill((255, 255, 255))
    screen.blit(obstacle_map, (0, 0))
    screen.blit(sprite_image, (sprite_x, sprite_y))

    pygame.display.flip()
    clock.tick(60)

# Quit the game
pygame.quit()
