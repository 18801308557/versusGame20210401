import random
import time
import pygame
from positionFunc import *
class shell():   #炮弹
    def __init__(self,screen,postion,target,launchTime,direction,shellType):
        self.screen=screen
        self.pos=postion
        # 设置炮弹的模型图片
        self.image = pygame.image.load("  ").convert()
        self.target = target  # 攻击目标

        self.visible=False #是否可见
        self.speed=10  #移动速度
        self.intercept=False#是否被拦截
        self.launchTime = launchTime  # 发射时间
        self.distance=0 #炮弹所走的距离
        self.direction = direction  #炮弹发射方向
        self.rect = self.image.get_rect()#获得炮弹矩形(x, y, width, height)，用于进行碰撞检测

        #self.shellR=100#炮弹射程   炮弹车所决定的
        self.shellNum_max = 100  # 炮弹最大库存为100
        self.shellNum_current=100 #炮弹当前库存

        self.shellType=shellType #类型，0，1，2
        self.name=["general_shell","intercept_shell","vision_shell"] #导弹的种类名称

    # 设置子弹rect的位置
    def set_pos(self):
        self.rect[0] = self.pos[0]
        self.rect[1] = self.pos[1]

    # 炮弹移动，更新位置信息
    def moveShell(self):
        if not self.visible:
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


    def calDistance(self):
        self.distance = self.speed * (time.time() - self.launchTime)

    def judge(self,):
        self.calDistance()  #计算已走的距离
        if self.rect[0] < 0 or self.rect[1] < 0 or self.rect[0] > self.scene.size[0] or self.rect[1] > self.scene.size[1]:#是否超出边界
            return True
        elif self.distance>=100:#射程？？？
            return True #超出射程限制范围
        elif self.intercept:  # 如果被拦截，返回不可见
            return True
        else:
            return False

        # 碰撞检测
    def detect_conlision(self, shell, target):
        # 判断炮弹的矩形和目标矩形是否相交
        if pygame.Rect.colliderect(shell.rect, target.rect):
            # 子弹设置为不可见
            shell.visible = False
            return True  # 表示碰撞
        else:
            return False  # 表示没有碰撞

    def display(self):
        if not self.visible:  # 不可见直接return
            return
        self.screen.blit(self.image, self.pos[0], self.pos[1])



