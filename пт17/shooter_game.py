import pygame
import random

pygame.init()
window = pygame.display.set_mode((500, 500))

background = pygame.image.load('galaxy.jpg')
background = pygame.transform.scale(background, (500, 500))
window.blit(background, (0, 0))
clock = pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.music.load('space.ogg')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(999)

fire = pygame.mixer.Sound('fire.ogg')
fire.set_volume(0.3)
fire.play()


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x + self.speed > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x + self.speed < 430:
            self.rect.x += self.speed

    def update_2(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x + self.speed > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x + self.speed < 430:
            self.rect.x += self.speed

lost = 0


class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 500:
            lost += 1
            self.rect.y = -50
            self.rect.x = random.randint(50, 450)


class Stone(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = -50
            self.rect.x = random.randint(50, 450)



class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()


hero = Player('rocket.png', 220, 400, 5, 80, 100)

ufos = pygame.sprite.Group()
bullets = pygame.sprite.Group()
for i in range(5):
    enemy1 = Enemy('ufo.png', random.randint(50, 450), random.randint(-250, -50), random.randint(1, 5), 80, 50)
    ufos.add(enemy1)

stones = pygame.sprite.Group()
for i in range(2):
    stone1 = Stone('asteroid.png', random.randint(0, 450), random.randint(-250, -50), random.randint(1, 3), 65, 65)
    stones.add(stone1)

pygame.font.init()
font1 = pygame.font.SysFont(None, 36)
font2 = pygame.font.SysFont(None, 72)

txt_win = font2.render('You win!', True, (0, 255, 0))
txt_lose = font2.render('You lose!', True, (255, 0, 0))

score = 0

btn_solo = GameSprite('btn_solo.png', 200, 200, 0, 100, 50)
btn_duo = GameSprite('btn_duo.png', 175, 300, 0, 150, 50)


screen = 'menu'
is_duo = False
is_win = 0
game = True
while game:
    window.blit(background, (0, 0))
    if screen == 'menu':
        btn_solo.reset()
        btn_duo.reset()

        # match is_win:
        #     case 1:
        #         window.blit(txt_lose, (150, 50))
        #     case 2:
        #         window.blit(txt_win, (150, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     x, y = event.pos
            #     if btn_solo.rect.collidepoint(x, y):
            #         screen = 'main'
            #     if btn_duo.rect.collidepoint(x, y):
            #         screen = 'main'
            #         hero2 = Player('rocket.png', 300, 400, 5, 80, 100)
            #         is_duo = True

        pygame.display.update()
    if screen == 'main':
        pygame.display.update()
        clock.tick(60)
        text_lost = font1.render(f'Пропущено: {lost}', True, (255, 255, 255))
        window.blit(text_lost, (10, 50))

        text_score = font1.render(f'Рахунок: {score}', True, (255, 255, 255))
        window.blit(text_score, (10, 10))

        sprites = pygame.sprite.groupcollide(bullets, ufos, True, True)
        for i in sprites:
            score += 1
            enemy1 = Enemy('ufo.png', random.randint(50, 450), random.randint(-250, -50), random.randint(1, 5), 80, 50)
            ufos.add(enemy1)

        pygame.sprite.groupcollide(bullets, stones, True, False)
        lose = pygame.sprite.spritecollide(hero, stones, False)
    

        ufos.draw(window)
        ufos.update()
        bullets.draw(window)
        bullets.update()
        stones.draw(window)
        stones.update()

        hero.reset()
        hero.update()
        if is_duo:
            hero2.reset()
            hero2.update_2()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet1 = Bullet('bullet.png', hero.rect.centerx, hero.rect.y, 15, 15, 20)
                    bullets.add(bullet1)
                    # fire.play()
                if event.key == pygame.K_UP and is_duo:
                    bullet1 = Bullet('bullet.png', hero2.rect.centerx, hero2.rect.y, 15, 15, 20)
                    bullets.add(bullet1)
                    # fire.play()













