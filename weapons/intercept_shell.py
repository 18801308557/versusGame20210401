import random
from positionFunc import *
from shell import *
class general_shell(shell):#拦截炮弹
    def __init__(self,position,target,launchTime,disturbFlag,image,):
        shell.__init__(position,target,launchTime,disturbFlag,image)
        self.name="bullet" #名称
        self.hit_area=2000 #攻击目标


    #计算命中概率  杀伤概率
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

    #移动函数
    def movePosition(self,position):
        return True #该语句仅作占位，写完即删
        #逻辑描述：判断是否有探测功能，若有探测，则误差半径逐步降低，否则不变，逐步计算下一步位置，更新位置，概率，计算总移动距离等。
