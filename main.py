import pygame
import os
import sys

# Pygame initialization
pygame.init()

# Windows setup
WIDTH = 800
HEIGHT = int(WIDTH * 0.8)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NOVNI") # Title
icon = pygame.image.load("assets/images/tiny_ship.png") # Icon
pygame.display.set_icon(icon)

# Set framerate
clock = pygame.time.Clock()
FPS = 60

# Define game variables
GRAVITY = 0.75

# Define player action variables
moving_left = False
moving_right = False
shoot = False

# Load images
bullet_img = pygame.image.load("assets/images/icons/bullet1.png").convert_alpha()

# Colors RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FALLOW = (193, 154, 107)
PERU = 	(205, 133, 63)

def draw_bg():
    screen.fill(PERU)
    pygame.draw.line(screen, BLACK, (0, 300), (WIDTH, 300))

# Player
class Alien(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
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
        for i in range(5):
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
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self):
        self.update_animation()
        # Update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        # Reset movement variables
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

        # Check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        # Update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            # Reduce ammo
            self.ammo -= 1

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
            self.frame_index = 0

    def update_action(self, new_action):
        # Check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
       pygame.sprite.Sprite.__init__(self)
       self.speed = 10
       self.image = bullet_img
       self.rect = self.image.get_rect()
       self.rect.center = (x, y)
       self.direction = direction

    def update(self):
        # Move bullet
        self.rect.x += (self.direction * self.speed)
        # Check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

# Create sprite groups
bullet_group = pygame.sprite.Group()


player = Alien("player",150, 550, 0.4, 5, 20)
#enemy = Alien("enemy", 300, 550, 0.3, 5, 20)

# Main
run = True
while run:

    clock.tick(FPS)
    
    draw_bg()
    
    player.update()
    player.draw()
    #enemy.draw()
    
    # Update and draw groups
    bullet_group.update()
    bullet_group.draw(screen)


    # Update player actions
    if player.alive:
        # Shoot bullets
        if shoot:
            player.shoot()
        if player.in_air:
            player.update_action(2) #2: jump
        elif moving_left or moving_right:
            player.update_action(1) #1: run
        else:
            player.update_action(0) #0: idle
        player.move(moving_left, moving_right)

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
            if event.key == pygame.K_w and player.alive:
                player.jump = True
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

    pygame.display.update()

pygame.quit()    