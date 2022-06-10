#Создай собственный Шутер!
from pygame import*
from random import randint
from time import time as timer
#шрифты
font.init()
font2 = font.SysFont("Arial", 36)

#спрайты
img_bg = "galaxy.png"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_enemy2 = "ufo2.png"
img_bullet = "bullet.png"
img_bullet2 = "heartFull.png"
img_bullet3 = "BebrikIco.png"
img_ast = "asteroid.png"

"""Переменные"""
score = 0
lost = 0
life = 3

'''Классы'''
#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, player_w, player_h, player_speed):
        sprite.Sprite.__init__(self)
        #Каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (player_w, player_h))
        self.speed = player_speed
        #Каждый спрайт должен хранить свойство rect - прямоугольник в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #метод отрисовки спрайта
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
    
    def fire2(self):
        bullet2 = Bullet(img_bullet2, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet2)

    def fire3(self):
        bullet3 = Bullet(img_bullet3, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet3)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Enemy2(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Aster(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0



class Boss(GameSprite):
    pass

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
'''Игровая сцена'''
win_width = 700
win_height = 800
window = display.set_mode((win_width,win_height))
display.set_caption('MAZE')
background =  transform.scale(image.load(img_bg), (win_width, win_height))

'''Персонажи игры'''
hero = Player(img_hero,5, win_height - 90, 80, 80, 4)

monsters = sprite.Group()
for i in range(1, 3):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)

monsters2 = sprite.Group()
for i in range(1, 3):
    monster2 = Enemy2(img_enemy2, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
    monsters2.add(monster2)

asteroids = sprite.Group()
for l in range(1, 3):
    asteroid = Aster(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1,7))
    asteroids.add(asteroid)


bullets = sprite.Group()

'''Игровой цикл'''
game = True
finish = False

clock = time.Clock()
FPS = 60
'''Музыка'''
mixer.init()
bgmusic = mixer.Sound("space.ogg")
fire_sound = mixer.Sound("fire.ogg")

font.init()
font = font.SysFont("Comic Sans MS", 45)
win = font.render("ТЫ ПОБЕДИЛ!", True, (255,215,0))
lose = font.render("ТЫ ПРОИГРАЛ(((((", True, (180,0,0))
#mixer.music.load('ASAPR.ogg')
#mixer.music.play()
rel_time = False
num_fire = 0

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    hero.fire()
                if num_fire >= 5 and rel_time == False:
                    num_fire = num_fire + 1
                    last_time = timer()
                    rel_time = True
            elif e.key == K_TAB:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    hero.fire2()
                if num_fire >= 5 and rel_time == False:
                    num_fire = num_fire + 1
                    last_time = timer()
                    rel_time = True
            elif e.key == K_CAPSLOCK:
                if num_fire < 5 and rel_time == False:
                    fire_sound.play()
                    hero.fire3()
                if num_fire >= 5 and rel_time == False:
                    num_fire = num_fire + 1
                    last_time = timer()
                    rel_time = True


    if not finish:

        window.blit(background,(0, 0))
        #отрисовка персов
        hero.reset()
        hero.update()
        monsters.update()
        monsters2.update()
        bullets.update()
        asteroids.update()


        counter = font.render("убито врагов:" + str(score), True, (180,0,0))
        counter2 = font.render("пропущено врагов:" + str(lost), True, (180,0,0))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        collides2 = sprite.groupcollide(monsters2, bullets, True, True)
        #перезарядка
        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reloadd = font.render("подожди, перезарядка...", 1, (150,0,0))
                window.blit(reloadd, (150, 600))
            else:
                num_fire = 0
                rel_time = False


        ###
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        for c in collides2:
            score = score + 1
            monster2 = Enemy2(img_enemy2, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            monsters2.add(monster2)

        window.blit(counter, (0,0))
        window.blit(counter2, (0,40))

        if life == 3:
            life_color = (0, 150, 0)
        if life == 3:
            life_color = (150, 150, 0)
        if life == 3:
            life_color = (150, 0, 0)
        
        text_life = font.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        monsters.draw(window)
        monsters2.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        if sprite.spritecollide(hero, monsters, False) or sprite.spritecollide(hero, monsters2, False) or sprite.spritecollide(hero, asteroids, False):
            life -= 1
        if lost >= 3 or life <= 0:
            finish = True
            window.blit(lose, (200,200))

        if score == 20:
            finish = True
            window.blit(win, (200,200))
        
        display.update()
    
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for k in monsters2:
            k.kill()
        for a in asteroids:
            a.kill()
        
        time.delay(3000)
        for i in range(1, 3):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)
        for i in range(1, 3):
            monster2 = Enemy2(img_enemy2, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster2)
        for l in range(1, 3):
            asteroid = Aster(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1,7))
            asteroids.add(asteroid)

    clock.tick(FPS)