import random
from positionFunc import *
class shell():   #炮弹
    def __init__(self,position,target,launchTime,disturbFlag,image):
        #初始位置，攻击目标，发射时间，是否开启探测
        self.image=image #表示该炮弹的模型或图像
        self.visible=True #是否可见
        self.target=target #攻击目标
        self.HP=100 #最大生命值
        self.curr_HP=100#当前生命值
        self.injureNum=0 #导弹毁伤，损毁的数量
        self.speed=1 #移动速度
        self.name=["general_shell","inercept_shell","vision_shell"] #导弹的种类名称
        self.start_pos=position #初始位置
        self.curr_pos=position #当前位置
        self.shoot=False #是否发射,开炮
        self.intercept=False #是否被拦截
        self.launchTima=launchTime #发射时间
        self.disturbFlag=disturbFlag #是否具备探测功能
        self.missRandomPropable=random.random()  #随机生成打不中的概率
        self.R=120 #概率半径  命中半径
        self.hitPropable=0 #命中概率，杀伤概率
        #属性按照需要自行增删改...


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

    #移动函数
    def movePosition(self,position):
        if(self.disturbFlag):
            self.R=self.R*3/4  #  半径降低1/4
        self.curr_pos=position #更新位置
        self.calPossibility(self)#计算命中概率
        #逻辑描述：判断是否有探测功能，若有探测，则误差半径逐步降低，否则不变，逐步计算下一步位置，更新位置，概率，计算总移动距离等。

    #