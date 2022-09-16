#The original code as well as the images and sounds come from https://www.youtube.com/watch?v=mFbdfXWmLU8&ab_channel=CodeXplore
#I've just optimized and balanced the game

import pygame
import sys
import random
from pygame.locals import * 

pygame.mixer.pre_init(frequency = 44100, size = -16, channels = 2, buffer = 512)

pygame.init()

# game's functions
def create_pipe():
    pipe_y_pos = random.choice(pipe_height)
    bot_pipe = pipe_surface.get_rect(midtop = (500,pipe_y_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500,(pipe_y_pos - 700)))
    return bot_pipe, top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            SCREEN.blit(pipe_surface, pipe)
        else:
            flipped_pipe = pygame.transform.flip(pipe_surface, False, True)
            SCREEN.blit(flipped_pipe, pipe)

def lose_condition(pipes):
    
    for pipe in pipes:
        if bird_pos.colliderect(pipe):
            die_sound.play()
            return False

    if bird_pos.centery >= 600 or bird_pos.centery <= 0:
        die_sound.play()
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_y_move*5, 1)
    return new_bird

def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_pos = new_bird.get_rect(center = (100, bird_pos.centery))
    return new_bird, new_bird_pos

def score_display(game_state):
    if game_state == 'running':
        score_surface = game_font_score.render(str(int(score)), True, WHITE)
        score_pos = score_surface.get_rect(center = (218, 100))
        SCREEN.blit(score_surface, score_pos)
    if game_state == 'game_over':
        score_surface = game_font_score.render('score: ' + str(int(score)), True, WHITE)
        score_pos = score_surface.get_rect(center = (218, 100))
        SCREEN.blit(score_surface, score_pos)

        high_score_surface = game_font_score.render('high score: '+ str(int(high_score)), True, WHITE)
        high_score_pos = high_score_surface.get_rect(center = (218, 540))
        SCREEN.blit(high_score_surface, high_score_pos)

        message = game_font_text.render("press 'space' to play again'", True, WHITE)
        message_pos = message.get_rect(center = (218, 585))
        SCREEN.blit(message, message_pos)

# set up the window
SCREEN = pygame.display.set_mode((432, 768))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
running = True
game_active = True
game_loop = False

WHITE = (255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)

# background
BACKGROUND = pygame.image.load('flappy_bird_background.png').convert()
BACKGROUND = pygame.transform.scale2x(BACKGROUND)

FLOOR = pygame.image.load('flappy_bird_floor.png').convert()
FLOOR = pygame.transform.scale2x(FLOOR)
floor_x_pos = 0

start_screen = pygame.image.load('start_screen.png').convert_alpha()
start_screen = pygame.transform.scale2x(start_screen)
start_screen_pos = start_screen.get_rect(center = (216, 384))

game_font_score = pygame.font.Font('04B_19.TTF', 36)
game_font_text = pygame.font.Font('04B_19.TTF', 28)

game_over_screen = pygame.image.load('game_over.png').convert_alpha()
game_over_screen = pygame.transform.scale2x(game_over_screen)
game_over_screen_pos = game_over_screen.get_rect(center = (216, 300))

# set up the game play
bird_up = pygame.image.load('yellowbird_upflap.png').convert_alpha()
bird_up = pygame.transform.scale(bird_up, (59.5, 42))
bird_mid = pygame.image.load('yellowbird_midflap.png').convert_alpha()
bird_mid = pygame.transform.scale(bird_mid, (59.5, 42))
bird_down = pygame.image.load('yellowbird_downflap.png').convert_alpha()
bird_down = pygame.transform.scale(bird_down, (59.5, 42))
bird_list = [bird_up, bird_mid, bird_down]
bird_index = 0
bird = bird_list[bird_index]
bird_pos = bird.get_rect(center=(100, 300))

bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 200)

gravity = 0.125
bird_y_move = 2

pipe_surface = pygame.image.load('Green_pipe.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [250, 300, 325, 350, 375, 400]

pipe_spawn = pygame.USEREVENT
pygame.time.set_timer(pipe_spawn, 1200)

score = 0
high_score = 0

# sound
flap_sound = pygame.mixer.Sound('sfx_wing.wav')
die_sound = pygame.mixer.Sound('sfx_die.wav')
score_sound = pygame.mixer.Sound('sfx_point.wav')
score_count = 1

# main loop
while running:
    # background
    SCREEN.blit(BACKGROUND, (0, 0))
    SCREEN.blit(start_screen, start_screen_pos)

    # game events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                start_screen.fill(TRANSPARENT)
                game_loop = True
        if game_loop:
            if event.type == KEYDOWN:
                if event.key == K_SPACE and game_active == True:
                    bird_y_move = -5
                    flap_sound.play()
                if event.key == K_SPACE and game_active == False:
                    game_active = True
                    pipe_list.clear()
                    bird_pos.center = (100, 300)
                    bird_y_move = 0
                    score = 0
            if event.type == pipe_spawn:
                pipe_list.extend(create_pipe())
            if event.type == bird_flap:
                if bird_index < 2:
                    bird_index += 1
                else:
                    bird_index = 0
                bird, bird_pos = bird_animation()

    if game_loop:
        # game play
        if score > high_score:
            high_score = score
        if game_active:
            # the bird
            bird_y_move += gravity
            rotated_bird = rotate_bird(bird)
            bird_pos.centery += bird_y_move
            SCREEN.blit(rotated_bird, bird_pos)
            game_active = lose_condition(pipe_list)

            # the pipes
            draw_pipe(pipe_list)
            pipe_list = move_pipe(pipe_list)

            # score
            score += 0.01
            score_display('running')
            score_count -= 0.01
            if score_count <= 0:
                score_sound.play()
                score_count = 1
        else:
            score_display('game_over')
            SCREEN.blit(game_over_screen, game_over_screen_pos)

    # the floor
    floor_x_pos -= 1
    if floor_x_pos <= -432:
        floor_x_pos = 0
    SCREEN.blit(FLOOR, (floor_x_pos, 600))
    SCREEN.blit(FLOOR, (floor_x_pos + 432, 600))

    pygame.display.update()
    clock.tick(120)
