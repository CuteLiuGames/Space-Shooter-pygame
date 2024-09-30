# -*- coding: utf-8 -*-
import pygame as pg

pg.init()


Width = 600
Height = 400


screen = pg.display.set_mode((Width,Height)) #視窗大小設定
pg.display.set_caption('hahaha game')
clock = pg.time.Clock() #建立時間元件
FPS = 30


White = (255,255,255)
Blue = (0,0,255)

#建立藍色球
class Box(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((70,70))
        self.image.fill(Blue)
        self.rect = self.image.get_rect()
        self.rect.center = (Width/2, Height/2)
        self.speedX=3
        self.speedY=3
    def update(self):
        self.rect.x += self.speedX
        if self.rect.right >= Width or self.rect.left <= 0:
            self.speedX *= -1
        self.rect.y += self.speedY
        if self.rect.bottom >= Height or self.rect.top <= 0:
            self.speedY *= -1


all_sprite = pg.sprite.Group()        
box = Box()
all_sprite.add(box)



speedX = 3
speedY = 3
running = True
while running:
    clock.tick(FPS)
    #取得輸入=>比如說是"按鍵控制"角色移動等
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    #更新遊戲
    all_sprite.update()
        
    #畫面顯示
    screen.fill(White)
    all_sprite.draw(screen)
    
    pg.display.update()
pg.quit()