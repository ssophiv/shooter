#Создай собственный Шутер!
from random import randint
from pygame import *
from time import time as timer
window = display.set_mode((700, 500))

view = transform.scale(image.load("pngwing.com (6).png"), (700, 500))

mixer.init()
mixer.music.load('Space-Jazz.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')
mixer.music.set_volume(0.1)

font.init()
font_1 = font.SysFont('Arial', 35)
font_2 = font.SysFont('Arial', 80)
win = font_2.render('YOU WIN!', True, (0,255,0))
lose = font_2.render('YOU LOSE!', True, (255,0,0))

lost = 0
score = 0
life = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, randint(1,3))
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80,620)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()


ship = Player('pngwing.com (4).png', 10, 400, 80, 100, 4)

enemies = sprite.Group()
for i in range(5):
    enemy = Enemy('pngwing.com (7) (2).png', randint(80,620), -20, 70, 90, randint(1,3))
    enemies.add(enemy)

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png',randint(80,620), -20, 30, 40, 2)
    asteroids.add(asteroid)



game = True
finish = False
clock = time.Clock()
FPS = 60

num_fire = 0
rel_time = False
while game:
    for e in event.get():
        if e.type == QUIT:
            exit()
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time != True:
                    ship.fire()
                    fire_sound.play()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(view,(0,0))
        ship.reset()
        ship.update()

        enemies.draw(window)
        enemies.update()

        bullets.draw(window)
        bullets.update()

        asteroids.draw(window)
        asteroids.update()

        text = font_1.render(f'Счёт: {score}',True,(255,255,255))
        window.blit(text,(10,20))
        text_lose = font_1.render(f'Пропущено: {lost}',True,(255,255,255))
        window.blit(text_lose,(10,50))

        collides = sprite.groupcollide(enemies, bullets, True, True)
        for c in collides:
            score += 1
            enemy = Enemy('pngwing.com (7).png', randint(80,620), -20, 70, 90, randint(1,5))
            enemies.add(enemy)
        
        if sprite.spritecollide(ship, enemies, False) or sprite.spritecollide(ship, asteroids, False):
            finish = True
            window.blit(lose,(200,200))
        
        if score > 9:
            finish = True
            window.blit(win,(200,200))

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font_2.render('перезаряжаюсь', True, (150,0,0))
                window.blit(reload,(200,400))
            else:
                num_fire = 0
                rel_time =False

    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        rel_time =False
        for b in bullets:
            b.kill()
        for e in enemies:
            e.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range(5):
            enemy = Enemy('pngwing.com (7).png', randint(80,620), -20, 70, 90, randint(1,5))
            enemies.add(enemy)
        for i in range(3):
            asteroid = Enemy('asteroid.png',randint(80,620), -20, 30, 40, 2)
            asteroids.add(asteroid)
    display.update()
    clock.tick(FPS)
