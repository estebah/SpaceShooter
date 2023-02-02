import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

WIDTH = 900
HEIGHT = 600
screen_size = (WIDTH, HEIGHT)
window = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Space Shooter')
icon = pygame.image.load('./img/spaceship.png')
pygame.display.set_icon(icon)

background = pygame.image.load('./img/space.png')
clock = pygame.time.Clock()

explosion_sound = pygame.mixer.Sound('./audio/explosion.wav')
shoot_sound = pygame.mixer.Sound('./audio/shoot.wav')

class Starship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('./img/spaceship.png')
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.x = 450
        self.rect.y = 540
        self.speed = 0
        self.score = 0
        self.lives = 3

    def update(self):
        self.speed = 0

        key = pygame.key.get_pressed()

        if key[pygame.K_a]:
            self.speed = -5

        elif key[pygame.K_d]:
            self.speed = 5

        self.rect.x += self.speed

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.left < 0:
            self.rect.left = 0

        if self.lives == 0:
            self.kill()
            pygame.quit()
            sys.exit()

        if pygame.sprite.spritecollide(self, asteroid_group, True):
            starship.lives -= 1

    def shoot(self):
        missile = Missile(starship.rect.x, starship.rect.y)
        missile_group.add(missile)
        shoot_sound.play()
        shoot_sound.fadeout(1000)
        shoot_sound.set_volume(0.1)

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('./img/asteroid.png')
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(-100,900)
        self.rect.y = random.randint(-150, 100)
        self.speed_x = random.randint(1, 8)
        self.speed_y = random.randint(4, 8)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
            self.rect.x = random.randint(-100,900)
            self.rect.y = random.randint(-150, -100)
            self.speed_x = random.randint(-8, 8)
            self.speed_y = random.randint(4, 10)


        if pygame.sprite.spritecollide(self, missile_group, True):
            self.kill
            starship.score += 1
            explosion_sound.play()
            self.rect.x = random.randint(-100,900)
            self.rect.y = random.randint(-150, -100)
            self.speed_x = random.randint(-8, 8)
            self.speed_y = random.randint(4, 10)

class Missile(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load('./img/missile.png')
        self.image = pygame.transform.scale(self.image, (30,30))
        self.rect = self.image.get_rect()
        self.rect.x = x + 10
        self.rect.y = y
        self.speed_y = 5

    def update(self):
        self.rect.y -= self.speed_y

        if self.rect.y > 0:
            self.kill

def write_text(text, x, y):
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render(text, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    window.blit(text, text_rect)

starship_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()
missile_group = pygame.sprite.Group()

starship = Starship()
starship_group.add(starship)

for ast in range(10):
    asteroid = Asteroid()
    asteroid_group.add(asteroid)

missile_cooldown = 100
last_missile = pygame.time.get_ticks() - missile_cooldown

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - last_missile > missile_cooldown:
                starship.shoot()
                last_missile = current_time

    window.blit(background, (0,0))

    starship_group.update()
    starship_group.draw(window)

    asteroid_group.update()
    asteroid_group.draw(window)

    missile_group.update()
    missile_group.draw(window)

    write_text(f'Lives: {starship.lives}', 850,20)
    write_text(f'Score: {starship.score}', 50,20)

    clock.tick(60)
    pygame.display.update()
