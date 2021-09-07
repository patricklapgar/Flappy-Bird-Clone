import pygame, sys, os, random

def draw_game_floor():
    # Create two instances of the game floor object and place them side by side
    screen.blit(floor_surface, (floor_x_position,900))
    screen.blit(floor_surface, (floor_x_position + 576,900))
    
def create_pipe():
    randome_pipe_position = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700, randome_pipe_position))
    top_pipe = pipe_surface.get_rect(midbottom = (700, randome_pipe_position - 300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    
    return pipes

# Iterate through pipe list and draw them to the screen
def draw_pipes(pipes):
    for pipe in pipes:

        # Flip pipe if it is upside down
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

# Collision detection function
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):

    if game_state == 'main_game':
        score_surface = game_font.render('Score: ' + str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)

    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (288, 850))
        screen.blit(score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    
    return high_score

asset_path = "/Users/papga/code_projects/Python_Projects/Flappy Bird/assets/"
sound_path = "/Users/papga/code_projects/Python_Projects/Flappy Bird/sound/"

# Initiate game and pygame mixer
pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()
 
# Create display surface
screen = pygame.display.set_mode((576, 1024)) # 576 pixels wide, 1024 pixels tall
# Create clock object
clock = pygame.time.Clock()

game_font = pygame.font.Font(os.path.abspath('/Users/papga/code_projects/Python_Projects/Flappy Bird/04B_19.ttf'), 40)

# Game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0


# Create game background
background_surface = pygame.image.load(os.path.abspath(asset_path + "background-day.png")).convert()
background_surface = pygame.transform.scale2x(background_surface) # Re-initiate variable to scale it according to screen

# Create game floor surface
floor_surface = pygame.image.load(os.path.abspath(asset_path + "base.png")).convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_position = 0

# Create bird image
# bird_surface = pygame.image.load(os.path.abspath(asset_path + "bluebird-midflap.png")).convert_alpha()
# bird_surface = pygame.transform.scale2x(bird_surface)
# bird_rect = bird_surface.get_rect(center = (100, 512))

bird_downflap = pygame.transform.scale2x(pygame.image.load(asset_path + "bluebird-downflap.png").convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load(asset_path + "bluebird-midflap.png").convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load(asset_path + "bluebird-upflap.png").convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# Create pip surfaces
pipe_surface = pygame.image.load(os.path.abspath(asset_path + "pipe-green.png")).convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = [] # Input pipes to display on screen
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800] # All possible heights that pipes can have

game_over_surface = pygame.transform.scale2x(pygame.image.load(asset_path + 'message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288, 512))

# Sound variables
flap_sound = pygame.mixer.Sound(sound_path + 'sfx_wing.wav')
death_sound = pygame.mixer.Sound(sound_path + 'sfx_hit.wav')
score_sound = pygame.mixer.Sound(sound_path + 'sfx_point.wav')
score_sound_countdown = 100

# Game loop
while True:

    # Event loop
    for event in pygame.event.get():
        
        # Close game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle space key event to make the bird jump
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 12
                flap_sound.play()

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            print(pipe_list)

        if event.type == BIRDFLAP:

            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            
            bird_surface, bird_rect = bird_animation()

    screen.blit(background_surface, (0,0))

    if game_active:
        # Bird movement
        bird_movement += gravity

        # Rotate bird
        rotated_bird = rotate_bird(bird_surface)

        bird_rect.centery += bird_movement 
        screen.blit(rotated_bird, bird_rect)

        game_active = check_collision(pipe_list)

        # Pipes movement
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        
        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1

        # Play the score sound after each cycle of score that is accumulated as the game progresses
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100

        floor_x_position -= 1
        draw_game_floor()
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')



    # Floor movement
    # When the edge of the far-right game floor reaches the boundary of the screen
    # reset the game floor position
    if floor_x_position <= -576:
        floor_x_position = 0


    pygame.display.update()
    clock.tick(120)
