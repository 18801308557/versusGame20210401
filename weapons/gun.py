import random
import pygame
from positionFunc import *
import time
class gun():
    #子弹的列表
    bulletList=[]
    def __init__(self,screen,position,direction,target):
        # 设置要显示内容的窗口
        self.screen = screen
        # 设置枪的初始位置
        self.pos=position
        #设置枪发射子弹的方向
        self.direction=direction
        #设置枪的模型图片，默认imageName
        self.image=pygame.image.load("  ").convert()

        self.HP_initial = 100  # 初始生命值
        self.HP_current=100  #当前生命值
        self.target = target  # 攻击敌人的目标
        self.oneHitNum_max=3 #枪最多一次发射几颗子弹，三连发
        self.bulletNum_current=100#当前子弹库存量
        self.hitArea = 100  # 枪的射程范围，默认为100

    #绘制枪和子弹，显示在主屏幕上
    def display(self):
        self.screen.blit(self.image,self.pos[0],self.pos[1])
        for bullet in self.bulletList:#循环取出子弹对象
            if bullet.judge(self.hitArea):#判断子弹是否超出范围，越界与否
                self.bulletList.remove(bullet) #移除越界的子弹
            if bullet.detect_conlision(bullet,self.target):#碰撞了
                self.bulletList.remove(bullet)  # 移除越界的子弹
                #target.HP-=15????敌方生命值减少，设置敌方摧毁
            bullet.moveBullet()#让一个子弹不断移动显示

    #发射子弹
    def fireBullet(self):
        if self.bulletNum_current>=self.oneHitNum_max:#还有子弹库存
            for i in self.oneHitNum_max:#一次最多发射几颗子弹
                fireTime=time.time()#记录发射子弹的时间
                newBullet=bullet(self.screen,self.pos,self.direction,fireTime)#新建子弹对象
                self.bulllist.append(newBullet)#加入子弹列表
                newBullet.visible = True  # 已经发射表示可见
                newBullet.displayBullet()#显示子弹
                self.bulletNum_current-=self.oneHitNum_max#库存量-1
        else:
            print("子弹库存量不足，请添加子弹！")

    #枪移动函数
    def moveLeft(self):
        self.pos[0]-=10

    def moveRight(self):
        self.pos[0]+=10

    def moveUp(self):
        self.pos[1]-=10

    def moveDown(self):
        self.pos[1]+=10


class bullet():
    def __init__(self,screen,position,direction,fireTime): #子弹初始位置与往哪移动
        # 主屏幕大小,显示内容的窗口
        self.main_scene = screen
        #设置子弹图片
        self.image=pygame.image.load("").convert()
        #子弹的位置
        self.pos=position
        #子弹移动的方向
        self.direction=direction
        # 子弹是否可见，不可见表示还没有发射或已经销毁
        self.visible=False
        # 获得子弹矩形(x, y, width, height)，用于进行碰撞检测
        self.rect = self.image.get_rect()
        # 移动速度
        self.speed = 5
        #子弹发射时间
        self.fireTime=fireTime
        #子弹走的距离是否超出射程
        self.distance=0#初始为0

    # 设置子弹rect的位置，可稍微与枪的位置调整
    def set_pos(self):
        self.rect[0] = self.pos[0]
        self.rect[1] = self.pos[1]

        # 子弹移动函数
    def moveBullet(self):
        if not self.visible: #如果子弹不可见，则返回空
            return
        #朝某个方向移动
        if self.direction=='right':
            self.rect[0]+=self.speed
        elif self.direction=='left':
            self.rect[0]-=self.speed
        elif self.direction=='up':
            self.rect[1]-=self.speed
        else:
            self.rect[1]+=self.speed

    #根据当前实践计算子弹走的距离，是否超出射程，如果超出射程则消失不可见
    def calDistance(self):
        self.distance=self.speed*(time.time()-self.fireTime)

    def judge(self,hitArea):
        self.calDistance()#计算已走的距离
        if self.rect[0] < 0 or self.rect[1]< 0 or self.rect[0] > self.main_scene.size[0] or self.rect[1] > self.main_scene.size[1]:#是否超出边界
            self.visible=False#越界销毁
            return True
        elif self.distance>=hitArea:
            self.visible=False#销毁
            return True #超出枪的射程限制范围
        else:
            return False

    #子弹显示
    def displayBullet(self):
        if not self.visible:#不可见直接return
            return
        self.main_scene.blit(self.image, (self.pos[0], self.pos[1]))

    # 碰撞检测
    def detect_conlision(self,bullet,target):
        # 判断子弹的矩形和飞机的矩形是否相交
        if pygame.Rect.colliderect(bullet.rect, target.rect):
            # 子弹设置为不可见
            bullet.visible = False
            return True#表示碰撞
        else:
            return False#表示没有碰撞













