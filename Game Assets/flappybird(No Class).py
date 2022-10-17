import random
import pygame
from pygame import mixer

pygame.init()

def game_floor():
    #print("score is building")
    screen.blit(floor_base,(floor_x_position,900))
    screen.blit(floor_base,(floor_x_position + 576,900))

def check_collision(pipes):
    # collision with pipes
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            die_sound.play()
            return False
    # check floor is not hit
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        die_sound.play()
        #print("HIT FLOOR")
        return False # to stop the game
        
    return True
def create_pipe():
    random_pipe_pos= random.choice(pipe_height) # Replace with random
    top_pipe= pipe_surface.get_rect(midbottom=(700,random_pipe_pos - 300))
    bottom_pipe= pipe_surface.get_rect(midtop=(700,random_pipe_pos))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -=5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe= pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe,pipe)

def bird_animation():
    new_bird = bird_imgs[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

screen= pygame.display.set_mode((576,1024))

# Vars
gravity= 0.25
bird_movement=0
score=0
pass_pipe= False
bird_index=0

# Background
background= pygame.image.load('background-day.png')
background= pygame.transform.scale2x(background)

# Floor base
floor_base= pygame.image.load('base.png')
floor_base= pygame.transform.scale2x(floor_base)
floor_x_position= 0

# Title and Icon
pygame.display.set_caption("Flappy Bird")
icon=pygame.image.load('001-angry-birds.png')
pygame.display.set_icon(icon)

# Bird
bird_img1= pygame.image.load('bluebird-1.png')
bird_img2= pygame.image.load('bluebird-2.png')
bird_img3= pygame.image.load('bluebird-3.png')
bird_imgs=[bird_img1,bird_img2,bird_img3]
bird_img= bird_imgs[bird_index]
bird_rect= bird_img.get_rect(center=(100,512))

BIRDFLAP= pygame.USEREVENT +1
pygame.time.set_timer(BIRDFLAP,150)

# Message
message= pygame.image.load('message.png')
message= pygame.transform.scale2x(message)
game_over_rect= message.get_rect(center=(288,512))

# Building Pipes
pipe_surface= pygame.image.load('pipe-green.png')
pipe_surface= pygame.transform.scale2x(pipe_surface)
pipe_list=[]
pipe_height= [400,600,800]

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)

flap_sound= pygame.mixer.Sound('audio_wing.wav')
die_sound = pygame.mixer.Sound('audio_hit.wav')

game_active= True

running= True
while running:
    screen.fill((0,0,0))

    screen.blit(background,(0,0))



    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            running= False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0 # ini yang buat twing twing
                bird_movement -= 7.5
                flap_sound.play()
                #bird_animation()
            if event.key == pygame.K_SPACE and game_active == False:
                bird_rect.center= (100,512)
                bird_movement= 0
                pipe_list.clear()
                game_active= True

        if event.type== SPAWNPIPE and game_active:# because we dont want the pipe still respawn when game over
            #print('pipe being created')
            pipe_list.extend(create_pipe())
            #print(pipe_list)
        if event.type== BIRDFLAP:
            if bird_index<2:
                bird_index +=1
            else:
                bird_index=0

            bird_img, bird_rect= bird_animation()

    # Create Floor
    floor_x_position -= 4
    game_floor()

    if game_active:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_img,bird_rect)
        # Draw pipes
        pipe_list=move_pipes(pipe_list)
        draw_pipes(pipe_list)
         # check for collsion
        game_active=check_collision(pipe_list)
    else:
        screen.blit(message, game_over_rect)



    if floor_x_position <=-576:
        floor_x_position=0


    pygame.display.update()