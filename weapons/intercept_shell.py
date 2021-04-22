import random
from positionFunc import *
from shell import *
from vision_shell import *
class intercept_shell(shell):#拦截炮弹

    def __init__(self, screen, x, y, target, launchTime, imageName, direction):
        shell.__init__(screen, x, y, target, launchTime, imageName, direction)
        self.shellNum_max = 50#拦截炮弹的数目
        self.name = "intercept_shell"  # 炮弹种类名称
        self.interceptR = 2000  # 拦截范围，半径
        self.interceptProbability=random.random()#随机生成拦截概率
        self.interceptStatus=False#拦截状态
        self.interceptList=[]#拦截可选对象

    #定义拦截策略，怎么拦截才能成功
    def Intercept(self):
        #是否照明？？？若照明则拦截概率增大
        #判断拦截可选对象中哪个最容易拦截
        return True


    #计算拦截概率
    def calPossibility(self):
        distance=distanceCal(self.x,self.y,self.target.curr_pos[0],self.target.cur_pos[1])
        if distance<=self.interceptR:
            self.interceptProbability=0.5
        elif distance>self.interceptR and distance<=self.interceptR*2:
            self.interceptProbability = 0.4
        elif distance>self.interceptR*2 and distance <= self.interceptR*3:
            self.interceptProbability=0.2
        else:
            self.interceptProbability=0.1

