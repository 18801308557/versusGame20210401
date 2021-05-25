import pygame
import math
import time
from positionFunc import *
from mobile_carrier.solider import *

class bullet():
    def __init__(self,oriX,oriY,tarX,tarY): #子弹初始位置与往哪移动
        # 主屏幕大小,显示内容的窗口
        #self.main_scene = screen
        #设置子弹图片
        self.image=pygame.image.load('./source/img/menu/bullet1.png').convert()
        #子弹的当前位置
        self.currentX=oriX*32
        self.currentY=oriY*32
        #攻击目标点
        self.targetX=tarX*32
        self.targetY=tarY*32

        # 子弹打中目标位置需要移动的xy值
        self.delt_x = self.targetX-self.currentX
        self.delt_y = self.targetY - self.currentY
        # 获得子弹矩形(x, y, width, height)，操作矩形进行旋转
        self.rect = self.image.get_rect()
        self.rect.x=self.currentX
        self.rect.y=self.currentY
        self.ori_X = oriX*32
        self.ori_Y = oriY*32
        # 移动速度
        self.speed = 2
        self.direction=0#表示方向
        self.live = True # 子弹是否有效

    #设置图片位置
    def setRectPos(self):
        self.rect.x = self.currentX
        self.rect.y= self.currentY
        #self.rect.center=(self.currentX,self.currentY)

    #确定攻击方向
    def getDirection(self):
        if self.currentX < self.targetX and self.currentY == self.targetY:  # 起点在终点的左上
            self.direction=1#向右
            #print("向右移动")
        if self.currentX > self.targetX and self.currentY == self.targetY:  # 起点在终点的左上
            self.direction=2#向左
            #print("向左移动")
        if self.currentX == self.targetX and self.currentY > self.targetY:  # 起点在终点的左上
            self.direction=3#向下
            #print("向下移动")
        if self.currentX == self.targetX and self.currentY < self.targetY:  # 起点在终点的左上
            self.direction=4#向上
            #print("向上移动")

    def judgeBullet(self):#判断子弹是否击中
        if self.currentX==self.targetX and self.currentY==self.targetY:
            return True
        else:
            return False

    #wzq 新的判断是否击中
    def hit_target(self,target):
        if abs(self.currentX-target.x)<32 and abs(self.currentY-target.y)<32:
            self.live =False
            target.health -= 20 #对应减少多少血量
            if target.health<= 0:
                target.live = False

    # 显示子弹
    def displayBullet(self,main_scene):
        main_scene.blit(self.image, (self.currentX, self.currentY))
        #print("显示:", self.currentX, self.currentY, self.targetX, self.targetY)


    def moveBullet(self):
        self.getDirection()
        #print("方向=", self.direction)
        #print("起点：(", self.currentX, ",", self.currentY, ");终点：", self.targetX, ",", self.targetY, ")")
        # 移动 1:右 2 左 3 下  4上
        #移动过程中判断是否有没有击中，击中的话则不存活并返回
        if self.currentX == self.targetX and self.currentY == self.targetY:
            self.live = False
            return
        #y方向没有变化，x方向移动
        if self.delt_y==0:
            #print("1")
            if self.targetX>self.ori_X:
                self.currentX += self.speed
                if self.currentX>self.targetX:
                    self.currentX=self.targetX
            else:
                self.currentX -= self.speed
                if self.currentX<self.targetX:
                    self.currentX=self.targetX
        #x方向没有变化，y方向移动
        elif self.delt_x==0:
            #print("2")
            if self.targetY>self.ori_Y:
                self.currentY += self.speed
                if self.currentY>self.targetY:
                    self.currentY=self.targetY
            else:
                self.currentY -= self.speed
                if self.currentY<self.targetY:
                    self.currentY=self.targetY
        #x,y方向都变化
        else:
            #print("3")
            # x方向，不足一步走的则直接走到终点，保证不越过终点，x_dis/y_dis表示x与y方向行走的比率，即同时达到终点其速度与距离成正比
            if math.fabs(self.currentX-self.targetX)<math.fabs((self.delt_x/self.delt_y)*self.speed):
                self.currentX=self.targetX
            else:
                #在x方向上足够一步移动的，则判断向哪个方向移动
                if self.delt_x >0:
                    self.currentX += math.fabs((self.delt_x /self.delt_y)*self.speed)
                else:
                    self.currentX -= math.fabs((self.delt_x /self.delt_y)*self.speed)
            #在y方向不够一步移动的，则直接走到终点
            if math.fabs(self.currentY-self.targetY)<self.speed:
                self.currentY=self.targetY
            else:
                if self.delt_y>0:
                    self.currentY +=self.speed
                else:
                    self.currentY -= self.speed

        # 更新当前图片位置点
        self.setRectPos()
        #print(self.rect.x, self.rect.y)

