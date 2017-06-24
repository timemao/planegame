import pygame
import random
from sys import exit

pygame.init()
screen = pygame.display.set_mode((450, 800), 0, 32)
pygame.display.set_caption("plane game")
background = pygame.image.load('back.jpg').convert()
plane = pygame.image.load('plane.png').convert_alpha()

class Bullet:
    def __init__(self):
        self.x = 0
        self.y = -1
        self.image = pygame.image.load('bullet.png').convert_alpha()
        self.active=False
    def move(self):
        if self.active:
            self.y-=3
        if self.y<0:
            self.active=False
    def restart(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        self.x = mouseX - self.image.get_width() / 2
        self.y = mouseY - self.image.get_height() / 2
        self.active=True
class Enemy:
    def restart(self):
        self.x = random.randint(50, 400)
        self.y = random.randint(-200, -50)
        self.speed = random.random() + 0.1

    def __init__(self):
        self.restart()
        self.image = pygame.image.load('enemy.png').convert_alpha()

    def move(self):
        if self.y < 800:
            self.y += self.speed
        else:
            self.restart()
class Plane:
    def restart(self):
        self.x=200
        self.y=600
    def __init__(self):
        self.restart()
        self.image=pygame.image.load('plane.png').convert_alpha()
    def move(self):
        x,y=pygame.mouse.get_pos()
        x-=self.image.get_width()/2
        y-=self.image.get_height()/2
        self.x=x
        self.y=y
# hit for cross-110
def checkHit(enemy,bullet):
    if(enemy.x<bullet.x<enemy.x+enemy.image.get_width()) and (
       enemy.y<bullet.y<enemy.y+enemy.image.get_height()):
        enemy.restart()
        bullet.active=False
        return True
    return False
def checkCrash(enemy,plane):
    if(plane.x+0.7*plane.image.get_width()>enemy.x) and (
        plane.x+0.3*plane.image.get_width()<enemy.x+enemy.image.get_width()) and (
        plane.y+0.7*plane.image.get_width()>enemy.y) and(
        plane.y+0.3*plane.image.get_height()<enemy.y+enemy.image.get_height()):
        return True
    return False
enemies=[]
for i in range(5):
    enemies.append(Enemy())
plane=Plane()
bullets=[]
for ii in range(5):
    bullets.append(Bullet())
count_b=len(bullets)
index_b=0
interval_b=0

score=0
gameover=False
font=pygame.font.Font(None,32)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if gameover and event.type==pygame.MOUSEBUTTONDOWN:
            plane.restart()
            for e in enemies:
                e.restart()
            for b in bullets:
                b.active=False
            score=0
            gameover=False
    screen.blit(background, (0, 0))
    if not gameover:
      interval_b-=1
      if interval_b<0:
        bullets[index_b].restart()
        interval_b=100
        index_b=(index_b+1)%count_b
    # multi-bullets for cross108
      for b in bullets:
        if b.active:
            for e in enemies:
                if checkHit(e,b):
                    score+=100
            b.move()
            screen.blit(b.image,(b.x,b.y))
    # multi-enemy for cross109
      for e in enemies:
          if checkCrash(e,plane):
              gameover=True
          e.move()
          screen.blit(e.image,(e.x,e.y))
      plane.move()
      screen.blit(plane.image,(plane.x,plane.y))
      text = font.render("score: %d" % score, 1, (255,0,0))
      screen.blit(text, (0, 0))
    else:
        text=font.render("score: %d" % score,1,(0,0,0))
        screen.blit(text,(190,190))
    pygame.display.update()