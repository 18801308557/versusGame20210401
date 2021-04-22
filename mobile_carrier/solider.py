
from positionFunc import *





class solider:
    def __init__(self,position,camp,soliderNum,oneHitNum,speed=0):
        #初始位置，阵营，士兵编号，是否探测，一波进攻数量，移动速度
        #self.visible=True #视野可见
        self.HP=100 #生命值
        self.speed=speed #移动速度
        self.camp=camp #所属阵营
        self.start_position=position #初始位置
        self.curr_position=position #当前位置
        self.soliderNum=soliderNum #士兵编号
        #self.disturbFlag=disturbFlag #是否开启探测
        self.oneHirNum=oneHitNum #一波进攻数量
        self.totalBulletNum=500 #总弹药量
        # 属性按照需要自行增删改...

        # 移动函数
        def movePosition(self, position):
            return True  # 该语句仅作占位，写完即删
            # 逻辑描述：逐步计算下一步位置，更新位置，概率，计算总移动距离等。

        # 计算命中概率
        def calPossibility(self):
            distance = distanceCal(self.curr_pos[0], self.curr_pos[1], self.target.curr_pos[0], self.target.cur_pos[1])
            if distance <= self.R:
                self.hitPropable = 0.5
            elif distance > self.R and distance <= self.R * 2:
                self.hitPropable = 0.4
            elif distance > self.R * 2 and distance <= self.R * 3:
                self.hitPropable = 0.05
            else:
                self.hitPropable = 0.01

        #移动攻击函数，enemyList是敌人列表
        def moveSoliderAttack(self,enemyList):
            return True
            # 逻辑描述：判断是否有探测功能，若有探测，则误差半径逐步降低，否则不变，逐步计算下一步位置，更新位置，概率，计算总移动距离等。

