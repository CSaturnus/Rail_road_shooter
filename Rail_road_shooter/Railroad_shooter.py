import pygame
import math
import random

pygame.init()
pygame.mixer.init()

#Loading in the different starships sprites
Starship_1 = pygame.image.load('Assets/sprites/Starship_1.png')
Starship_1_gun = pygame.image.load('Assets/sprites/Starship_1_gun.png')
Shooter = pygame.image.load('Assets/sprites/Shooting_device_Starship_1.png')

Laser_sprite = pygame.image.load('Assets/sprites/Laser.png')
Laser_sprite2 = pygame.image.load('Assets/sprites/Laser_2.png')
Big_laser_sprite = pygame.image.load('Assets/sprites/Big_laser.png')

Enemy_1 = pygame.image.load('Assets/sprites/Starship_3.png')
Enemy_2 = pygame.image.load('Assets/sprites/Starship_2.png')

Panel = pygame.image.load('Assets/sprites/Wood_panel.png')
Ammo_bar = pygame.image.load('Assets/sprites/Ammo_bar.png')

# RGB values of standard colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (65, 105, 225)
RED = (155, 28, 49)

WIDTH, HEIGHT = 1160, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("space_shooter")

clock = pygame.time.Clock() 
FPS = 60

def get_sprite(sheet, x, y, width, height):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    return sprite

class Ship:
    def __init__(self, posx, posy, width, height):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.spriteCounter = 0
        self.ammo = 80
        self.playerrect = pygame.Rect(posx, posy, width, height)
        self.powerup = 0
	
    def display(self):
        sprite = get_sprite(Starship_1_gun, self.spriteCounter*78, 0, 78, 62)
        self.ShipRect = pygame.Rect(self.posx, self.posy, self.width, self.height)
        screen.blit(sprite, self.ShipRect)
        self.spriteCounter += 1
        if self.spriteCounter > 4:
            self.spriteCounter = 0

class Bullet:
    def __init__(self, posx, posy, width, height, speed):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.rect = pygame.Rect(posx, posy, width, height)

    def move(self):
        self.posy -= self.speed
        self.rect.y = self.posy

    def display(self):
        pygame.draw.rect(screen, WHITE, self.rect)
        screen.blit(Laser_sprite, self.rect)

class Big_laser:
    def __init__(self, posx, posy, width, height):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.rect = pygame.Rect(posx, posy, width, height)

    def move(self, posx, posy):
        self.posy = posy
        self.posx = posx
        self.rect.y = self.posy-self.height+66
        self.rect.x = self.posx

    def display(self):
        screen.blit(Big_laser_sprite, self.rect)

class enemyShip1:
    def __init__(self, posx, posy, speed):
        self.posx = posx
        self.posy = posy
        self.width = 50
        self.height = 50
        self.speed = speed
        self.rect = pygame.Rect(posx, posy, self.width, self.height)
        self.spriteCounter = 0
        self.animationSpeed = 5  # Adjust this value to control the animation speed
        self.animationTimer = 0
        self.sine_wave_amplitude = random.randint(50, 150)
        self.sine_wave_frequency = random.uniform(0.01, 0.05)
        self.initial_x = posx

    def move(self):
        self.posy += self.speed
        self.posx = self.initial_x + self.sine_wave_amplitude * math.sin(self.sine_wave_frequency * self.posy)
        
        # Ensure the enemy stays within the box
        if self.posx < 90:
            self.posx = 90
        elif self.posx > WIDTH - 145:
            self.posx = WIDTH - 145
        
        self.rect.y = self.posy
        self.rect.x = self.posx

    def display(self):
        self.animationTimer += 1
        if self.animationTimer % self.animationSpeed == 0:
            self.spriteCounter += 1
            if self.spriteCounter > 4:
                self.spriteCounter = 0
        sprite = get_sprite(Enemy_1, self.spriteCounter * 50, 0, 50, 50)
        sprite = pygame.transform.rotate(sprite, 180)
        self.ShipRect = pygame.Rect(self.posx, self.posy, self.width, self.height)
        screen.blit(sprite, self.ShipRect)

class enemyShip2:
    def __init__(self, posx, posy, speed):
        self.posx = posx
        self.posy = posy
        self.width = 50
        self.height = 60
        self.speed = speed
        self.rect = pygame.Rect(posx, posy, self.width, self.height)
        self.spriteCounter = 0
        self.animationSpeed = 5  # Adjust this value to control the animation speed
        self.animationTimer = 0
        self.direction = 1
        self.hp = 10

    def move(self):
        if self.posy < 100:
            self.posy += self.speed
        else:
            if self.posx < 90:
                self.direction *= -1
            if self.posx > WIDTH - 145:
                self.direction *= -1
            self.posx += self.speed * self.direction
            
        self.rect.y = self.posy
        self.rect.x = self.posx

    def display(self):
        self.animationTimer += 1
        if self.animationTimer % self.animationSpeed == 0:
            self.spriteCounter += 1
            if self.spriteCounter > 7:
                self.spriteCounter = 0
        sprite = get_sprite(Enemy_2, self.spriteCounter * 50, 0, 50, 60)
        self.ShipRect = pygame.Rect(self.posx, self.posy, self.width, self.height)
        screen.blit(sprite, self.ShipRect)

class Laser2:
    def __init__(self, posx, posy, width, height, speed):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.rect = pygame.Rect(posx, posy, width, height)

    def move(self):
        self.posy += self.speed
        self.rect.y = self.posy

    def display(self):
        pygame.draw.rect(screen, WHITE, self.rect)
        screen.blit(Laser_sprite2, self.rect)

def gameplay():
    running = True

    #INitializing the starship and the bullets
    Starship = Ship(WIDTH/2, HEIGHT/2, 78, 62)    
    bullets = []
    enemy_laser = []
    enemies_1 = []
    enemies_2 = []
    Big_laser_coll = []
    Big_laser_counter = 0
    gun_change = False
    initialFireRate = 30  # Initial fire rate (higher value means slower firing)
    minFireRate = 2  # Minimum fire rate (higher value means slower firing)'
    ammoReload = True
    Enemy_1_timer = 0
    Laser_counter = 0
    build_up_timer = 0
    spawn_2 = FPS * 7
    Big_laser_charge = 0

    while running:
        clock.tick(FPS)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:  # Key pressed
                if event.key == pygame.K_l and Big_laser_charge == FPS*20:
                    Big_laser_charge = 0
                    Big_laser_coll.append(Big_laser(Starship.posx + 2, Starship.posy, 74, 800))

        if Big_laser_charge < FPS*20:
            Big_laser_charge += 1


        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and Starship.posy > 0:
            Starship.posy -= 5
        if keys[pygame.K_s] and Starship.posy < HEIGHT - Starship.height:
            Starship.posy += 5
        if keys[pygame.K_a] and Starship.posx > 90:
            Starship.posx -= 5
        if keys[pygame.K_d] and Starship.posx < WIDTH - Starship.width - 95:
            Starship.posx += 5
        if keys[pygame.K_j] and Starship.ammo > 0 and ammoReload == True:
            gunTimer += 1
            fireRate = max(minFireRate, initialFireRate * math.exp(-0.025 * gunTimer))
            if gunTimer % int(fireRate) == 0:
                if gun_change == False:
                    bullets.append(Bullet(Starship.posx + 69, Starship.posy + 10, 5, 19, 10))
                    gun_change = True
                    Starship.ammo -= 1
                else:
                    bullets.append(Bullet(Starship.posx + 4, Starship.posy + 10, 5, 19, 10))
                    gun_change = False
                    Starship.ammo -= 1
        else:
            gunTimer = 0
            fireRate = initialFireRate  # Reset fire rate when the button is released

        if Starship.ammo == 0 or ammoReload == False:
            ammoReload = False
            Starship.ammo += 1
            if Starship.ammo == 80:
                ammoReload = True

        Enemy_1_timer += 1 + build_up_timer

        spawn_2 -= 1
        if len(enemies_2) < 1 and spawn_2 < 0:
            spawn_enemy = True
            enemies_2.append(enemyShip2(random.random() * 930 + 90, -50, 7))
        elif len(enemies_2) == 1:
            spawn_2 = FPS * 10
            Laser_counter += 1
            
        
        if Laser_counter*random.random() > 50 and len(enemies_2) > 0:
            enemy_laser.append(Laser2(enemies_2[0].posx + 25, enemies_2[0].posy + 50, 5, 19, 10))
            Laser_counter = 0

        if len(enemies_1) < 20 and int(Enemy_1_timer) > 20:
            spawn_enemy = True
            while spawn_enemy:
                new_enemy_1_posx = random.random() * 930 + 90
                new_enemy_1_posy = -50
                new_enemy_rect = pygame.Rect(new_enemy_1_posx, new_enemy_1_posy, 50, 50)
                spawn_enemy = False
                for enemy in enemies_1:
                    if new_enemy_rect.colliderect(enemy.rect):
                        spawn_enemy = True
                        break
            enemies_1.append(enemyShip1(new_enemy_1_posx, new_enemy_1_posy, random.random()*5))
            Enemy_1_timer = 0
            build_up_timer += 0.002

        for enemy in enemies_2:
            enemy.move()
        
        for enemy in enemies_1:
            enemy.move()
            if enemy.posy > 800:
                enemies_1.remove(enemy)

        for bullet in bullets:
            bullet.move()
            if bullet.posy < -20:
                bullets.remove(bullet)

        #THE BIG LASER
        for laser in Big_laser_coll:
            laser.move(Starship.posx + 2, Starship.posy - 50)
            Big_laser_counter += 1
            print(Big_laser_counter)
            if Big_laser_counter > FPS*2:
                Big_laser_coll.remove(laser)
                Big_laser_counter = 0
            for enemy in enemies_1:
                if laser.rect.colliderect(enemy.rect):
                    enemies_1.remove(enemy)
            for enemy_2 in enemies_2:
                if laser.rect.colliderect(enemy_2.rect):
                    enemies_2.remove(enemy_2)
            

        for laser in enemy_laser:
            laser.move()
            if laser.posy > HEIGHT:
                enemy_laser.remove(laser)
        
        for bullet in bullets:
            for enemy in enemies_1:
                if bullet.rect.colliderect(enemy.rect):
                    bullets.remove(bullet)
                    enemies_1.remove(enemy)
                    break
            for enemy_2 in enemies_2:
                if bullet.rect.colliderect(enemy_2.rect):
                    bullets.remove(bullet)
                    enemy_2.hp -= 1
                    if enemy_2.hp == 0:
                        enemies_2.remove(enemy_2)
                    break
        
        for enemy in enemies_1:
            if enemy.rect.colliderect(Starship.ShipRect):
                running = False
        for enemy in enemies_2:
            if enemy.rect.colliderect(Starship.ShipRect):
                running = False
        for laser in enemy_laser:
            if laser.rect.colliderect(Starship.ShipRect):
                running = False

        # Drawing the enemies
        for enemy in enemies_1:
            enemy.display()

        for enemy in enemies_2:
            enemy.display()
        

        # Drawing ammo bar
        current_ammo_height = (Starship.ammo / 80) * 770
        pygame.draw.rect(screen, BLUE, (19, 38 + 770 - current_ammo_height, 52, current_ammo_height))
        # Drawing side panels
        screen.blit(Ammo_bar, (0 , 0))

        #Drawing laser charge bar
        current_charge_height = (Big_laser_charge / (FPS*20)) * 770
        pygame.draw.rect(screen, RED, (WIDTH - 71, 38 + 770 - current_charge_height, 52, current_charge_height))
        screen.blit(Ammo_bar, (WIDTH - 90 , 0))

        #Displaying the starship
        Starship.display()

        #displaying the bullets, lasers
        for bullet in bullets:
            bullet.display()
        for laser in enemy_laser:
            laser.display()
        for laser in Big_laser_coll:
            laser.display()
        
        #print clock in terminal for debugging

        #updating diplay
        pygame.display.update()

if __name__ == "__main__":
    print(Starship_1)
    gameplay()
    pygame.quit()