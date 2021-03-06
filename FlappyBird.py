import pygame  
import sys
import os
import random
def drawBox():
    screen.blit(floor_surface,(floor_x,900))
    screen.blit(floor_surface,(floor_x + 576,900))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pip_surface.get_rect(midtop = (700,random_pipe_pos))
    top_pipe = pip_surface.get_rect(midbottom = (700,random_pipe_pos - 300))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5

    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom > 1024:
            screen.blit(pip_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pip_surface,False,True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    # print("true")
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            # death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird,new_bird_rect

def score_display(game_state):

    if game_state == "main_state":
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)

    if game_state == "game_over":
        score_surface = game_font.render(f"Score: {(int(score))}",True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f"Score: {int(high_score)}",True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (288,850))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score


os.chdir("D:\Study\Machine Learning\Flappy bird")

pygame.mixer.pre_init(frequency = 44100 ,size = 16 ,channels = 1, buffer = 512)
pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font("04B_19__.TTF",40)


# Variable
gravity = 0.25
bird_movement = 0
pipe_height = [400,600,800]
game_active = True
score = 0
high_score = 0



bg_suface = pygame.image.load("assets/background-day.png").convert()
bg_suface = pygame.transform.scale2x(bg_suface)

floor_surface = pygame.image.load("assets/base.png").convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x = 0 


# bird_surface = pygame.image.load("assets/bluebird-midflap.png").convert_alpha()
# bird_surface = pygame.transform.scale2x(bird_surface)
# bird_rect = bird_surface.get_rect(center = (100,512))

bird_downflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-downflap.png").convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-midflap.png").convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-upflap.png").convert_alpha())
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,512))
BIRDFLAP = pygame.USEREVENT +1 
pygame.time.set_timer(BIRDFLAP,200)


pip_surface = pygame.image.load("assets/pipe-green.png").convert()
pip_surface = pygame.transform.scale2x(pip_surface)
pip_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)

game_over_surface = pygame.transform.scale2x(pygame.image.load("assets/message.png").convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288,512))


flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
death_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
score_sound = pygame.mixer.Sound("sound/sfx_point.wav")
score_sound_countdown = 100

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_active:
                bird_movement = 0
                bird_movement -= 10
                flap_sound.play()
            if event.key == pygame.K_UP and game_active == False:
                game_active = True
                pip_list.clear()
                bird_rect.center = (100,512)
                bird_movement = 0
                score = 0 
        if event.type == SPAWNPIPE:
            pip_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            
            bird_surface,bird_rect = bird_animation()
    
    
    screen.blit(bg_suface,(0,0))
    
    # print(game_active)
    if game_active:
        game_active = check_collision(pip_list)
        #Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)

        #Pipes
        pip_list = move_pipes(pip_list)
        draw_pipes(pip_list)

        score += 0.01
        score_display("main_state")
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100    
    else:
        # print("else")
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display("game_over")
        



    #Floor
    floor_x = floor_x - 1 
    if floor_x < -576 :
        floor_x = 0 
    drawBox()
    
    check_collision(pip_list)
    
    pygame.display.update()
    clock.tick(120)