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
boss_img = pg.image.load(os.path.join('img', 'boss.png')).convert()

#玩家命數圖示
player_img_small = pg.transform.scale(player_img, (340/10,420/10))
player_img_small.set_colorkey(Black)
pg.display.set_icon(player_img_small)
#載入爆炸圖片
expl_anim = {}
expl_anim['player'] = []
for i in range (9):
    player_expl_img = pg.image.load(os.path.join('img',f'player_expl{i}.png'))
    player_expl_img.set_colorkey(Black)
    expl_anim['player'].append(player_expl_img)

#增強物件
power_imgs = {}
power_imgs['gun'] = pg.image.load(os.path.join('img', 'gun.png')).convert()
power_imgs['shield'] = pg.image.load(os.path.join('img', 'shield.png')).convert()

#載入音樂
pg.mixer.music.load(os.path.join('sound', 'background.ogg'))
pg.mixer.music.play()#播放
shoot_sound = pg.mixer.Sound(os.path.join('sound', 'shoot.wav')) #射擊音效
expl_sound = [pg.mixer.Sound(os.path.join('sound', 'expl0.wav')), pg.mixer.Sound(os.path.join('sound', 'expl1.wav'))] #爆破音效
boss_appear_sound = pg.mixer.Sound(os.path.join('sound', 'Space Ripple.wav')) #首領出現音效
font_name = pg.font.match_font('comic sans ms')



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
    
def draw_health(surf,hp,x,y, maxV):
    Bar_Length = 100
    Bar_Height = 10
    if hp < 0:
        hp = 0

    fill = (hp/maxV) * Bar_Length
    outline_rect = pg.Rect(x,y, Bar_Length, Bar_Height)
    fill_rect = pg.Rect(x,y, fill, Bar_Height)
    bfill_rect = pg.Rect(x,y, Bar_Length, Bar_Height)
    pg.draw.rect(surf, Black, bfill_rect)
    if hp < maxV * 0.2:
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
        self.gun = 1
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
        if self.gun == 3:
          bullet = Bullet(self.rect.centerx-40, self.rect.centery-15)
          all_sprite.add(bullet)
          bullets.add(bullet)
          bullet = Bullet(self.rect.centerx, self.rect.centery-15)
          all_sprite.add(bullet)
          bullets.add(bullet)
          bullet = Bullet(self.rect.centerx+40, self.rect.centery-15)
          all_sprite.add(bullet)
          bullets.add(bullet)
        elif self.gun == 2:
          bullet = Bullet(self.rect.centerx-20, self.rect.centery-15)
          all_sprite.add(bullet)
          bullets.add(bullet)
          bullet = Bullet(self.rect.centerx+20, self.rect.centery-15)
          all_sprite.add(bullet)
          bullets.add(bullet)
        else:
          bullet = Bullet(self.rect.centerx, self.rect.centery)
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
        
class BossBullet(pg.sprite.Sprite):
    def __init__(self,x,y, speeds):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((6,20))
        self.image.fill(Red)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedX = speeds
        self.speedY= 7
    def update(self):
        global FPS
        self.rect.x += self.speedX
        self.rect.y += (self.speedY / (FPS / 30))
        
        
#創造首領
class Boss(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image =pg.transform.scale(boss_img,(98,92))
        self.image.set_colorkey(Black)
        self.hp = 3000
        self.rect = self.image.get_rect()
        self.rect.center = (Width/2, 130)
        self.speedX = 5
        self.frame = 0
        self.rate = 20
    def update(self):
        global FPS
        self.rect.x += ((self.speedX) / (FPS / 30))
        self.frame += 1
        if self.hp < 3000 * 0.2:
          self.rate = 10
        else:
          self.rate = 20
        if self.frame >= self.rate:
          self.frame = 0
          bullet = BossBullet(self.rect.centerx - 50, self.rect.centery+40, -5)
          all_sprite.add(bullet)
          boss_bullets.add(bullet)
          bullet = BossBullet(self.rect.centerx, self.rect.centery+40, 0)
          all_sprite.add(bullet)
          boss_bullets.add(bullet)
          bullet = BossBullet(self.rect.centerx + 50, self.rect.centery+40, 5)
          all_sprite.add(bullet)
          boss_bullets.add(bullet)
        if self.rect.right >= Width - 30:
            self.rect.right = Width - 30
            self.speedX *= -1
        if self.rect.left <= 30:
            self.rect.left = 30
            self.speedX *= -1
       
        
        
#寶物
class Power(pg.sprite.Sprite):
    def __init__(self,center):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(['gun', 'shield'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedY= 3
    def update(self):
        global FPS
        self.rect.y += (self.speedY/ (FPS / 30))

#爆炸
class Explosion(pg.sprite.Sprite):
    def __init__(self,center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50
    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center
        
        
        
#創造角色石頭群組

all_sprite = pg.sprite.Group()  
rocks = pg.sprite.Group()       
bosses = pg.sprite.Group()
boss_bullets = pg.sprite.Group() 
bullets = pg.sprite.Group() 
player = Player()
boss = Boss()
powers = pg.sprite.Group() 
bossIn = False

all_sprite.add(player)
for i in range(8):
    rock = Rock()
    rocks.add(rock)


#遊戲運行
Power_rate = 0.05 #掉寶率
speedX = 3
speedY = 3
running = True
score = 0
acc = 0
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
            player.gun = 1
            death_expl = Explosion(player.rect.center, 'player')
            all_sprite.add(death_expl)
            if player.lives <= 0:
              player.hp = 0
              player.lives = 0
              player.gun = 1
              running = False
    hits = pg.sprite.spritecollide(player, boss_bullets, True) #移除石頭
    for hit in hits: #重生石頭
        player.hp -= 10
        if player.hp <= 0:
            player.hp = 100
            player.lives -= 1
            player.gun = 1
            death_expl = Explosion(player.rect.center, 'player')
            all_sprite.add(death_expl)
            if player.lives <= 0:
              player.hp = 0
              player.lives = 0
              player.gun = 1
              running = False
    hits = pg.sprite.groupcollide(bosses, bullets, False, True) #移除石頭
    for hit in hits: #重生石頭     
      hit.hp -= 40
      if hit.hp <= 0:
          score += 1000
          all_sprite.remove(boss_bullets)
          boss_bullets.remove(boss_bullets)
          all_sprite.remove(boss)
          bosses.remove(boss)
          bossIn = False
          for i in range(8):
              rock = Rock()
              rocks.add(rock)
    hits = pg.sprite.groupcollide(rocks, bullets, True, True) #移除石頭
    for hit in hits: #重生石頭
        score += hit.radius
        acc += hit.radius
        random.choice(expl_sound).play()
        rock = Rock()
        rocks.add(rock)
        if acc >= 10000:
            acc = 0
            boss_appear_sound.play()
            rocks.remove(rocks)
            all_sprite.remove(rocks)
            all_sprite.add(boss)
            bosses.add(boss)
            boss.hp = 3000
            boss.frame = 0
            bossIn = True
        elif random.random() <= Power_rate:
          power = Power(hit.rect.center)
          all_sprite.add(power)
          powers.add(power)
        
    hits = pg.sprite.spritecollide(player, powers, True) #移除石頭
    for hit in hits: #增加血量
       if hit.type == 'gun':
           player.gun += 1
           if player.gun >= 3:
               player.gun = 3
       else:
          player.hp += 50
          if player.hp > 100:
            player.hp = 100
        
    #畫面顯示
    #screen.fill(Black)
    screen.blit(background_img,(0,0))#背景圖片
    all_sprite.draw(screen)
    rocks.draw(screen)
    draw_text(screen, str(score), 20, Width/2, 20)
    draw_health(screen, player.hp, 5, 10, 100)
    if bossIn == True:
       draw_health(screen, boss.hp, boss.rect.x, 60, 3000)
    draw_lives(screen, player.lives, player_img_small, Width-40, 5)
    pg.display.update()
pg.quit()