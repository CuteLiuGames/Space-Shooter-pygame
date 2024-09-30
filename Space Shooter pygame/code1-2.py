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
#建立畫布bg
bg = pg.Surface(screen.get_size()).convert()
bg.fill(White) #(R,G,B)


ball = pg.Surface((70,70))
ball.fill(White)
pg.draw.circle(ball, Blue,(35,35),35,0)
rect = ball.get_rect()
rect.center= (Width/2, Height/2)
x,y = rect.topleft



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
    x += speedX
    rect.topleft = (x,y)
    if rect.right >= Width or rect.left <= 0:
        speedX *= -1
    y += speedY
    rect.topleft = (x,y)
    if rect.bottom >= Height or rect.top <= 0:
        speedY *= -1
        
    #畫面顯示
    screen.blit(bg, (0,0)) # (放入顯示的東西,座標
    screen.blit(ball, (x,y)) # (放入顯示的東西,座標
    pg.display.update()
pg.quit()