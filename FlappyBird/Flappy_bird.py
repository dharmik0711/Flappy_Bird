import pygame
from pygame.locals import *
import random

# Initialize Pygame
pygame.init()

# Display dimensions
display_width = 400
display_height = 650
game_on = True

# Initialize score variables
score = 0
high_score = 0
gravity = 0.33
bird_movement = 0

# Set up the display
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("My game")

# Load images
base = pygame.image.load('base.png').convert()
pipes_list = ['green.jpg', 'red_transparent.png']
pipe_surface = pygame.image.load(random.choice(pipes_list)).convert_alpha()
pipe_height = [150, 250, 350]

# Bird setup
bird_sur = pygame.image.load('download.png').convert_alpha()
bird_sur = pygame.transform.scale(bird_sur, (50, 40))
bird_rectangle = bird_sur.get_rect(center=(100, 325))

pipe_surface = pygame.transform.scale(pipe_surface, (50, 300))

# Background setup
Background = pygame.image.load('bgg.jpg').convert()
Background = pygame.transform.scale(Background, (display_width, display_height))

# Set up clock and timer for pipes
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1300)

# Initialize variables for base and pipes
base_x_pos = 0
pipes_list2 = []

# Set up font for displaying score
font = pygame.font.Font('Evil_Empire.otf', 50)

def adding_pipes():
    random_pipe_height = random.choice(pipe_height)
    base_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_height + 100))
    top_pipe = pipe_surface.get_rect(midbottom=(500, random_pipe_height - 100))
    return base_pipe, top_pipe

def pipes_move(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return [pipe for pipe in pipes if pipe.right > 0]

def show_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 510:
            game_display.blit(pipe_surface, pipe)
        else:
            reverse_pipe = pygame.transform.flip(pipe_surface, False, True)
            game_display.blit(reverse_pipe, pipe)

def collision(pipes):
    for pipe in pipes:
        if bird_rectangle.colliderect(pipe):
            return False
    if bird_rectangle.top <= -25 or bird_rectangle.bottom >= 550:
        return False   
    return True

def base_move():
    game_display.blit(base, (base_x_pos, 550))
    game_display.blit(base, (base_x_pos + 285, 550))

def event_handler():
    global pipes_list2, base_x_pos, bird_movement, game_on, score
    
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q)):
            pygame.quit()
            quit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_on:
                    bird_movement = -9  # Move bird up
                else:
                    # Reset the game
                    pipes_list2.clear()
                    game_on = True
                    bird_movement = 0
                    bird_rectangle.center = (100, 325)  # Reset bird position
                    score = 0  # Reset score

        if event.type == pygame.USEREVENT:
            pipes_list2.extend(adding_pipes())

while True:
    event_handler()

    if game_on:
        base_x_pos -= 1
        if base_x_pos <= -285:
            base_x_pos = 0

        pipes_list2 = pipes_move(pipes_list2)

        game_display.blit(Background, (0, 0))
        show_pipes(pipes_list2)
        
        bird_rectangle.centery += bird_movement
        bird_movement += gravity
        
        base_move()
        game_display.blit(bird_sur, bird_rectangle)

        # Check for collision
        if not collision(pipes_list2):
            game_on = False  # Stop the game if a collision occurs
        else:
            # Increment score if the bird has passed a pipe
            for pipe in pipes_list2:
                if pipe.centerx == bird_rectangle.centerx:  # Check if bird passed the pipe
                    score += 1

        if score > high_score:
            high_score = score

        # Display score on the screen
        score_surface = font.render(f'Score: {score}', True, (0, 0, 0))  # White color
        game_display.blit(score_surface, (10, 10))  # Draw score at the top left corner
        
        high_score_surface = font.render(f'High Score: {high_score}', True, (0, 0, 0))  # White color
        game_display.blit(high_score_surface, (display_width / 3.3, display_height - 50))  # Draw high score at the bottom

        pygame.display.update()
        clock.tick(60)
