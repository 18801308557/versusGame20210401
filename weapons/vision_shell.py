import random
from positionFunc import *
from shell import *
class vision_shell(shell):#vision_shell视野照明弹  继承shell炮弹
    def __init__(self,position,target,launchTime,disturbFlag,image):
        shell.__init__(position,target,launchTime,disturbFlag,image)
        self.name="bullet" #炮弹种类名称
        self.vision_R=200 #照明范围，半径
        self.LightTime = 12  # 持续照明时间  12s



