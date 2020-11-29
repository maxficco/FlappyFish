import pygame, sys, random


def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,450))
    screen.blit(floor_surface,(floor_x_pos+288,450))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (350,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (350,random_pipe_pos-150))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flipped_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flipped_pipe, pipe)
def check_collison(pipes):
    for pipe in pipes:
        if birdbox.colliderect(pipe):
            death_sound.play()
            return False
    if birdbox.top < 0 or birdbox.bottom > 512:
        death_sound.play()
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50, birdbox.centery))
    return new_bird, new_bird_rect
def score_display(game_state):

    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (144,100))
        screen.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render("Score: " + str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (144,100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render("High Score: " + str(int(high_score)), True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (144,425))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.mixer.pre_init(frequency = 44100, size = 32, channels = 1, buffer = 1028)

pygame.init()
pygame.display.set_caption("Flappy Fish - by Max Ficco")
screen = pygame.display.set_mode((288,512))
clock = pygame.time.Clock()
game_font = pygame.font.Font("assets/04b_19.ttf",20)


# Game Variables
gravity = 0.125
bird_movement = 0
game_active = False 
score = 0
high_score = 0


bg_surface = pygame.image.load("assets/background-day.png").convert()
floor_surface = pygame.image.load("assets/base.png").convert()
floor_x_pos = 0

bird_downflap = pygame.image.load("assets/fish-downflap.png").convert_alpha()
bird_midflap = pygame.image.load("assets/fish-midflap.png").convert_alpha()
bird_upflap = pygame.image.load("assets/fish-upflap.png").convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
birdbox = bird_surface.get_rect(center = (50,256))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)


pipe_surface =  pygame.image.load("assets/pipe-green.png")
pipe_list = [] 
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [200,300,400]

game_over_surface = pygame.image.load("assets/message.png").convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (144, 256))

INCSCORE = pygame.USEREVENT
pygame.time.set_timer(INCSCORE,1200)


flap_sound = pygame.mixer.Sound("sounds/sfx_wing.wav")
death_sound = pygame.mixer.Sound("sounds/sfx_hit.wav")
score_sound = pygame.mixer.Sound("sounds/sfx_point.wav")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_SPACE) and game_active:
                bird_movement = 0
                bird_movement -= 4.5
                flap_sound.play()
            if (event.key == pygame.K_UP or event.key == pygame.K_SPACE) and game_active == False:
                game_active = True
                pipe_list = []
                birdbox = bird_surface.get_rect(center = (50,256))
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index +=1
            else:
                bird_index = 0
            bird_surface,birdbox = bird_animation()
        if event.type == INCSCORE and game_active:
            score_sound.play()
            score += 1
        if event.type == pygame.MOUSEBUTTONUP and game_active: 
            bird_movement = 0
            bird_movement -= 4
            flap_sound.play()
        if event.type == pygame.MOUSEBUTTONUP and game_active == False:
            game_active = True
            pipe_list = []
            birdbox = bird_surface.get_rect(center = (50,256))
            bird_movement = 0
            score = 0
    
    # Background
    screen.blit(bg_surface,(0,0))
    # Active Game Loop
    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        birdbox.centery += bird_movement
        screen.blit(rotated_bird,birdbox)
        # Collisions
        game_active = check_collison(pipe_list)
        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score_display("main_game")
    else: # Game Over
        high_score = update_score(score, high_score)
        score_display("game_over")
        screen.blit(game_over_surface, game_over_rect)
    # Floor
    floor_x_pos -= 0.5
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)

#ENDOFCODE
