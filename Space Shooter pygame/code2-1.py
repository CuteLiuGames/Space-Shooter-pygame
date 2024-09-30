# -*- coding: utf-8 -*-
import pygame as pg
import random
import os

pg.init()


Width = 400
Height = 600


screen = pg.display.set_mode((Width,Height)) #視窗大小設定
pg.display.set_caption('hahaha game')
clock = pg.time.Clock() #建立時間元件
FPS = 30


White = (255,255,255)
Black = (0,0,0)
Blue = (0,0,255)
Red = (255,0,0)
Yellow = (255,255,0)

#載入圖片
background_img = pg.image.load(os.path.join('img', 'stars.png')).convert()
player_img = pg.image.load(os.path.join('img', 'player.png')).convert()
rock_img = pg.image.load(os.path.join('img', 'rock.png')).convert()
bullet_img = pg.image.load(os.path.join('img', 'bullet.png')).convert()

#建立藍色球
class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(player_img,(340/4,420/4))
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.center = (Width/2, Height-20)
        self.speedX=3
        self.speedY=3
    def update(self):
        key_pressed = pg.key.get_pressed()
        if key_pressed[pg.K_LEFT]:
            self.rect.x += self.speedX * -1;
        if key_pressed[pg.K_RIGHT]:
            self.rect.x += self.speedX;
            
            
        if self.rect.right >= Width:
            self.rect.right = Width
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.bottom >= Height:
            self.rect.bottom = Height
        if self.rect.top <= 0:
            self.rect.top = 0
            
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery-15)
        all_sprite.add(bullet)
        bullets.add(bullet)

#建立石頭
class Rock(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(rock_img,(45,40))
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(20,Width-20), -20)
        self.speedX=random.randint(-3,3)
        self.speedY= random.randint(3,5)
    def update(self):
        self.rect.x += self.speedX;
        self.rect.y += self.speedY;
        if self.rect.right >= Width+20:
            self.rect.center = (random.randint(20,Width-20), -20)
            self.speedX=random.randint(-3,3)
            self.speedY= random.randint(3,5)
        if self.rect.left <= -20:
            self.rect.center = (random.randint(20,Width-20), -20)
            self.speedX=random.randint(-3,3)
            self.speedY= random.randint(3,5)
        if self.rect.bottom >= Height+20:
            self.rect.center = (random.randint(20,Width-20), -20)
            self.speedX=random.randint(-3,3)
            self.speedY= random.randint(3,5)

#創造子彈
class Bullet(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((10,40))
        self.image.fill(Yellow)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedY= -10
    def update(self):
        self.rect.y += self.speedY;
        
#創造角色石頭群組

all_sprite = pg.sprite.Group()  
rocks = pg.sprite.Group()       
bullets = pg.sprite.Group() 
player = Player()

all_sprite.add(player)
for i in range(8):
    rock = Rock()
    rocks.add(rock)


#遊戲運行
speedX = 3
speedY = 3
running = True
while running:
    clock.tick(FPS)
    #取得輸入=>比如說是"按鍵控制"角色移動等
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN: #按下
            if event.key == pg.K_SPACE:
                player.shoot()
    #更新遊戲
    all_sprite.update()
    rocks.update()
    #判斷玩家是否碰到石頭
    hits = pg.sprite.spritecollide(player, rocks, True) #移除石頭
    for hit in hits: #重生石頭
        rock = Rock()
        rocks.add(rock)
    hits = pg.sprite.groupcollide(bullets, rocks, True, True) #移除石頭
    for hit in hits: #重生石頭
        rock = Rock()
        rocks.add(rock)
    #畫面顯示
    #screen.fill(Black)
    screen.blit(background_img,(0,0))#背景圖片
    all_sprite.draw(screen)
    rocks.draw(screen)
    pg.display.update()
pg.quit()