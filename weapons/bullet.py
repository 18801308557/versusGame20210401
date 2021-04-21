import pygame
import math
import time
from positionFunc import *
from mobile_carrier.solider import *
Bullet_groups = pygame.sprite.Group()#  炮弹组，sprite.Group精灵组是一个容器，盛放程序中大量实体
class bullet(pygame.sprite.Sprite):
    def __init__(self,screen,oriX,oriY,tarX,tarY): #子弹初始位置与往哪移动
        pygame.sprite.Sprite.__init__(self)  # 基类的init函数
        # 主屏幕大小,显示内容的窗口
        self.main_scene = screen
        #设置子弹图片
        self.image=pygame.image.load('./source/img/menu/bullet.png').convert()
        #子弹的当前位置
        self.currentX=oriX
        self.currentY=oriY
        #攻击目标点
        self.targetX=tarX
        self.targetY=tarY
        # 获得子弹矩形(x, y, width, height)，操作矩形进行旋转
        self.rect = self.image.get_rect()
        # 移动速度
        self.speed = 5

    #设置图片位置
    def setRectPos(self):
        self.rect.x = self.currentX
        self.rect.y= self.currentY

    #旋转子弹图片
    def rotateBullet(self):
        #计算旋转角度
        angle = math.atan2((self.targetY - self.currentY), (self.targetX - self.currentX))  # angle弧度
        theta = angle * (180 / math.pi)  # 角度
        #旋转图片(注意：这里要搞一个新变量，存储旋转后的图片）
        newImage = pygame.transform.rotate(self.image,angle)
        # 校正旋转图片的中心点
        newImageRect = newImage.get_rect(center=self.rect.center)
        # 这里要用newRect区域，绘制图象
        self.main_scene.blit(newImage, newImageRect)
        return True

    # 子弹移动函数
    def moveBullet(self):

        self.rotateBullet()
        # 向目标位置靠近
        if self.currentX < self.targetX:
            self.currentX+=self.speed
            if self.currentX >= self.targetX:
                self.currentX = self.targetX

        elif self.currentX > self.targetX:
            self.currentX -= self.speed
            if self.currentX <= self.targetX:
                self.currentX = self.targetX

        if self.currentY < self.targetY:
            self.currentY += self.speed
            if self.currentY >= self.targetY:
                self.currentY = self.targetY
        elif self.currentY > self.targetY:
            self.currentY -= self.speed
            if self.currentY <= self.targetY:
                self.currentY = self.targetY
        self.setRectPos()

    #显示子弹
    def displayBullet(self):
        self.main_scene.blit(self.image, (self.currentX, self.currentY))



    #     #记录时间，更新子弹射击的频率
    #     self.last_time=time.time()
    #
    # def shoot(self):
    #     while solider.totalBulletNum>0:
    #         self.now = time.time()  # 获取现在时间
    #         if self.now - self.last_time > 0.5:  # 子弹时间间隔
    #             newBullet = bullet(self.main_scene,self.originalX, self.originalY)  # 创建炮弹对象
    #             Bullet_groups.add(newBullet)  # Bullet炮弹组加入
    #             Bullet_groups.update() # 设置方向标志更新炮弹的方向
    #             Bullet_groups.draw(self.main_scene)
    #             pygame.display.update()
    #             self.last_time = self.now



