import random
from positionFunc import *
from shell import *
class general_shell(shell):#一般炮弹
    def __init__(self,position,target,launchTime,disturbFlag):
        #初始位置，攻击目标，发射时间，是否开启探测
        self.visible=True #是否可见
        self.target=target #攻击目标？？
        self.speed=10 #移动速度
        self.name="general_shell" #名称
        self.hit_area=2000 #攻击范围
        self.start_pos=position #初始位置
        self.curr_pos=position #当前位置
        self.shoot=False #是否发射
        self.intercept=False #是否被拦截
        self.launchTime=launchTime #发射时间
        self.disturbFlag=disturbFlag #是否具备探测功能
        self.missRandomPropable=random.random()  #随机生成打不中的概率
        self.R=120 #概率半径
        self.hitPropable=0 #命中概率


    #计算命中概率
    def calPossibility(self):
        distance=distanceCal(self.curr_pos[0],self.curr_pos[1],self.target.curr_pos[0],self.target.cur_pos[1])
        if distance<=self.R:
            self.hitPropable=0.5
        elif distance>self.R and distance<=self.R*2:
            self.hitPropable = 0.4
        elif distance>self.R*2 and distance <= self.R*3:
            self.hitPropable=0.05
        else:
            self.hitPropable=0.01

    #计算攻击函数，攻击策略，怎么攻击成功概率大
    def hit(self):

        return True
