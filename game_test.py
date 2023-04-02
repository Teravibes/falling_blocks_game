import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 1024
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Blocks")

# Set up the clock
clock = pygame.time.Clock()

# Game object class that accepts images
class GameObject:
    def __init__(self, x, y, width, height, color=None, image=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.image = image
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        elif self.color:
            pygame.draw.rect(screen, self.color, self.rect)

# Create the paddle
PADDLE_WIDTH = 500
PADDLE_HEIGHT = 80

def scale_image(image, max_width, max_height, allow_upscale=True):
    width, height = image.get_size()
    aspect_ratio = width / height

    if width > max_width or (allow_upscale and width < max_width):
        width = max_width
        height = int(width / aspect_ratio)

    if height > max_height or (allow_upscale and height < max_height):
        height = max_height
        width = int(height * aspect_ratio)

    return pygame.transform.scale(image, (width, height))



# Load the minecart image
minecart_image = pygame.image.load('minecart.png')

# Scale the minecart image while preserving its aspect ratio
minecart_image = scale_image(minecart_image, PADDLE_WIDTH, PADDLE_HEIGHT)

# Update the paddle dimensions to match the scaled image
PADDLE_WIDTH, PADDLE_HEIGHT = minecart_image.get_size()

# Create the paddle with the minecart image
paddle = GameObject(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - PADDLE_HEIGHT * 2, PADDLE_WIDTH, PADDLE_HEIGHT, image=minecart_image)

# Load the background image
background_image = pygame.image.load('background.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))



# Create the blocks
BLOCK_WIDTH = 60
BLOCK_HEIGHT = 60
blocks = []

# Create power-up blocks list
power_up_blocks = []

# Initialize speed boost variables
speed_boost_remaining = 0
speed_boost_duration = 10  # Duration in seconds

# Load the block image
block_image = pygame.image.load('block.png')
block_image = pygame.transform.scale(block_image, (BLOCK_WIDTH, BLOCK_HEIGHT))

# Load the power-up block image
power_up_block_image = pygame.image.load('power_up_block.png')
power_up_block_image = pygame.transform.scale(power_up_block_image, (BLOCK_WIDTH, BLOCK_HEIGHT))


# Load the freezing block image
freezing_block_image = pygame.image.load('freezing_block.png')
freezing_block_image = pygame.transform.scale(freezing_block_image, (BLOCK_WIDTH, BLOCK_HEIGHT))

# Create freezing blocks list
freezing_blocks = []

# Initialize freeze variables
freeze_duration = 5  # Duration in seconds
freeze_remaining = 0

def create_block():
    x = random.randint(0, WIDTH - BLOCK_WIDTH)
    y = -BLOCK_HEIGHT

    block_type = random.random()

    if block_type < 0.1:  # 10% chance to create a power-up block
        block = GameObject(x, y, BLOCK_WIDTH, BLOCK_HEIGHT, image=power_up_block_image)
        power_up_blocks.append(block)
    elif block_type < 0.2:  # 10% chance to create a freezing block
        block = GameObject(x, y, BLOCK_WIDTH, BLOCK_HEIGHT, image=freezing_block_image)
        freezing_blocks.append(block)
    else:
        block = GameObject(x, y, BLOCK_WIDTH, BLOCK_HEIGHT, image=block_image)
        blocks.append(block)



create_block()

# Initialize the score
score = 0

# Set up a font for displaying the score
font = pygame.font.Font(None, 36)

timer_font = pygame.font.Font(None, 36)
timer_text = None
freeze_timer_text = None


# Falling speed
falling_speed = 100  # Pixels per second

# Game loop
while True:
    dt = clock.tick(60) / 1000  # Delta time, in seconds

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # # User input
    keys = pygame.key.get_pressed()
    
    if freeze_remaining <= 0:
        if keys[pygame.K_LEFT]:
            paddle.x -= paddle_speed * dt
        if keys[pygame.K_RIGHT]:
            paddle.x += paddle_speed * dt
    else:
        freeze_remaining -= dt


    # Keep the paddle within the screen bounds
    paddle.x = max(0, min(WIDTH - PADDLE_WIDTH, paddle.x))

    # Update the paddle's rect
    paddle.rect.x = paddle.x

    # Update the freezing blocks
    for block in freezing_blocks:
        block.y += falling_speed * dt
        block.rect.y = block.y

        # Check for collisions with the paddle
        if block.rect.colliderect(paddle.rect):
            freezing_blocks.remove(block)
            create_block()
            freeze_remaining = freeze_duration

        # Check if the block has reached the bottom of the screen
        if block.y > HEIGHT:
            freezing_blocks.remove(block)
            create_block()


    # Update the blocks
    for block in blocks:
        block.y += falling_speed * dt
        block.rect.y = block.y

        # Check for collisions with the paddle
        if block.rect.colliderect(paddle.rect):
            blocks.remove(block)
            create_block()
            score += 10  # Increase the score

        # Check if the block has reached the bottom of the screen
        if block.y > HEIGHT:
            blocks.remove(block)
            create_block()

    # Update the power-up blocks
    for block in power_up_blocks:
        block.y += falling_speed * dt
        block.rect.y = block.y

        # Check for collisions with the paddle
        if block.rect.colliderect(paddle.rect):
            power_up_blocks.remove(block)
            create_block()
            speed_boost_remaining = speed_boost_duration

        # Check if the block has reached the bottom of the screen
        if block.y > HEIGHT:
            power_up_blocks.remove(block)
            create_block()

    # Clear the screen by drawing the background image
    screen.blit(background_image, (0, 0))

    # Draw game objects
    paddle.draw(screen)
    for block in blocks:
        block.draw(screen)

    # Draw the power-up blocks
    for block in power_up_blocks:
        block.draw(screen)

    # Draw the freezing blocks
    for block in freezing_blocks:
        block.draw(screen)

     # Draw the score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    # Update and draw the speed boost timer
    if speed_boost_remaining > 0:
        timer_text = timer_font.render(f"Power-up: {int(speed_boost_remaining)}s", True, (255, 255, 255))
        screen.blit(timer_text, (10, 10))

    # Update and draw the freeze timer
    if freeze_remaining > 0:
        freeze_timer_text = timer_font.render(f"Freeze: {int(freeze_remaining)}s", True, (255, 255, 255))
        screen.blit(freeze_timer_text, (WIDTH // 2 - freeze_timer_text.get_width() // 2, 10))


    # Update the falling speed based on the score
    falling_speed = 100 + (score // 50) * 20

    # Update the paddle's speed based on the speed boost remaining time
    paddle_speed = 300
    if speed_boost_remaining > 0:
        paddle_speed *= 2  # Double the paddle speed
        speed_boost_remaining -= dt


    # Update the display
    pygame.display.flip()

