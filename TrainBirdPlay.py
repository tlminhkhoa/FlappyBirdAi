import pygame  
import sys
import os
import random
import pickle
from NN import NeuralNetWork

scale_down = 0.765625
gravity = 0.25*scale_down
pipe_spawn_time = 1700
clock_tick = 120

def drawBox():
    screen.blit(floor_surface,(floor_x,700))
    screen.blit(floor_surface,(floor_x + 576*scale_down,700))
def create_pipe():
    random_pipe_pos = (random.randint(3,5)*100)
    bottom_pipe = pip_surface.get_rect(midtop = (700,random_pipe_pos))
    top_pipe = pip_surface.get_rect(midbottom = (700,random_pipe_pos - 150))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5*scale_down

    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom > dimension[1]:
            screen.blit(pip_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pip_surface,False,True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird.rect.colliderect(pipe):
            return False

    if bird.rect.top <= -50 or bird.rect.bottom >= 700:
        return False
    return True

def rotate_bird(bird):
    return pygame.transform.rotozoom(bird.surface,-bird.movement * 3,1)

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird,new_bird_rect

def score_display(game_state):

    if game_state == "main_state":
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (220,92))
        screen.blit(score_surface,score_rect)

    if game_state == "game_over":
        score_surface = game_font.render(f"Score: {(int(score))}",True,(255,255,255))
        score_rect = score_surface.get_rect(center = (220,92))
        screen.blit(score_surface,score_rect)

def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score
def apple_scale_down(Intuple):
    return (int(Intuple[0]*scale_down),int(Intuple[1]*scale_down))
        
def get_size_scale_surface(surface):
    return apple_scale_down((surface.get_width(), surface.get_height()))

def closest_pipe(pip_list):
    closest = 1000
    closestpipes = []
    currentID = 0
    if pip_list == []:
        return False
    for Ipipe in range(len(pip_list)):
        current = abs(pip_list[Ipipe].centerx - 36)
        if  current < closest and pip_list[Ipipe].centerx > 36 :
            closest = current
            currentID = Ipipe
    closestpipes.append(pip_list[currentID] )
    closestpipes.append(pip_list[currentID + 1] )
    return closestpipes


class Bird:
    def __init__(self,id):
        colorBird = ["assets/bluebird-midflap.png","assets/redbird-midflap.png", "assets/yellowbird-midflap.png"]
        self.surface = pygame.image.load(random.choice(colorBird)).convert_alpha()
        self.surface = pygame.transform.scale(self.surface,(51, 36))
        self.rect = self.surface.get_rect(center = (76,392))
        self.movement = 0
        self.brain = NeuralNetWork(5,2,1,6)
        self.id = id
        self.status = True
        self.score = score
        self.mutate = False
    def falldown(self):
        self.rect.centery += self.movement
    def think(self):

        closestpipes = closest_pipe(pip_list)
        if not closestpipes:
            return False
        distToPipe = (closestpipes[0].centerx - self.rect.centerx )/ 600
        distToBottom = (closestpipes[0].centery - self.rect.centery )/ 784
        distToTop =  (closestpipes[1].centery - self.rect.centery )/ 784
        yCoordinate = self.rect.centery/  784
        BrainInput = [distToPipe,distToBottom,distToTop,yCoordinate,self.movement/10] 

        self.brain.forwardPropagation(BrainInput)
        return True
    def jump(self):
        if not self.think():
            return
        if self.brain.output[0][0] > self.brain.output[0][1]:
            newevent = pygame.event.Event(BIRDJUMP, message = self.id) #create the event
            pygame.event.post(newevent)


os.chdir("D:\Study\Machine Learning\Flappy bird")

pygame.mixer.pre_init(frequency = 44100 ,size = 16 ,channels = 1, buffer = 512)
pygame.init()

dimension = apple_scale_down((576,1024))
screen = pygame.display.set_mode(dimension)
clock = pygame.time.Clock()
game_font = pygame.font.Font("./Fonts/04B_19__.TTF",40)



# Variable
game_active = True
score = 0
high_score = 0
BIRDJUMP = pygame.USEREVENT

with (open("trainBird.pkl", "rb")) as openfile:
    BirdBrain = pickle.load(openfile)
bird = Bird(1)
bird.brain = BirdBrain

bg_suface = pygame.image.load("assets/background-day.png").convert()
bg_suface = pygame.transform.scale2x(bg_suface)

floor_surface = pygame.image.load("assets/base.png").convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x = 0 


bird_downflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-downflap.png").convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-midflap.png").convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-upflap.png").convert_alpha())
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,512))
BIRDFLAP = pygame.USEREVENT + 2
pygame.time.set_timer(BIRDFLAP,200)


pip_surface = pygame.image.load("assets/pipe-green.png").convert()
pip_surface = pygame.transform.scale2x(pip_surface)
pip_list = []
SPAWNPIPE = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNPIPE,pipe_spawn_time)

game_over_surface = pygame.transform.scale2x(pygame.image.load("assets/message.png").convert_alpha())
game_over_rect = game_over_surface.get_rect(center = apple_scale_down((288,512)))


flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
death_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
score_sound = pygame.mixer.Sound("sound/sfx_point.wav")
score_sound_countdown = 100
pip_list.extend(create_pipe())


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_UP and game_active:
            #     bird_movement = 0
            #     bird_movement -= 10
            #     flap_sound.play()
            if event.key == pygame.K_UP and game_active == False:
                game_active = True
                pip_list.clear()
                bird_rect.center = (100,512)
                bird_movement = 0
                score = 0 
        if event.type == BIRDJUMP:
            bird.movement = 0
            bird.movement -= 6
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
        bird.movement += gravity
        rotated = rotate_bird(bird)
        bird.falldown()
        screen.blit(rotated,bird.rect)
        game_active = check_collision(pip_list)
        bird.jump()
        bird.score = score

        #Pipes
        pip_list = move_pipes(pip_list)
        draw_pipes(pip_list)
        
        score += 0.01
        score_display("main_state")
        # score_sound_countdown -= 1
        # if score_sound_countdown <= 0:
            # score_sound.play()
            # score_sound_countdown = 100    
    else:
        # print("else")
        # screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display("game_over")
        



    #Floor
    floor_x = floor_x - 1 
    if floor_x < -(576*scale_down) :
        floor_x = 0 
    drawBox()
    
    check_collision(pip_list)
    
    pygame.display.update()
    clock.tick(clock_tick)