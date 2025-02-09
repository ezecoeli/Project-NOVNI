import pygame
from pygame import mixer
import random
import csv
import button
import math

# Pygame initialization
pygame.init()
# Mixer initialization
mixer.init()

# Windows setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("NOVNI") # Title

icon = pygame.image.load("assets/images/tiny_ship.png") # Icon
pygame.display.set_icon(icon)

# Set framerate
clock = pygame.time.Clock()
FPS = 60

# Define game variables
GRAVITY = 1
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 34
MAX_LEVELS = 9 #########  Update for more levels
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
start_intro = False
show_story= False
glow_effects = []
score = 0
game_won = False

# Define player action variables
moving_left = False
moving_right = False
shoot = False
bomb = False
bomb_thrown = False

# Load sound and effects
walk_fx = pygame.mixer.Sound("assets/audio/sounds/walk.mp3")
walk_fx_channel = pygame.mixer.Channel(4)

jump_fx = pygame.mixer.Sound("assets/audio/sounds/jump.mp3")
jump_fx_channel = pygame.mixer.Channel(3)

power_fx = pygame.mixer.Sound("assets/audio/sounds/power.mp3")
power_fx_channel = pygame.mixer.Channel(3)

bomb_fx = pygame.mixer.Sound("assets/audio/sounds/bomb.mp3")
bomb_fx_channel = pygame.mixer.Channel(3)

thrown_bomb_fx = pygame.mixer.Sound("assets/audio/sounds/thrown_bomb.mp3")
thrown_bomb_fx_channel = pygame.mixer.Channel(3)

shot_fx = pygame.mixer.Sound("assets/audio/sounds/shot.mp3")
shot_fx.set_volume(0.1)
death_fx = pygame.mixer.Sound("assets/audio/sounds/death.mp3")
death_fx.set_volume(0.1)
grenade_fx = pygame.mixer.Sound("assets/audio/sounds/grenade.mp3")
grenade_fx.set_volume(0.2)
thrown_grenade_fx = pygame.mixer.Sound("assets/audio/sounds/thrown_grenade.mp3")
thrown_grenade_fx.set_volume(0.6)
bazooka_shot_fx = pygame.mixer.Sound("assets/audio/sounds/bazooka_shot.mp3")
bazooka_shot_fx.set_volume(0.3)
bazooka_hit_fx = pygame.mixer.Sound("assets/audio/sounds/bazooka_shot.mp3")
bazooka_hit_fx.set_volume(0.3)
item_box_fx = pygame.mixer.Sound("assets/audio/sounds/item_box_sound.mp3")
item_box_fx.set_volume(0.3)
typewriter_sound = pygame.mixer.Sound("assets/audio/sounds/typewriter_sound.mp3")
typewriter_sound.set_volume(0.3)
typewriter_channel = pygame.mixer.Channel(1)
boss_defeated_sound = pygame.mixer.Sound("assets/audio/sounds/boss_defeated_sound.mp3")
boss_defeated_sound.set_volume(0.3)
ship_fx = pygame.mixer.Sound("assets/audio/sounds/ship_sound.mp3")
ship_fx_channel = pygame.mixer.Channel(5)

## Load images
logo_img = pygame.image.load("assets/images/logo.png").convert_alpha()
logo_img = pygame.transform.scale(logo_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
story_img = pygame.image.load("assets/images/story.png").convert_alpha()
story_img = pygame.transform.scale(story_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
military_base_img = pygame.image.load("assets/images/military_base.png").convert_alpha()
boss_defeated_img = pygame.image.load("assets/images/boss_defeated.png").convert_alpha()
boss_defeated_img = pygame.transform.scale(boss_defeated_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Button images
start_img = pygame.image.load("assets/images/icons/start.png").convert_alpha()
exit_img = pygame.image.load("assets/images/icons/exit.png").convert_alpha()
restart_img = pygame.image.load("assets/images/icons/restart.png").convert_alpha()
game_over_img = pygame.image.load("assets/images/icons/game_over.png").convert_alpha()

# Levels Background
background_images = {
    1: pygame.image.load("assets/images/backgrounds/minnesota.png").convert_alpha(),
    2: pygame.image.load("assets/images/backgrounds/ohio.png").convert_alpha(),
    3: pygame.image.load("assets/images/backgrounds/nebraska.png").convert_alpha(),
    4: pygame.image.load("assets/images/backgrounds/wyoming.png").convert_alpha(),
    5: pygame.image.load("assets/images/backgrounds/nevada.png").convert_alpha(),
    6: pygame.image.load("assets/images/backgrounds/entrance.png").convert_alpha(),
    7: pygame.image.load("assets/images/backgrounds/x5G.png").convert_alpha(),
    8: pygame.image.load("assets/images/backgrounds/final.png").convert_alpha(),
    9: pygame.image.load("assets/images/backgrounds/ship.png").convert_alpha(),
    # add more
}
current_background = background_images[1]  # Start with level 1 background

# Store tiles in a list based on the level
def load_tiles_for_level(level):
    img_list = []
    tile_path = f"assets/images/tiles/level_{level}"
    for x in range(TILE_TYPES):
        img = pygame.image.load(f"{tile_path}/{x}.png")
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        img_list.append(img)
    return img_list

# Weapons and skills
power_img = pygame.image.load("assets/images/icons/power.png").convert_alpha()
bomb_img = pygame.image.load("assets/images/icons/bomb.png").convert_alpha()
bullet_img = pygame.image.load("assets/images/icons/bullet.png").convert_alpha()
grenade_img = pygame.image.load("assets/images/icons/grenade.png").convert_alpha()
projectile_img = pygame.image.load("assets/images/icons/projectile.png").convert_alpha()
# pick up boxes 
health_box_img = pygame.image.load("assets/images/icons/health.png").convert_alpha()
ammo_box_img = pygame.image.load("assets/images/icons/ammo.png").convert_alpha()
bombs_box_img = pygame.image.load("assets/images/icons/bombs_box.png").convert_alpha()
item_boxes = {
    "Health": health_box_img,
    "Ammo": ammo_box_img,
    "Bombs": bombs_box_img,
}

# Colors RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MATTE_BLACK = (85, 85, 85)
FALLOW = (193, 154, 107)
PERU = (205, 133, 63)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
CORAL = (255, 127, 80)

# Define font
font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 14)

# Texts function
def draw_text(text, font, text_col,x ,y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# Function to adjust text to multiple lines if necessary
def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        # Check the width of the line with the new word added
        test_line = current_line + " " + word if current_line else word
        width, _ = font.size(test_line)
        
        if width <= max_width:
            current_line = test_line
        else:
            if current_line:  # If there is already something in the line, save it and start a new one
                lines.append(current_line)
            current_line = word  # Start with the new word

    if current_line:  # Add the last line if there is text left to add
        lines.append(current_line)
    
    return lines

# Function to draw the wrapped text
def draw_wrapped_text(text, font, text_col, x, y, max_width):
    
    lines = wrap_text(text, font, max_width)
    for i, line in enumerate(lines):
        if not typewriter_channel.get_busy():
            typewriter_channel.play(typewriter_sound)
        draw_text(line, font, text_col, x, y + i * 45)

# Story variables
intro_text = """… En su viaje por el universo, el pequeño NOVNI sufre un accidente al ser alcanzado por una tormenta cósmica y aterriza de emergencia en la Tierra. Para regresar a casa, debe recuperar las piezas dispersas y llegar al cuartel del ejército X5G donde al parecer el Dr. Metroid tiene secuestrada su nave. Durante su camino deberá enfrentar a los soldados que quieren atraparlo para analizarlo. ¿Podrá NOVNI reconstruir su nave y regresar a casa? La aventura comienza ahora…"""
outro_text = """Tras superar todos los desafíos, NOVNI recuperó su nave y despegó rumbo a casa. Mientras la Tierra queda atrás, siente orgullo por su aventura. Su misión ha terminado... ¿o quizá sea solo el comienzo?"""
typed_text = ""
typed_text_final = ""
index = 0
typing_speed = 50
last_update_time = pygame.time.get_ticks()

# Victory screen function
def show_victory_screen():
    # Background
    victory_img = pygame.image.load("assets/images/victory.png")
    victory_img = pygame.transform.scale(victory_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(victory_img, (0, 0))

    # Victory music
    victory_music = pygame.mixer.Sound("assets/audio/music/victory_music.mp3")
    victory_music.play(loops=-1, maxtime=0, fade_ms=0)

    # Text victory
    text = font.render("¡Felicidades, has ganado!", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 300))

    text2 = font.render("Continuará...", True, WHITE)
    screen.blit(text2, (SCREEN_WIDTH - text2.get_width() - 10, SCREEN_HEIGHT - text2.get_height() - 100))

    text3 = font.render("Presiona Enter para volver al menú principal", True, CORAL)
    screen.blit(text3, (SCREEN_WIDTH - text3.get_width() - 95, SCREEN_HEIGHT - text3.get_height() - 10))

    # Show final player score
    score_text = font.render(f"Puntaje Final: {score}", True, CORAL)
    screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, screen.get_height() // 2 - 275))

    pygame.display.update()

# Reset level function
def reset_level():
    enemy_group.empty()
    rocket_group.empty()
    bullet_group.empty()
    bomb_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    # Create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data

# Background function
def draw_bg():
    scroll_position = bg_scroll % current_background.get_width()
    screen.blit(current_background, (-scroll_position, 0))
    screen.blit(current_background, (current_background.get_width() - scroll_position, 0))

# Check enemy kills and increase score
def check_enemy_deaths(enemy_group):
    global score
    for enemy in enemy_group:
        if enemy.health <= 0 and enemy.alive:
            enemy.alive = False
            score += 200

# Player
class Alien(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, bombs):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.bombs = bombs
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.in_spaceship = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        temp_list = []
        for i in range(2):
            img = pygame.image.load(f"assets/images/{self.char_type}/Idle/{i}.png")
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(9):
            img = pygame.image.load(f"assets/images/{self.char_type}/Run/{i}.png")
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)  
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(1):
            img = pygame.image.load(f"assets/images/{self.char_type}/Jump/{i}.png")
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)  
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(0):
            img = pygame.image.load(f"assets/images/{self.char_type}/Death/{i}.png")
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)  
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(1):
            img = pygame.image.load(f"assets/images/{self.char_type}/Shot/{i}.png")
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(1):
            img = pygame.image.load(f"assets/images/{self.char_type}/Throw/{i}.png")
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        for i in range(1):
            img = pygame.image.load(f"assets/images/{self.char_type}/Crouch/{i}.png")
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()
        # Update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        if self.in_spaceship:
            return 0, False

        # Reset movement variables
        screen_scroll = 0
        dx = 0
        dy = 0

        # Assign movement variables left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:    
            dx = self.speed
            self.flip = False
            self.direction = 1

        # Shot
        if shoot:
            self.update_action(4) #4: Shot

        # Throw bombs
        if bomb_thrown:
            self.update_action(5) #5: Throw

        # Jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -16
            self.jump = False
            self.in_air = True

        # Apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y    

        # Check for collision
        for tile in world.obstacle_list:
            # Check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                # If the AI has hit a wall then make it turn around
                if self.char_type == "player":
                    self.direction *= -1
                    self.move_counter = 0

            # Check collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # Check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
				# Check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        # Check for collision with water
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0
            self.alive = False

        # Check for collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

        # Check if fallen off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0
            self.alive = False

        # Check if going off the edges of the screen
        if self.char_type == "player":
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        # Update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        # Update scroll based on player position
        if self.char_type == "player":
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
				or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def shoot(self):
        if self.in_spaceship:
            return

        if self.shoot_cooldown == 0 and self.ammo > 0 and not player.in_spaceship:
            self.shoot_cooldown = 15
            power = Power(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery - 10, self.direction)
            power_group.add(power)
			# Reduce ammo
            self.ammo -= 1
            power_fx_channel.set_volume(0.3)
            power_fx_channel.play(power_fx)

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 200
        # Update image depending on current time
        self.image = self.animation_list[self.action][self.frame_index]
        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # Reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:    
                self.frame_index = 0

    def update_action(self, new_action):
        # Check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            #self.update_action(3)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

# Player shots (power)
class Power(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
       pygame.sprite.Sprite.__init__(self)
       self.speed = 10
       self.image = power_img
       self.rect = self.image.get_rect()
       self.rect.center = (x, y)
       self.direction = direction

    def update(self):
        global score
        # Move shots
        self.rect.x += (self.direction * self.speed) + screen_scroll
        # Check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        # Check for collision with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, power_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    score += 20
                    self.kill()

# Player Bombs
class Bombs(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
       pygame.sprite.Sprite.__init__(self)
       self.timer = 100
       self.vel_y = -11
       self.speed = 7
       self.image = bomb_img
       self.rect = self.image.get_rect()
       self.rect.center = (x, y)
       self.width = self.image.get_width()
       self.height = self.image.get_height()
       self.direction = direction

    def update(self):
        global score
        self.rect.x += screen_scroll
        self.vel_y += GRAVITY
        dx = self.direction * self.speed 
        dy = self.vel_y
        
        # Check for collision with level
        for tile in world.obstacle_list:
			# Check collision with walls
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
			# Check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
				# Check if below the ground, i.e. thrown up
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
				# Check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom

        # Update bomb position
        self.rect.x += dx
        self.rect.y += dy

        # Countdown timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            bomb_fx_channel.set_volume(0.3)
            bomb_fx_channel.play(bomb_fx)
            explosion = BombExplosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)
            # Do damage to anyone that is nearby
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 50
            for enemy in enemy_group:    
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 50
                    score += 50

# Boss
class Boss(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, projectiles, shoot_cooldown_time=40):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.shoot_cooldown_time = shoot_cooldown_time
        self.projectiles = projectiles
        self.last_grenade_time = 0
        self.grenade_cooldown = 2000
        self.health = 300
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        # AI specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 500, 50)
        self.idling = False
        self.idling_counter = 0

        temp_list = []
        for i in range(2):
            img = pygame.image.load(f"assets/images/{self.char_type}/Idle/{i}.png")
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(6):
            img = pygame.image.load(f"assets/images/{self.char_type}/Run/{i}.png")
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)  
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(0):
            img = pygame.image.load(f"assets/images/{self.char_type}/Jump/{i}.png")
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)  
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f"assets/images/{self.char_type}/Dead/{i}.png")
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()
        # Update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        # Reset movement variables
        screen_scroll = 0
        dx = 0
        dy = 0

        # Assign movement variables left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # Apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #check for collision
        for tile in world.obstacle_list:
			#check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
				#if the ai has hit a wall then make it turn around
                if self.char_type == "boss":
                    self.direction *= -1
                    self.move_counter = 0
			#check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				#check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
				#check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    if self.rect.bottom - dy <= tile[1].top + 5:
                        self.vel_y = 0
                        self.in_air = False
                        dy = tile[1].top - self.rect.bottom

        # Check for collision with water
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

        # Check if fallen off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

        # Update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        # Update scroll based on player position
        if self.char_type == "player":
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
				or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = self.shoot_cooldown_time
            rocket = Rocket(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery - 4, self.direction)
            rocket_group.add(rocket)
            # Reduce ammo
            self.ammo -= 1
            bazooka_shot_fx.play()

    def throw_projectiles(self):
        projectile = Projectile(self.rect.centerx + (self.direction * 25), self.rect.centery, self.direction)
        projectile_group.add(projectile)
        self.projectiles -= 1

    def ai(self):
        current_time = pygame.time.get_ticks()
        if self.alive and player.alive:

            # Random jump
            if not self.in_air and random.randint(1, 80) == 1:
                self.vel_y = -20
                self.in_air = True

            # Random move
            if self.idling == False and random.randint(1, 250) == 1 and not self.in_air:
                self.update_action(0) #0: idle
                self.idling = True
                self.idling_counter = 40
            # Update vision zone
            self.vision.center = (self.rect.centerx, self.rect.centery)

			# Check if the ai in near the player
            if self.vision.colliderect(player.rect):
				# Chase the player by moving towards him
                if player.rect.centerx < self.rect.centerx:
                    self.direction = -1  # Move left
                    ai_moving_left = True
                    ai_moving_right = False
                else:
                    self.direction = 1  # Move right
                    ai_moving_left = False
                    ai_moving_right = True

                self.move(ai_moving_left, ai_moving_right)
                self.update_action(1) #1: run
                self.shoot()
                if current_time - self.last_grenade_time > self.grenade_cooldown:
                    if random.randint(1, 3) == 1 and self.projectiles > 0:
                        bazooka_shot_fx.play() 
                        self.throw_projectiles()
                        self.last_grenade_time = current_time
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1) #1: run
                    self.move_counter += 1
					# Update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx, self.rect.centery)

                    if self.move_counter > random.randint(TILE_SIZE * 3, TILE_SIZE * 5):
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

		# Scroll
        self.rect.x += screen_scroll

    def update_animation(self):
		# Update animation
        ANIMATION_COOLDOWN = 200
		# Update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
		# Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
		# If the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
		# Check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
			# Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.update_action(3)
            self.health = 0
            self.speed = 0
            self.alive = False
            self.kill()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        boss_health_bar = BossHealthBar(self, self.health, self.max_health)
        boss_health_bar.draw(screen)

# Boss rockets
class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
       pygame.sprite.Sprite.__init__(self)
       self.speed = 5
       self.image = projectile_img
       self.rect = self.image.get_rect()
       self.rect.center = (x, y)
       self.direction = direction

       if self.direction == -1:
           self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        # Move power
        self.rect.x += (self.direction * self.speed) + screen_scroll
		# Check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
		# Check for collision with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                bazooka_hit_fx.play()
                self.kill()
                explosion = ProjectileExplosion(self.rect.x, self.rect.y, 0.5)
                explosion_group.add(explosion)
                return 

		# Check collision with characters
        if pygame.sprite.spritecollide(player, rocket_group, False):
            if player.alive:
                player.health -= 20
                bazooka_hit_fx.play()
                self.kill()
            explosion = ProjectileExplosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)

# Boss projectiles
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
       pygame.sprite.Sprite.__init__(self)
       self.timer = 100
       self.vel_y = -11
       self.speed = 7
       self.image = projectile_img
       self.rect = self.image.get_rect()
       self.rect.center = (x, y)
       self.width = self.image.get_width()
       self.height = self.image.get_height()
       self.direction = direction

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.x += screen_scroll
        self.vel_y += GRAVITY
        dx = self.direction * self.speed 
        dy = self.vel_y
        
        # Check for collision with level
        for tile in world.obstacle_list:
			# Check collision with walls
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
			# Check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
				# Check if below the ground, i.e. thrown up
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
				# Check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom

        # Update bomb position
        self.rect.x += dx
        self.rect.y += dy

        # Countdown timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            grenade_fx.play()
            explosion = ProjectileExplosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)

            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 50

# Enemy
class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades, shoot_cooldown_time=20):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.shoot_cooldown_time = shoot_cooldown_time
        self.grenades = grenades
        self.last_grenade_time = 0
        self.grenade_cooldown = 2000
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        # AI specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0

        temp_list = []
        for i in range(2):
            img = pygame.image.load(f"assets/images/{self.char_type}/Idle/{i}.png")
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(6):
            img = pygame.image.load(f"assets/images/{self.char_type}/Run/{i}.png")
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)  
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f"assets/images/{self.char_type}/Dead/{i}.png")
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()
        # Update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        # Reset movement variables
        screen_scroll = 0
        dx = 0
        dy = 0

        # Assign movement variables left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:    
            dx = self.speed
            self.flip = False
            self.direction = 1

        # Apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y    

        #check for collision
        for tile in world.obstacle_list:
			#check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
				#if the ai has hit a wall then make it turn around
                if self.char_type == "enemy":
                    self.direction *= -1
                    self.move_counter = 0
			#check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				#check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
				#check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    if self.rect.bottom - dy <= tile[1].top + 5:
                        self.vel_y = 0
                        self.in_air = False
                        dy = tile[1].top - self.rect.bottom

        # Check for collision with water
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

        # Check if fallen off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

        # Update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        # Update scroll based on player position
        if self.char_type == "player":
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
				or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = self.shoot_cooldown_time
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery - 9, self.direction)
            bullet_group.add(bullet)
            # Reduce ammo
            self.ammo -= 1
            shot_fx.play()

    def throw_grenade(self):
        grenade = Grenade(self.rect.centerx + (self.direction * 25), self.rect.centery, self.direction)
        grenade_group.add(grenade)
        self.grenades -= 1

    def ai(self):
        current_time = pygame.time.get_ticks()
        if self.alive and player.alive:

            # Random move
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0) #0: idle
                self.idling = True
                self.idling_counter = 50

			# Check if the ai in near the player
            if self.vision.colliderect(player.rect):
				# Stop running and face the player
                self.update_action(0) #0: idle
				# Shoot
                self.shoot()
                if current_time - self.last_grenade_time > self.grenade_cooldown:
                    if random.randint(1, 3) == 1 and self.grenades > 0:
                        thrown_grenade_fx.play() 
                        self.throw_grenade()
                        self.last_grenade_time = current_time
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1) #1: run
                    self.move_counter += 1
					# Update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
		# Scroll
        self.rect.x += screen_scroll

    def update_animation(self):
		# Update animation
        ANIMATION_COOLDOWN = 200
		# Update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
		# Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
		# If the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 2:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
		# Check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
			# Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(2)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

# Enemy shots
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
       pygame.sprite.Sprite.__init__(self)
       self.speed = 5
       self.image = bullet_img
       self.rect = self.image.get_rect()
       self.rect.center = (x, y)
       self.direction = direction

    def update(self):
        # Move power
        self.rect.x += (self.direction * self.speed) + screen_scroll
		# Check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
		# Check for collision with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

		# Check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()

        # Check collision with player power
        for power in power_group:
            if pygame.sprite.collide_rect(self, power):
                self.kill()
                power.kill()

# Enemy grenades
class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
       pygame.sprite.Sprite.__init__(self)
       self.timer = 100
       self.vel_y = -11
       self.speed = 7
       self.image = grenade_img
       self.rect = self.image.get_rect()
       self.rect.center = (x, y)
       self.width = self.image.get_width()
       self.height = self.image.get_height()
       self.direction = direction

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.x += screen_scroll
        self.vel_y += GRAVITY
        dx = self.direction * self.speed 
        dy = self.vel_y
        
        # Check for collision with level
        for tile in world.obstacle_list:
			# Check collision with walls
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
			# Check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
				# Check if below the ground, i.e. thrown up
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
				# Check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom

        # Update bomb position
        self.rect.x += dx
        self.rect.y += dy

        # Countdown timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            grenade_fx.play()
            explosion = GrenadeExplosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)

            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 35

# World class
class World():
    def __init__(self):
        self.obstacle_list = []

        # Defines the global tile mapping
        self.tile_mapping = {
            range(0, 9): self.add_obstacle,
            range(9, 11): self.add_water,
            range(11, 15): self.add_decoration,
            15: self.add_player,
            16: self.add_enemy,
            17: lambda img, x, y: self.add_item_box("Ammo", x, y),
            18: lambda img, x, y: self.add_item_box("Bombs", x, y),
            19: lambda img, x, y: self.add_item_box("Health", x, y),
            20: self.add_exit,
            range(21, 25): self.add_decoration,
            25: self.add_enemy2,
            26: self.add_decoration,
            27: self.add_enemy3,
            range(28, 30): self.add_obstacle,
            30: self.add_enemy4,
            31: self.add_enemy5,
            32: self.add_boss,
        }

    def add_obstacle(self, img, x, y):
        img_rect = img.get_rect()
        img_rect.x = x * TILE_SIZE
        img_rect.y = y * TILE_SIZE
        self.obstacle_list.append((img, img_rect))

    def add_water(self, img, x, y):
        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
        water_group.add(water)

    def add_decoration(self, img, x, y):
        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
        decoration_group.add(decoration)

    def add_player(self, img, x, y):
        global player, health_bar
        player = Alien("player", x * TILE_SIZE, y * TILE_SIZE, 0.7, 5, 10, 5)
        health_bar = HealthBar(8, 10, player.health, player.health)

    def add_enemy(self, img, x, y):
        enemy = Soldier("enemy", x * TILE_SIZE, y * TILE_SIZE, 1.2, 1, 100, 0, shoot_cooldown_time=30)
        enemy_group.add(enemy)

    def add_enemy2(self, img, x, y):
        enemy = Soldier("enemy2", x * TILE_SIZE, y * TILE_SIZE, 1.2, 1, 100, 5, shoot_cooldown_time=30)
        enemy_group.add(enemy)

    def add_enemy3(self, img, x, y):
        enemy = Soldier("enemy3", x * TILE_SIZE, y * TILE_SIZE, 1.2, 1, 100, 10, shoot_cooldown_time=20)
        enemy_group.add(enemy)

    def add_enemy4(self, img, x, y):
        enemy = Soldier("enemy4", x * TILE_SIZE, y * TILE_SIZE, 1.3, 2, 100, 15, shoot_cooldown_time=15)
        enemy_group.add(enemy)

    def add_enemy5(self, img, x, y):
        enemy = Soldier("enemy5", x * TILE_SIZE, y * TILE_SIZE, 1.3, 1, 100, 0, shoot_cooldown_time=10)
        enemy_group.add(enemy)

    def add_boss(self, img, x, y):
        enemy = Boss("boss", x * TILE_SIZE, y * TILE_SIZE, 1.3, 3, 500, 0, shoot_cooldown_time=80)
        enemy_group.add(enemy)

    def add_item_box(self, item_type, x, y):
        item_box = ItemBox(item_type, x * TILE_SIZE, y * TILE_SIZE)
        item_box_group.add(item_box)

    def add_exit(self, img, x, y):
        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
        exit_group.add(exit)

    def process_data(self, data, level):
        # Load tiles for the current level
        global img_list
        img_list = load_tiles_for_level(level)

        self.level_length = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    for tile_range, action in self.tile_mapping.items():
                        if (isinstance(tile_range, range) and tile in tile_range) or tile == tile_range:
                            action(img, x, y)
                            break
        return player, health_bar

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])

# Decorations class
class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll  

# Water class
class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

# Exit class (ship components)
class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        self.initial_y = self.rect.y 
        

    def update(self):
        self.rect.x += screen_scroll
        self.rect.y = self.initial_y + int(4 * math.sin(pygame.time.get_ticks() / 200.0))

        if pygame.sprite.collide_rect(self, player) and level == 9:
            player.image.set_alpha(0)
            player.in_spaceship = True
            spaceship.elevating = True

# Item drops
class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
       pygame.sprite.Sprite.__init__(self)
       self.item_type = item_type
       self.image = item_boxes[self.item_type]
       self.rect = self.image.get_rect()
       self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
       self.initial_y = self.rect.y 

    def update(self):
        global score
        # Scroll
        self.rect.x += screen_scroll
        self.rect.y = self.initial_y + int(4 * math.sin(pygame.time.get_ticks() / 200.0))
        # Check if the player has picked up the box
        if pygame.sprite.collide_rect(self, player):
            # Check type of box
            if self.item_type == "Health":
                item_box_fx.play()
                player.health += 25
                score += 100
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == "Ammo":
                if player.ammo < 20:
                    item_box_fx.play()
                    player.ammo += 15
                    score += 100
                    if player.ammo > 20:
                        player.ammo = 20
            elif self.item_type == "Bombs":
                item_box_fx.play()
                player.bombs += 3
                score += 100
            # Delete item box
            self.kill()

# Health bar
class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        # Update with new health
        self.health = health
        # Calculate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 160 * ratio, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 156, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 156 * ratio, 20))

# Boss Health Bar
class BossHealthBar():
    def __init__(self, boss, health, max_health):
        self.x = boss.rect.centerx - 50
        self.y = boss.rect.top -20
        self.health = health
        self.max_health = max_health
        self.width = 120
        self.height = 10

    def draw(self, surface):
        # Update health
        ratio = self.health / self.max_health

        # Define bar colors
        BACKGROUND_COLOR = (50, 50, 50)
        BORDER_COLOR = (255, 255, 255)
        HEALTH_COLOR = (39, 174, 96)

        if self.health <= self.max_health * 0.6:
            HEALTH_COLOR = (255, 165, 0)
        if self.health <= self.max_health * 0.3:
            HEALTH_COLOR = (255, 0, 0)

        pygame.draw.rect(surface, BACKGROUND_COLOR, (self.x - 2, self.y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(surface, BORDER_COLOR, (self.x, self.y, self.width, self.height), 2)
        pygame.draw.rect(surface, HEALTH_COLOR, (self.x, self.y, self.width * ratio, self.height))

# Bombs explotions
class BombExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 5):
            img = pygame.image.load(f"assets/images/explosions/bomb/exp{num}.png").convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # Scroll
        self.rect.x += screen_scroll

        EXPLOSION_SPEED = 4
        # Update explosion animation
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            # If animation is complete, delete explosion
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]

# Bombs explotions
class ProjectileExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 5):
            img = pygame.image.load(f"assets/images/explosions/projectile/exp{num}.png").convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # Scroll
        self.rect.x += screen_scroll

        EXPLOSION_SPEED = 4
        # Update explosion animation
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            # If animation is complete, delete explosion
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]

# Grenades explotions
class GrenadeExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 5):
            img = pygame.image.load(f"assets/images/explosions/grenade/exp{num}.png").convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # Scroll
        self.rect.x += screen_scroll

        EXPLOSION_SPEED = 4
        # Update explosion animation
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            # If animation is complete, delete explosion
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]

# Screen fade class
class ScreenFade():
    def __init__(self, direction, colour,speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1: # Whole screen fade
            pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.colour, (0, SCREEN_HEIGHT // 2 +self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
        if self.direction == 2: # Vertical screen fade down
            pygame.draw.rect(screen, self.colour, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True

        return fade_complete

# Spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/images/tiny_ship.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=(x, y))
        self.elevating = False

    def update(self):
        global game_won
        if self.elevating:
            if not ship_fx_channel.get_busy():
                ship_fx_channel.set_volume(0.2)
                ship_fx_channel.play(ship_fx)
            self.rect.y -= 3
            if self.rect.bottom < 0:
                ship_fx_channel.stop()
                self.kill()
                game_won = True

# Create Spaceship
spaceship = Spaceship((SCREEN_WIDTH // 2) - 47, SCREEN_HEIGHT - 155)


# Create screen fades
intro_fade = ScreenFade(1, MATTE_BLACK, 4)
death_fade = ScreenFade(2, BLACK, 4)

# Create buttons
start_button = button.Button(SCREEN_WIDTH // 2 - 38, SCREEN_HEIGHT - 220, start_img, 0.4)
exit_button = button.Button(737, 3, exit_img, 0.3)
restart_button = button.Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 120, restart_img, 0.4)

# Create sprite groups
enemy_group = pygame.sprite.Group()
power_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
bomb_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
rocket_group = pygame.sprite.Group()

# Create empty tile list
world_data = []
for row in range(ROWS):
	r = [-1] * COLS
	world_data.append(r)
# Load in level data and create world
with open(f'assets/levels/level{level}_data.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for x, row in enumerate(reader):
		for y, tile in enumerate(row):
			world_data[x][y] = int(tile)
world = World()
player, health_bar = world.process_data(world_data, level)


# Main Loop
menu_music_started = False
game_music_started = False
game_over_music_played = False
death_fx_played = False
level7_music_started = False
level8_music_started = False

menu_music_channel = pygame.mixer.Channel(0)
menu_music = pygame.mixer.Sound("assets/audio/music/intro_music.mp3")


run = True

while run:
    clock.tick(FPS)

    # Start menu music
    if start_game == False:
        if not menu_music_started:
            menu_music_channel.set_volume(0.2)
            menu_music_channel.play(menu_music, loops=-1)
            menu_music_started = True

    # Events and keys
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif not start_game: # Main menu
                if event.key == pygame.K_RETURN:
                    show_story = True
                    start_game = True
                    start_intro = True
            elif show_story: # Story
                if event.key == pygame.K_RETURN:
                    show_story = False
                    start_intro = True
            elif start_game: # Game
                if event.key == pygame.K_LEFT and not player.in_spaceship:
                    moving_left = True
                    if not walk_fx_channel.get_busy():
                        walk_fx_channel.set_volume(0.1)
                        walk_fx_channel.play(walk_fx, loops=-1)
                elif event.key == pygame.K_RIGHT and not player.in_spaceship:
                    moving_right = True
                    if not walk_fx_channel.get_busy():
                        walk_fx_channel.set_volume(0.1)
                        walk_fx_channel.play(walk_fx, loops=-1)

                elif event.key == pygame.K_a:
                    shoot = True
                elif event.key == pygame.K_s and not player.in_spaceship:
                    bomb = True
                    thrown_bomb_fx_channel.set_volume(0.3)
                    thrown_bomb_fx_channel.play(thrown_bomb_fx)
                elif event.key == pygame.K_SPACE and player.alive and not player.in_spaceship:
                    player.jump = True
                    jump_fx_channel.set_volume(0.1)
                    jump_fx_channel.play(jump_fx)

        elif event.type == pygame.KEYUP:
            if start_game:
                if event.key == pygame.K_LEFT:
                    moving_left = False
                    walk_fx_channel.stop()
                elif event.key == pygame.K_RIGHT:
                    moving_right = False
                    walk_fx_channel.stop()
                elif event.key == pygame.K_a:
                    shoot = False
                elif event.key == pygame.K_s:
                    bomb = False
                    bomb_thrown = False

    # Draw menu
    if not start_game:
        screen.fill(MATTE_BLACK)
        screen.blit(logo_img, (0, 0))
        if start_button.draw(screen):
            show_story = True
            start_game = True
            start_intro = True
        elif exit_button.draw(screen):
            run = False

    # Story
    elif show_story:
        screen.blit(story_img, (0, 0))
        current_time = pygame.time.get_ticks()
        if current_time - last_update_time > typing_speed and index < len(intro_text):
            typed_text += intro_text[index]
            index += 1
            last_update_time = current_time
        # Draw Wrapped Text
        draw_wrapped_text(typed_text, font, WHITE, 50, 80, 700)
        # If the text is complete, display:
        if index >= len(intro_text):
            draw_text("Presiona Enter para comenzar...", font, CORAL, 369, 617)
            typewriter_channel.stop()
            # If player press Enter then start game
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        show_story = False

    # Game
    else:
        # Stop music if player dies
        if not player.alive and not game_over_music_played:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            game_over_music_played = True

            if not death_fx_played:
                death_fx.play()
                death_fx_played = True

        # Play game music if it is running
        if player.alive:
            if not game_music_started:
                typewriter_channel.stop()
                menu_music_channel.stop()
                menu_music_started = False
                pygame.mixer.music.stop()
                pygame.mixer.music.load("assets/audio/music/game_music.mp3")
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1, 0.0, 1000)
                game_music_started = True

            # Stop music on level 6
            if level == 6:
                pygame.mixer.music.stop()
                game_music_started = False

            # Play level 7 music
            elif level == 7:
                if not level7_music_started:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("assets/audio/music/final_music.mp3")
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(-1, 0.0, 1000)
                    level7_music_started = True
            # Play level 8 music
            elif level == 8:
                if not level8_music_started:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("assets/audio/music/boss_music.mp3")
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(-1, 0.0, 1000)
                    level8_music_started = True

            # Play level 9 music
            elif level == 9:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.fadeout(500)
                level8_music_started = False

        draw_bg()
        # Glow effect for next level activation item
        for exit_obj in exit_group:
            glow_radius = 25 + 10 * math.sin(pygame.time.get_ticks() / 500.0)
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            glow_color = (255, 255, 255, 50)
            pygame.draw.ellipse(glow_surface, glow_color, (0, 0, glow_radius * 2, glow_radius * 2))
            glow_x = exit_obj.rect.centerx - glow_radius
            glow_y = exit_obj.rect.centery - glow_radius
            screen.blit(glow_surface, (glow_x, glow_y))

        world.draw()
        health_bar.draw(player.health)
        draw_text(f"SALUD: {player.health}", font, WHITE, 10, 13)
        screen.blit(ammo_box_img, (6, 32))
        for x in range(player.ammo):
            screen.blit(power_img, (42 + (x * 12), 35))
        screen.blit(bombs_box_img, (8, 60))
        for x in range(player.bombs):
            screen.blit(bomb_img, (45 + (x * 12), 64))

        # Show score on screen
        score_text = font.render(f"Puntos: {score:05}", True, (255, 255, 255))
        screen.blit(score_text, (320, 10))

        player.update()

        check_enemy_deaths(enemy_group)

        player.draw()
        
        # Update and draw ship on level 9 
        if level == 9:
            spaceship.update()
            screen.blit(spaceship.image, spaceship.rect)
            # Activate game won
            if spaceship.rect.bottom < 0:
                game_won = True

        if game_won:
            show_victory_screen()
            victory_screen_active = True
            index = 0
            last_update_time = pygame.time.get_ticks()

            while victory_screen_active:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        victory_screen_active = False
                        run = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            victory_screen_active = False
                            run = False
                        elif event.key == pygame.K_RETURN:
                            start_intro = True
                            level = 1
                            score = 0
                            game_won = False
                            victory_screen_active = False
                            start_game = False

                            pygame.mixer.music.stop()
                            menu_music_started = False
                            game_music_started = False
                            pygame.mixer.music.load("assets/audio/music/intro_music.mp3")
                            pygame.mixer.music.play(-1, 0.0, 1000)

                            # Reset player and level
                            world_data = reset_level()
                            with open(f"assets/levels/level{level}_data.csv", newline="") as csvfile:
                                reader = csv.reader(csvfile, delimiter=",")
                                for x, row in enumerate(reader):
                                    for y, tile in enumerate(row):
                                        world_data[x][y] = int(tile)
                            world = World()
                            player, health_bar = world.process_data(world_data, level)
                            current_background = background_images[level]
                            
                pygame.display.update()

        for enemy in enemy_group:
            enemy.ai()
            enemy.update()
            enemy.draw()

        # Update and draw groups
        for group in [power_group, grenade_group, projectile_group, rocket_group, bullet_group, bomb_group, explosion_group, item_box_group, decoration_group, water_group, exit_group]:
            group.update()
            group.draw(screen)

        # Show fade
        if start_intro and intro_fade.fade():
            start_intro = False
            intro_fade.fade_counter = 0

        if player.alive:
            if shoot:
                player.shoot()
                moving_left = False
                moving_right = False
            elif bomb and not bomb_thrown and player.bombs > 0:
                bomb = Bombs(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction), player.rect.top, player.direction)
                bomb_group.add(bomb)
                player.bombs -= 1
                bomb_thrown = True
            if player.in_air:
                player.update_action(2)
            elif moving_left or moving_right:
                player.update_action(1)
            else:
                player.update_action(0)
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll
            # Handle boss level
            if level == 8:
                boss_alive = any(isinstance(enemy, Boss) and enemy.alive for enemy in enemy_group)
                if not boss_alive:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.fadeout(500)
                        level8_music_started = False
                        screen.blit(boss_defeated_img, (0, 0))
                        boss_defeated_sound.play()
                        pygame.display.update()
                        pygame.time.delay(5000)

                        level_complete = True

            if level_complete and level < 9:
                start_intro = True
                level += 1
                bg_scroll = 0
                # Save player stats before load next levels
                previous_health = player.health
                previous_ammo = player.ammo
                previous_bombs = player.bombs

                world_data = reset_level()

                if level <= MAX_LEVELS:
                    current_background = background_images[level]
                    # Load level data
                    with open(f"assets/levels/level{level}_data.csv", newline="") as csvfile:
                        reader = csv.reader(csvfile, delimiter=",")
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data, level)

                    # Restore player stats
                    player.health = previous_health
                    player.ammo = previous_ammo
                    player.bombs = previous_bombs

        else:
            player.image.set_alpha(max(0, player.image.get_alpha() - 10))
            screen_scroll = 0
            if death_fade.fade():
                # Show "Game Over" screen
                screen.blit(game_over_img, (250, 200))

                if restart_button.draw(screen):
                    # Reset variables for restart game
                    death_fade.fade_counter = 0
                    death_fx_played = False
                    game_over_music_played = False

                    start_intro = True
                    bg_scroll = 0
                    player.health = player.max_health  
                    player.alive = True  
                    moving_left = False
                    moving_right = False
                    shoot = False
                    bomb = False
                    bomb_thrown = False

                    # Restart level data
                    world_data = reset_level()
                    with open(f"assets/levels/level{level}_data.csv", newline="") as csvfile:
                        reader = csv.reader(csvfile, delimiter=",")
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data, level)
                    current_background = background_images[level]

                    # Resume game music
                    if game_music_started:
                        pygame.mixer.music.play(-1, 0.0, 1000)

    pygame.display.update()

pygame.quit()