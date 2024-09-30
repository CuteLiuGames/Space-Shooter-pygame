# -*- coding: utf-8 -*-
import pygame as pg

pg.init()
screen = pg.display.set_mode((600,400)) #視窗大小設定
pg.display.set_caption('hahaha game')

#建立畫布bg
bg = pg.Surface(screen.get_size()).convert()
bg.fill((255,255,255)) #(R,G,B)

screen.blit(bg, (0,0)) # (放入顯示的東西,座標
pg.display.update()



running = True
while running:
    #取得輸入=>比如說是"按鍵控制"角色移動等
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    #更新遊戲
    
    #畫面顯示
pg.quit()