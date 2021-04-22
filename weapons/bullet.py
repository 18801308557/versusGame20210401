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
        self.rect.x=self.currentX
        self.rect.y=self.currentY
        # 移动速度
        self.speed = 3

    #设置图片位置
    def setRectPos(self):
        self.rect.x = self.currentX
        self.rect.y= self.currentY

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

    # #旋转子弹图片
    # def rotateBullet(self):
    #     #计算旋转角度
    #     theta=self.rotateAngle()# 角度
    #     #旋转图片(注意：这里要搞一个新变量，存储旋转后的图片）
    #     old_center=self.rect.center
    #     newImage = pygame.transform.rotate(self.image,theta)
    #     # 校正旋转图片的中心点
    #     newImageRect = newImage.get_rect()
    #     self.newImageRect.center = old_center
    #     # 这里要用newRect区域，绘制图象
    #     self.main_scene.blit(newImage, newImageRect)
    #     pygame.display.update()

    # 旋转子弹函数
    def moveBullet(self):
        #显示子弹
        #self.displayBullet()
        lastTime = time.time()
        print("lastTime=", lastTime)
        angle, flag = self.rotateAngle()  # 得到旋转角度
        print("角度angle=", angle, ";flag=", flag)
        # 旋转图片(注意：这里要搞一个新变量，存储旋转后的图片）
        oldCenter = self.rect.center
        newLeaf = pygame.transform.rotate(self.image, angle)
        # 校正旋转图片的中心点
        newImageRect = newLeaf.get_rect()
        newImageRect.center = oldCenter
        self.screen.blit(newLeaf, newImageRect)
        pygame.display.update()
        # 移动
        while True:
            # nowTime = time.time()
            # if nowTime - lastTime > 0.05:
            if flag == 1:  # up
                newImageRect.y += self.speed  # 移动炮弹
                newImageRect.x += self.speed
                if newImageRect.y > self.targetY:
                    newImageRect.y = self.targetY
                if newImageRect.x > self.targetX:
                    newImageRect.x = self.targetX
            elif flag == 2:  # 正下方
                newImageRect.y -= self.speed
                if newImageRect.y < self.targetY:
                    newImageRect.y = self.targetY
            elif flag == 3:  # 正上方
                newImageRect.y += self.speed
                if newImageRect.y>self.targetY:
                    newImageRect.y=self.targetY
            elif flag == 4:  # right
                newImageRect.x += self.speed
                if newImageRect.x>self.targetX:
                    newImageRect.x=self.targetX
            elif flag == 5:  # right
                newImageRect.x -= self.speed
                if newImageRect.x<self.targetX:
                    newImageRect.x=self.targetX
            elif flag == 6:  # 正上方
                newImageRect.y += self.speed
                newImageRect.x -= self.speed
                if newImageRect.y>self.targetY:
                    newImageRect.y=self.targetY
                if newImageRect.x<self.targetX:
                    newImageRect.x=self.targetX
            elif flag == 7:  # right
                newImageRect.x -= self.speed
                newImageRect.y -= self.speed
                if newImageRect.y<self.targetY:
                    newImageRect.y=self.targetY
                if newImageRect.x<self.targetX:
                    newImageRect.x=self.targetX
            elif flag == 8:  # right
                newImageRect.x += self.speed
                newImageRect.y -= self.speed
                if newImageRect.y<self.targetY:
                    newImageRect.y=self.targetY
                if newImageRect.x>self.targetX:
                    newImageRect.x=self.targetX
            # lastTime = nowTime
            self.screen.blit(newLeaf, newImageRect)
            pygame.display.update()
            print("x:", newImageRect.x - self.targetX, "y:", newImageRect.y - self.targetY)
            if math.fabs(newImageRect.x - self.targetX) <= 2 and math.fabs(newImageRect.y - self.targetY) <= 2:
                print("x:", newImageRect.x - self.targetX, "y:", newImageRect.y - self.targetY)
                break  # 击中推出移动循环

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



