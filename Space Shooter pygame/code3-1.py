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
Green = (0,255,0)

#載入圖片
background_img = pg.image.load(os.path.join('img', 'stars.png')).convert()
player_img = pg.image.load(os.path.join('img', 'player.png')).convert()
rock_img = pg.image.load(os.path.join('img', 'rock.png')).convert()
bullet_img = pg.image.load(os.path.join('img', 'bullet.png')).convert()
power_img = pg.image.load(os.path.join('img', 'power.png')).convert()

#玩家命數圖示
player_img_small = pg.transform.scale(player_img, (340/10,420/10))
player_img_small.set_colorkey(Black)
pg.display.set_icon(player_img_small)
#載入音樂
pg.mixer.music.load(os.path.join('sound', 'background.ogg'))
pg.mixer.music.play()#播放
shoot_sound = pg.mixer.Sound(os.path.join('sound', 'shoot.wav')) #射擊音效
expl_sound = [pg.mixer.Sound(os.path.join('sound', 'expl0.wav')), pg.mixer.Sound(os.path.join('sound', 'expl1.wav'))] #爆破音效

font_name = pg.font.match_font('comic sans ms')


Bar_Length = 100
Bar_Height = 10
fillOff = Bar_Length

def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, White)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surf.blit(text_surface,text_rect)

def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x - i * 32
        img_rect.y = y
        surf.blit(img, img_rect)
    
def draw_health(surf,hp,x,y):
    global fillOff
    global Bar_Length
    global Bar_Height
    if hp < 0:
        hp = 0

    fill = (hp/100) * Bar_Length
    outline_rect = pg.Rect(x,y, Bar_Length, Bar_Height)
    fillOff += (fill - fillOff) / (2.5 * (FPS / 30))
    fill_rect = pg.Rect(x,y, fillOff, Bar_Height)
    bfill_rect = pg.Rect(x,y, Bar_Length, Bar_Height)
    pg.draw.rect(surf, Black, bfill_rect)
    if hp < 20:
      pg.draw.rect(surf, Red, fill_rect)
    else:
      pg.draw.rect(surf, Green, fill_rect)
    pg.draw.rect(surf, White, outline_rect,2)
    
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
        self.hp = 100
        self.lives = 3
    def update(self):
        global FPS
        key_pressed = pg.key.get_pressed()
        if key_pressed[pg.K_LEFT]:
            self.rect.x += ((self.speedX * -1) / (FPS / 30))
        if key_pressed[pg.K_RIGHT]:
            self.rect.x += ((self.speedX) / (FPS / 30))
            
            
        if self.rect.right >= Width:
            self.rect.right = Width
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.bottom >= Height:
            self.rect.bottom = Height
        if self.rect.top <= 0:
            self.rect.top = 0
            
    def shoot(self):
        shoot_sound.play()
        bullet = Bullet(self.rect.centerx, self.rect.centery-15)
        all_sprite.add(bullet)
        bullets.add(bullet)

#建立石頭
class Rock(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.radius = random.randrange(5,75)
        self.image =pg.transform.scale(rock_img,(self.radius,self.radius))
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(20,Width-20), -20)
        self.speedX = random.randint(-3,3)
        self.speedY = random.randint(3,5)
    def update(self):
        global FPS
        self.rect.x += (self.speedX / (FPS / 30))
        self.rect.y += (self.speedY / (FPS / 30))
        if self.rect.right >= Width+40:
            self.rect.center = (random.randint(20,Width-20), -20)
            self.speedX= random.randint(-3,3)
            self.speedY= random.randint(3,5)
        elif self.rect.left <= -40:
            self.rect.center = (random.randint(20,Width-20), -20)
            self.speedX=random.randint(-3,3)
            self.speedY= random.randint(3,5)
        elif self.rect.bottom >= Height+40:
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
        global FPS
        self.rect.y += (self.speedY / (FPS / 30))
        
#寶物
class Power(pg.sprite.Sprite):
    def __init__(self,center):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(power_img,(17,17))
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedY= 3
    def update(self):
        global FPS
        self.rect.y += (self.speedY/ (FPS / 30))
        
        
#創造角色石頭群組

all_sprite = pg.sprite.Group()  
rocks = pg.sprite.Group()       
bullets = pg.sprite.Group() 
player = Player()
powers = pg.sprite.Group() 

all_sprite.add(player)
for i in range(8):
    rock = Rock()
    rocks.add(rock)


#遊戲運行
Power_rate = 0.1 #掉寶率
speedX = 3
speedY = 3
running = True
score = 0
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
        player.hp -= (hit.radius / 2)
        rock = Rock()
        rocks.add(rock)
        if player.hp <= 0:
            player.hp = 100
            player.lives -= 1
            if player.lives <= 0:
              player.hp = 0
              player.lives = 0
              running = False
    hits = pg.sprite.groupcollide(rocks, bullets, True, True) #移除石頭
    for hit in hits: #重生石頭
        score += hit.radius
        random.choice(expl_sound).play()
        rock = Rock()
        rocks.add(rock)
        if random.random() <= Power_rate:
          power = Power(hit.rect.center)
          all_sprite.add(power)
          powers.add(power)
    hits = pg.sprite.spritecollide(player, powers, True) #移除石頭
    for hit in hits: #增加血量
       player.hp += 50
       if player.hp > 100:
           player.hp = 100
        
    #畫面顯示
    #screen.fill(Black)
    screen.blit(background_img,(0,0))#背景圖片
    all_sprite.draw(screen)
    rocks.draw(screen)
    draw_text(screen, str(score), 20, Width/2, 20)
    draw_health(screen, player.hp, 5, 10)
    draw_lives(screen, player.lives, player_img_small, Width-40, 5)
    pg.display.update()
pg.quit()