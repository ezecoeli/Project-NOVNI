import pygame
from pygame import mixer
import random
import csv
import button
import os
import time

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
TILE_TYPES = 25
MAX_LEVELS = 6 #########  Update for more levels
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
start_intro = False

# Define player action variables
moving_left = False
moving_right = False
shoot = False
bomb = False
bomb_thrown = False

# Load music and sounds
pygame.mixer.music.load("assets/audio/music/menu.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = pygame.mixer.Sound("assets/audio/sounds/jump.mp3")
jump_fx.set_volume(0.2)
power_fx = pygame.mixer.Sound("assets/audio/sounds/power.mp3")
power_fx.set_volume(0.2)
bomb_fx = pygame.mixer.Sound("assets/audio/sounds/bomb.mp3")
bomb_fx.set_volume(0.2)
thrown_bomb_fx = pygame.mixer.Sound("assets/audio/sounds/thrown_bomb.mp3")
thrown_bomb_fx.set_volume(0.2)
shot_fx = pygame.mixer.Sound("assets/audio/sounds/shot.mp3")
shot_fx.set_volume(0.2)

## Load images
logo_img = pygame.image.load("assets/images/logo.png")
logo_img = pygame.transform.scale(logo_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
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
    6: pygame.image.load("assets/images/backgrounds/x5G.png").convert_alpha(),
    # add more
}
current_background = background_images[1]  # Start with level 1 background

# Store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f"assets/images/tiles/{x}.png")
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

# Weapons and skills
power_img = pygame.image.load("assets/images/icons/power.png").convert_alpha()
bomb_img = pygame.image.load("assets/images/icons/bomb.png").convert_alpha()
bullet_img = pygame.image.load("assets/images/icons/bullet.png").convert_alpha()
#grenade_img = pygame.image.load("assets/images/icons/grenade.png").convert_alpha()
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

# Define font
font = pygame.font.Font("assets/fonts/vhs_gothic.ttf", 15)

# Texts function
def draw_text(text, font, text_col,x ,y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Reset level function
def reset_level():
    enemy_group.empty()
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
        for i in range(1):
            img = pygame.image.load(f"assets/images/{self.char_type}/Death/{i}.png")
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

        # Jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -15
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

        # Check for collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

        # Check if fallen off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

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
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            power = Power(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            power_group.add(power)
			# Reduce ammo
            self.ammo -= 1
            shot_fx.play()

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 300
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
            self.update_action(3)

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
            bomb_fx.play()
            explosion = Explosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)
            # Do damage to anyone that is nearby
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 50
            for enemy in enemy_group:    
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 50

# Enemy
class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
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
        for i in range(1):
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

        # Jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

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
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery - 10, self.direction)
            bullet_group.add(bullet)
            # Reduce ammo
            self.ammo -= 1
            shot_fx.play()

    def ai(self):
        if self.alive and player.alive:
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
        ANIMATION_COOLDOWN = 300
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
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

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
            range(21, 30): self.add_decoration,
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
        player = Alien("player", x * TILE_SIZE, y * TILE_SIZE, 0.8, 5, 10, 5)
        health_bar = HealthBar(10, 10, player.health, player.health)

    def add_enemy(self, img, x, y):
        enemy = Soldier("enemy", x * TILE_SIZE, y * TILE_SIZE, 0.9, 2, 100)
        enemy_group.add(enemy)

    def add_item_box(self, item_type, x, y):
        item_box = ItemBox(item_type, x * TILE_SIZE, y * TILE_SIZE)
        item_box_group.add(item_box)

    def add_exit(self, img, x, y):
        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
        exit_group.add(exit)

    def process_data(self, data):
        self.level_length = len(data[0])
        # Iterate through each value in level data
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

# Function to load tiles dynamically by level
def load_tile_images(level_path):
    img_list = []
    for i in range(len(os.listdir(level_path))):
        img = pygame.image.load(f"{level_path}/{i}.png").convert_alpha()
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        img_list.append(img)
    return img_list

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

# Exit class
class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

# Item drops
class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
       pygame.sprite.Sprite.__init__(self)
       self.item_type = item_type
       self.image = item_boxes[self.item_type]
       self.rect = self.image.get_rect()
       self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    
    def update(self):
        # Scroll
        self.rect.x += screen_scroll
        # Check if the player has picked up the box
        if pygame.sprite.collide_rect(self, player):
            # Check type of box
            if self.item_type == "Health":
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == "Ammo":
                player.ammo += 15
            elif self.item_type == "Bombs":
                player.bombs += 3
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
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154 * ratio, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))

# Explotions
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 5):
            img = pygame.image.load(f"assets/images/explosion/exp{num}.png").convert_alpha()
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

# Create screen fades
intro_fade = ScreenFade(1, MATTE_BLACK, 4)
death_fade = ScreenFade(2, BLACK, 4)

# Create buttons
start_button = button.Button(SCREEN_WIDTH // 2 - 38, SCREEN_HEIGHT - 200, start_img, 0.4)
exit_button = button.Button(SCREEN_WIDTH - 90, SCREEN_HEIGHT - 70, exit_img, 0.4)
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

# Create empty tile list
world_data = []
for row in range(ROWS):
	r = [-1] * COLS
	world_data.append(r)
# Load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for x, row in enumerate(reader):
		for y, tile in enumerate(row):
			world_data[x][y] = int(tile)
world = World()
player, health_bar = world.process_data(world_data)


# Main
run = True
while run:

    clock.tick(FPS)

    if start_game == False:
        # Draw menu
        screen.fill(MATTE_BLACK)
        # Add buttons and Logo
        screen.blit(logo_img, (0, 0))
        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            run = False
    else:
        # Update background
        draw_bg()
        # Draw world map
        world.draw()
        # Show player health
        health_bar.draw(player.health)
        # Show health
        draw_text(f"HEALTH: {player.health}", font, WHITE, 10, 12)
        # Show ammo
        draw_text("AMMO: ", font, WHITE, 10, 35)
        for x in range(player.ammo):
            screen.blit(power_img, (65 + (x * 10), 36))
        # Show bombs
        draw_text("BOMBS: ", font, WHITE, 10, 60)
        for x in range(player.bombs):
            screen.blit(bomb_img, (77 + (x * 10), 65))
        
        player.update()
        player.draw()

        # Update and draw enemies
        for enemy in enemy_group:
            enemy.ai()
            enemy.update()
            enemy.draw()

        # Update groups
        power_group.update()
        bullet_group.update()
        bomb_group.update()
        explosion_group.update()
        item_box_group.update()
        decoration_group.update()
        water_group.update()
        exit_group.update()
        # Draw groups
        power_group.draw(screen)
        bullet_group.draw(screen)
        bomb_group.draw(screen)
        explosion_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)

        # Show intro
        if start_intro == True:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0

        # Update player actions
        if player.alive:
            # Shoot power
            if shoot:
                player.shoot()
            # Throw bombs
            elif bomb and bomb_thrown == False and player.bombs > 0:
                bomb = Bombs(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction), player.rect.top, player.direction)
                bomb_group.add(bomb)
                # Reduce bombs
                player.bombs -= 1
                bomb_thrown = True
            if player.in_air:
                player.update_action(2) #2: jump
            elif moving_left or moving_right:
                player.update_action(1) #1: run
            else:
                player.update_action(0) #0: idle
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll
            # Check if player has completed the level
            if level_complete:
                start_intro = True
                level += 1
                bg_scroll = 0
                world_data = reset_level()
                if level <= MAX_LEVELS:
                    current_background = background_images[level]
                    # Load in level data and create world
                    with open(f"level{level}_data.csv", newline= "") as csvfile:
                        reader = csv.reader(csvfile, delimiter= ",")
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data)
        else:
            screen_scroll = 0
            if death_fade.fade():
                screen.blit(game_over_img, (250, 200))
                if restart_button.draw(screen):
                    death_fade.fade_counter = 0
                    start_intro = True
                    bg_scroll = 0
                    world_data = reset_level()
                    # Load in level data and create world
                    with open(f"level{level}_data.csv", newline= "") as csvfile:
                        reader = csv.reader(csvfile, delimiter= ",")
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data)

    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
            run = False
        # Keyboard presses    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:
                bomb = True
                thrown_bomb_fx.play()
            if event.key == pygame.K_w and player.alive:
                player.jump = True
                jump_fx.play()
            if event.key == pygame.K_ESCAPE:
                run = False

        # Keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False    
            if event.key == pygame.K_q:
                bomb = False
                bomb_thrown = False

    pygame.display.update()

pygame.quit()
