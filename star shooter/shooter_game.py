from pygame import *
from random import *
window = display.set_mode((700, 500))
display.set_caption("star shooter")
speed = 6
global crashed,missed,missed_one,num_fire,rel_time,start_time
crashed = 0
missed = 0
missed_one = 0
life = 3
num_fire = 0
rel_time = False
start_time = 0
class Game_sprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,scale_x,scale_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(scale_x,scale_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x,self.rect.y))
class Bullet(Game_sprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -32:
            self.kill()
class Player(Game_sprite):
    def fire(self):
        bullet = Bullet("bullet.png",  self.rect.centerx, self.rect.top, 20, 30,20)
        bullets.add(bullet)
    def update(self):
        global num_fire, rel_time,start_time
        key_pressed = key.get_pressed()
        if not rel_time:
            if num_fire == 30:
                rel_time = True
                start_time = time.get_ticks()
                num_fire = 0
        if key_pressed[K_LEFT] and self.rect.x >= 2:
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.x  <= 598:
            self.rect.x += self.speed
        if key_pressed[K_UP] and not rel_time:
            self.fire()
            num_fire += 1
class Enemy(Game_sprite):
    def update(self):
        global missed,missed_one
        self.rect.y += self.speed
        if self.rect.y > 510:
            missed += 1
            missed_one += 1
            self.rect.y = -70
            self.rect.x = randint(0,600)
            self.speed = randint(1,2)
class Asteroid(Game_sprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 510:
            self.rect.y = -70
            self.rect.x = randint(0,600)
            self.speed = randint(2,4)
background = transform.scale(image.load("galaxy.jpg"),(700, 500))
ufos = sprite.Group()
asts = sprite.Group()
bullets = sprite.Group()
hero = Player("rocket.png", 325, 362, 100, 135, speed)
font.init()
font = font.Font(None,50)
win = font.render("You Win", 1,(0,255,0))
loose = font.render("You Loose", 1,(255,0,0))
crash = font.render("счёт:"+str(crashed),1,(255,255,255))
miss = font.render("пропущено:"+str(missed_one),1,(255,255,255))
lifes = font.render(str(life),1,(0,255,0))
rel_str = font.render("идёт перезарядка",1,(255,0,0))
clock = time.Clock()
game_rendering = True
play_time = True
while game_rendering:
    for e in event.get():
        if e.type == QUIT:
            game_rendering = False
    if play_time:
        current_time = time.get_ticks()
        while len(ufos) < 3:
            ufo = Enemy("ufo.png", randint(0,600),-70,100, 70, randint(1,2))
            ufos.add(ufo)
        while len(asts) < 2:
            ast = Asteroid("asteroid.png",randint(0,600),-70,100, 70, randint(4,5))
            asts.add(ast)
        if sprite.groupcollide(ufos,bullets,True,True):
            crashed += 1
            ufo = Enemy("ufo.png", randint(0,600),-70,100, 70, randint(1,2))
            ufos.add(ufo)
        if sprite.groupcollide(asts,bullets,False,True):
            pass
        
        if sprite.spritecollide(hero,ufos,True) or  sprite.spritecollide(hero,asts,True) or missed >= 3:
            life -= 1
        if missed >=3:
            missed = 0
        fps = 60
        clock.tick(fps)
        
                  
        if life == 3:
            color_l = (0,255,0)
        if life == 2:
            color_l = (200,170,0)
        if life < 2:
            color_l = (255,0,0)
        lifes = font.render(str(life),1,(color_l))
        crash = font.render("счёт"+str(crashed),1,(255,255,255))
        miss = font.render("пропущено"+str(missed_one),1,(255,255,255))
        window.blit(background, (0,0))
        window.blit(crash,(0,0))
        window.blit(miss,(0,30))
        window.blit(lifes,(650,0))
        if crashed >= 10:
            window.blit(win,(270,230))  
            play_time = False
        if life == 0:
            window.blit(loose,(270,230))
            play_time = False
        if current_time-start_time >= 1000:
            rel_time = False
        elif rel_time:
            window.blit(rel_str,(300,470))
        hero.update()
        hero.reset()
        asts.update()
        asts.draw(window)
        ufos.update()
        ufos.draw(window)
        bullets.update()
        bullets.draw(window)
    display.update()