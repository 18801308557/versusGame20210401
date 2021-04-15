import random
import pygame
from positionFunc import *
class gun():
    def __init__(self,screen,target):
        #设置枪的默认位置
        self.x=50
        self.y=50
        #设置要显示内容的窗口
        self.screen=screen
        #设置枪的模型图片
        self.imageName=""
        self.image=pygame.image.load(self.imageName).convert()
        #储存枪发射的所有子弹
        self.bulllist=[]

        self.visible = True  # 是否可见
        self.HP = 100  # 初始生命值
        self.target = target  # 攻击目标
        self.shoot = False  # 是否发射，发射就new一个bullet
        self.bulletNum=100#初始库存为100
        self.R = 120  # 概率半径
        self.hitPropable = 0  # 命中概率

    #绘制枪
    def display(self):
        self.screen.blit(self.image,self.x,self.y)
        for bullet in self.bulllist:
            bullet.display()#显示一个子弹的位置
            bullet.movePosition()#让一个子弹移动，下一次再显示的时候就会看到子弹再移动

    #是否可移动枪？？
    def moveLeft(self):
        self.x-=10

    def moveRight(self):
        self.x+=10

    def moveUp(self):
        self.y-=10

    def moveDown(self):
        self.y+=10

    #发射子弹
    def lauchBullet(self):
        newBullet=bullet(self.screen,self.x,self.y,)
        self.bulllist.append(newBullet)
        self.bulletNum-=1

    #计算命中概率
    def calPossibility(self):
        distance=distanceCal(self.x,self.y,self.target.curr_pos[0],self.target.cur_pos[1])
        if distance<=self.R:
            self.hitPropable=0.5
        elif distance>self.R and distance<=self.R*2:
            self.hitPropable = 0.4
        elif distance>self.R*2 and distance <= self.R*3:
            self.hitPropable=0.05
        else:
            self.hitPropable=0.01



class bullet():
    def __init__(self,screen,x,y):
        # 主屏幕大小,显示内容的窗口
        self.main_scene = screen
        #设置子弹图片
        self.image=pygame.image.load("").convert()
        #子弹的位置
        self.x+=10
        self.y-=10

        self.name = "bullet"  # 名称
        self.speed = 10  # 移动速度

        # 移动函数
    def movePosition(self):
        if not self.visible:
            return
        #朝某个方向移动
        self.x-=self.speed
        # 子弹超出屏幕范围，则不可见
        if self.x < 0 or self.y < 0 or self.x > self.main_scene.size[0] or self.y > self.main_scene.size[1]:
            self.visible = False

    def display(self):
        self.main_scene.blit(self.image, (self.x, self.y))












