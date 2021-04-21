import random
from positionFunc import *
from shell import *
import time
class vision_shell(shell):#vision_shell视野照明弹  继承shell炮弹
    vision_shell=[]#照明弹列表
    def __init__(self,screen,x,y,target,launchTime,imageName,direction,shellType):
        shell.__init__(screen,x,y,target,launchTime,imageName,direction,shellType)
        self.shellNum=20
        self.shellName="vision_shell"#炮弹种类名称
        self.visionR=200 #照明范围，半径
        self.visionTime = 10  # 可以照明时间  10s
        self.isVision=False


    #照明函数，startVisionTime开始照明时间，从发射到指定位置后计时，照明特定时间后消失
    def Lighting(self,startVisionTime,pos):
        if self.visionTime<time.time()-startVisionTime:
            self.visible=False#达到照明时间，结束，不可见
        else:
            self.isVision=True
            #????下面是照明对作战情况的改变









