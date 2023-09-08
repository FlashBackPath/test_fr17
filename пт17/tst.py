import random

import pygame

pygame.init()
window = pygame.display.set_mode((500, 500))

background = pygame.image.load('galaxy.jpg')
background = pygame.transform.scale(background, (500, 500))
window.blit(background, (0, 0))
clock = pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.music.load('space.ogg')
pygame.mixer.music.set_volume(0.3)
# pygame.mixer.music.play()

fire = pygame.mixer.Sound('fire.ogg')
fire.set_volume(0.3)
# fire.play()


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x-self.speed > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x+self.speed < 420:
            self.rect.x += self.speed

lost = 0

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed

        if self.rect.y >= 500:
            self.rect.y = -50
            self.rect.x = random.randint(0, 450)
            lost += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


class Stone(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y >= 500:
            self.rect.y = random.randint(-250, -50)
            self.rect.x = random.randint(0, 450)


hero = Player('rocket.png', 5, 400, 10, 80, 100)
enemies = pygame.sprite.Group()
for i in range(5):
    enemy1 = Enemy('ufo.png', random.randint(0, 450), random.randint(-250, -50), random.randint(1, 6), 80, 50)
    enemies.add(enemy1)

bullets = pygame.sprite.Group()

asteroids = pygame.sprite.Group()
for i in range(2):
    stone1 = Stone('asteroid.png', random.randint(0, 450), random.randint(-250, -50), random.randint(1, 3), 65, 65)
    asteroids.add(stone1)

font1 = pygame.font.Font(None, 36)
font2 = pygame.font.Font(None, 86)
text_winR = font2.render('YOU WIN!', True, (0, 255, 0))
text_loseR = font2.render('YOU LOSE!', True, (255, 0, 0))
win = 0
game = True
while game:
    window.blit(background, (0, 0))

    text_lose = font1.render(f'Пропущено: {lost}', True, (255, 255, 255))
    window.blit(text_lose, (10, 10))

    text_win = font1.render(f'Збито: {win}', True, (255, 255, 255))
    window.blit(text_win, (10, 50))

    if win >= 10:
        window.blit(text_winR, (110, 200))
    elif lost >= 3:
        window.blit(text_loseR, (100, 200))
    else:
        enemies.update()
        asteroids.update()
        hero.update()
        bullets.update()



    enemies.draw(window)

    asteroids.draw(window)

    hero.reset()

    bullets.draw(window)

    # 1 спосіб
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        b1 = Bullet('bullet.png', hero.rect.centerx-6, hero.rect.y, 20, 15, 20)
        bullets.add(b1)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit()
        # 2 спосіб
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                b1 = Bullet('bullet.png', hero.rect.centerx, hero.rect.y, 20, 15, 20)
                bullets.add(b1)

    if pygame.sprite.groupcollide(bullets, enemies, True, True):
        # win += 1
        enemy1 = Enemy('ufo.png', random.randint(0, 450), random.randint(-250, -50), random.randint(1, 6), 80, 50)
        enemies.add(enemy1)

    pygame.display.update()
    clock.tick(60)
