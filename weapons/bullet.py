import pygame
import math
import time
from positionFunc import *
from mobile_carrier.solider import *

class bullet():
    def __init__(self,screen,oriX,oriY,tarX,tarY): #子弹初始位置与往哪移动
        # 主屏幕大小,显示内容的窗口
        self.main_scene = screen
        #设置子弹图片
        self.image=pygame.image.load('./source/img/menu/bullet1.png').convert()
        #子弹的当前位置
        self.currentX=oriX*32
        self.currentY=oriY*32
        #攻击目标点
        self.targetX=(tarX+1)*32
        self.targetY=tarY*32
        # 获得子弹矩形(x, y, width, height)，操作矩形进行旋转
        self.rect = self.image.get_rect()
        self.rect.x=self.currentX
        self.rect.y=self.currentY
        # 移动速度
        self.speed = 10
        self.direction=0#表示方向

        self.clock = pygame.time.Clock()
        self.fps=2

    #设置图片位置
    def setRectPos(self):
        self.rect.x = self.currentX
        self.rect.y= self.currentY
        #self.rect.center=(self.currentX,self.currentY)

    #确定攻击方向
    def getDirection(self):
        if self.currentX < self.targetX and self.currentY == self.targetY:  # 起点在终点的左上
            self.direction=1#向右
            print("向右移动")
        if self.currentX > self.targetX and self.currentY == self.targetY:  # 起点在终点的左上
            self.direction=2#向左
            print("向左移动")
        if self.currentX == self.targetX and self.currentY > self.targetY:  # 起点在终点的左上
            self.direction=3#向下
            print("向下移动")
        if self.currentX == self.targetX and self.currentY < self.targetY:  # 起点在终点的左上
            self.direction=4#向上
            print("向上移动")

    def judgeBullet(self):#判断子弹是否击中
        if self.currentX==self.targetX and self.currentY==self.targetY:
            return True
        else:
            return False
    # 显示子弹
    def displayBullet(self):
        self.main_scene.blit(self.image, (self.currentX, self.currentY))
        print("显示:", self.currentX, self.currentY, self.rect.x, self.rect.y)

    def moveBullet(self):
        self.getDirection()
        print("方向=", self.direction)
        print("起点：(", self.currentX, ",", self.currentY, ");终点：", self.targetX, ",", self.targetY, ")")
        # 移动 1:右 2 左 3 下  4上



        # if self.direction == 1:  # 右
        #     self.currentX += self.speed
        #     print("向右走")
        #     if self.currentX > self.targetX:
        #         self.currentX = self.targetX
        # elif self.direction == 2:  # 左
        #     self.currentX -= self.speed
        #     print("向左走")
        #     if self.currentX < self.targetX:
        #         self.currentX = self.targetX
        # elif self.direction == 3:  # 下
        #     self.currentY -= self.speed
        #     print("向下走")
        #     if self.currentY < self.targetY:
        #         self.currentY = self.targetY
        # elif self.direction == 4:  # 上
        #     self.currentY += self.speed
        #     print("向上走")
        #     if self.currentY > self.targetY:
        #         self.currentY = self.targetY
        # 更新当前图片位置点
        self.setRectPos()
        print(self.rect.x, self.rect.y)

    #旋转子弹
    def rotateAngle(self):
        # 计算旋转角度
        angle = math.atan2(math.fabs((self.targetY - self.currentY)), math.fabs((self.targetX - self.currentX)))  # angle弧度
        print("angle:", angle)
        theta = 0
        flag = 0
        if self.currentX < self.targetX and self.currentY < self.targetY:  # 起点在终点的左上
            theta = 360 - angle * (180 / math.pi)  # 角度
            flag=1
            print("左上")
        elif self.currentX == self.targetX and self.currentY > self.targetY:  # 起点在终点的上方
            theta = angle * (180 / math.pi)  # 角度
            flag=2
            print("正下方")
        elif self.currentX == self.targetX and self.currentY < self.targetY:  # 起点在终点的上方
            theta = 180 + angle * (180 / math.pi)  # 角度
            flag=3
            print("正上方")
        elif self.currentX < self.targetX and self.currentY == self.targetY:  # 在上方
            theta = angle * (180 / math.pi)  # 角度
            flag=4
            print("正左方")
        elif self.currentX > self.targetX and self.currentY == self.targetY:  # 在上方
            theta = 180 + angle * (180 / math.pi)  # 角度
            flag=5
            print("正右方")
        elif self.currentX > self.targetX and self.currentY < self.targetY:  # 起点在终点的右上
            theta = 180 + angle * (180 / math.pi)  # 角度
            flag=6
            print("右上")
        elif self.currentX > self.targetX and self.currentY > self.targetY:  # 起点在终点的右下
            theta = 180 - angle * (180 / math.pi)  # 角度
            flag=7
            print("右下")
        else:  # 起点在终点的左下
            theta = angle * (180 / math.pi)  # 角度
            flag=8
            print("左下")
        print("角度=", theta,"flag=",flag)
        return theta,flag





