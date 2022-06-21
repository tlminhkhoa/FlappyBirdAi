import pygame  
import sys
import os
import random
import copy
from NN import NeuralNetWork
import pickle
import json
os.chdir("D:\Study\Machine Learning\Flappy bird")
def drawBox():
    screen.blit(floor_surface,(floor_x,700))
    screen.blit(floor_surface,(floor_x + 576*scale_down,700))

def create_pipe():
    random_pipe_pos = (random.randint(3,6)*100)
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

def check_collision(pipes,bird):
    for pipe in pipes:
        if bird.rect.colliderect(pipe):
            return False

    if bird.rect.top <= -50 or bird.rect.bottom >= 700:
        return False
    return True

def rotate_bird(bird):
    return pygame.transform.rotozoom(bird.surface,-bird.movement * 3,1)


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
        distToPipe = (closestpipes[0].centerx - self.rect.centerx )/ 600
        distToBottom = (closestpipes[0].centery - self.rect.centery )/ 784
        distToTop =  (closestpipes[1].centery - self.rect.centery )/ 784
        yCoordinate = self.rect.centery/  784
        BrainInput = [distToPipe,distToBottom,distToTop,yCoordinate,self.movement/10] 

        self.brain.forwardPropagation(BrainInput)
        return 
    def jump(self):
        self.think()
        if self.brain.output[0][0] > self.brain.output[0][1]:
            newevent = pygame.event.Event(BIRDJUMP, message = self.id) #create the event
            pygame.event.post(newevent)


def generate_clone(bestBird,n):
    flock = []
    for id in range(n):
        newBird = Bird(id)
        brain_structure = copy.deepcopy(bestBird.brain.denes_layers)
        newBird.brain.constructFromSameDenses(brain_structure)
        # newBird.brain.weightMutation(0.5)
        flock.append(newBird)
    return flock


def bestBirdsReturn(flock):
    sortedFlock = sorted(flock, key=lambda bird: bird.score, reverse=True)
    return sortedFlock[:10]

def generate_new_generation_crossover(flock):
    newflock = []
    bestbirds = bestBirdsReturn(flock)
    for bird in bestbirds:
        newflock.append(generate_clone(bird,10))
    
 
    for i in range(len(newflock)):
        newflock[i][0].mutate = True

    

    m = 0
    for i in range(len(newflock)):
        m = i + 1
        for j in range(len(newflock[0])):
            if newflock[i][j].mutate == False:
                k = searchUnmutatedBird(newflock[m])
                newflock[i][j].brain.crossOverNN(0.4,newflock[m][k].brain)
                newflock[i][j].mutate = True
                newflock[m][k].mutate = True
                
                # print("pair i,j",i,j)
                # print("pair m,k",m,k)
                m += 1

    # try to reserve the original bird
    for i in range(len(newflock)):
        newflock[i][0].mutate = False

    newflock = [item for sublist in newflock for item in sublist]
    
    # here
    for bird in newflock:
        if bird.mutate == True:
            bird.brain.weightMutation(0.3)
        
    
    GiveId = 0
    for bird in newflock:
        bird.id = GiveId
        GiveId += 1

    # print("len",len(newflock))
    return newflock


def searchUnmutatedBird(gen):
    for j in range(len(gen)):
        if gen[j].mutate == False:
            return j

        

    
    

pygame.mixer.pre_init(frequency = 44100 ,size = 16 ,channels = 1, buffer = 512)
pygame.init()

scale_down = 0.765625

dimension = apple_scale_down((576,1024))
# print(dimension)
screen = pygame.display.set_mode(dimension)
clock = pygame.time.Clock()
game_font = pygame.font.Font("04B_19__.TTF",40)


# Variable
gravity = 0.25*scale_down
game_active = True
score = 0
high_score = 0
BIRDJUMP = pygame.USEREVENT 

bg_suface = pygame.image.load("assets/background-day.png").convert()
bg_suface = pygame.transform.scale2x(bg_suface)

floor_surface = pygame.image.load("assets/base.png").convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x = 0 

flock = []
numberOfBirds = 100
for id in range(numberOfBirds):
    flock.append(Bird(id))
    
# bird = Bird(1)



pip_surface = pygame.image.load("assets/pipe-green.png").convert()
pip_surface = pygame.transform.scale2x(pip_surface)
pip_list = []
SPAWNPIPE = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNPIPE,870)

game_over_surface = (pygame.image.load("assets/message.png").convert_alpha())
game_over_surface = pygame.transform.scale(game_over_surface,(276,400))
game_over_rect = game_over_surface.get_rect(center = apple_scale_down((288,512)))


flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
death_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
score_sound = pygame.mixer.Sound("sound/sfx_point.wav")
score_sound_countdown = 100
pip_list.extend(create_pipe())

gen = 0

bestScores = []
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            bestScore = 0
            for bird in flock:
                if bird.score > bestScore:
                    bestScore = bird.score
                    bestBird = bird
            with open('trainBird.pkl', 'wb') as output:
                pickle.dump(bestBird.brain, output, pickle.HIGHEST_PROTOCOL)
            

            with open('scores.txt', 'w') as f:
                f.write(json.dumps(bestScores))

            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_active:
                bird.movement = 0
                bird.movement -= 6
                

        if event.type == BIRDJUMP:
            for bird in flock:
                if bird.id == event.message:
                
                    bird.movement = 0
                    bird.movement -= 6

        if event.type == SPAWNPIPE and game_active :
            pip_list.extend(create_pipe())
            if len(pip_list) > 6:
                del pip_list[0]
                del pip_list[1]    

    screen.blit(bg_suface,(0,0))
    
    countBirdSurvived = 0
    
    listBirdStatus = [] 
    if game_active:
        #Bird
        for bird in flock:
            listBirdStatus.append(bird.status)
            if bird.status and pip_list: 
                bird.jump()
                bird.movement += gravity
                rotated = rotate_bird(bird)
                bird.falldown()
                screen.blit(rotated,bird.rect)
                bird.status = check_collision(pip_list,bird)
                bird.score = score
        
        if pip_list:
        #Pipes
    
            pip_list = move_pipes(closest_pipe(pip_list))
            draw_pipes(closest_pipe(pip_list))
            

            score += 0.01
            score_display("main_state")
            score_sound_countdown -= 1
            if score_sound_countdown <= 0:
                score_sound_countdown = 100  
        
        if not any(listBirdStatus):
            game_active = False
    else:
        bestScore = 0
        for bird in flock:
            if bird.score > bestScore:
                bestScore = bird.score
                bestBird = bird
        bestScores.append(bestScore)
        print(bestScore)
       

        flock = generate_new_generation_crossover(flock)
        gen = gen + 1
        print("generation", gen)

        
        score = 0 
        game_active = True
        pip_list.clear()
        
        


    
    #Floor
    floor_x = floor_x - 1 
    if floor_x < -(576*scale_down) :
        floor_x = 0 
    drawBox()
    
    
    pygame.display.update()
    clock.tick(120)
