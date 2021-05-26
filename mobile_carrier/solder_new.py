import pygame

from astar import AStar
from weapons.bullet import bullet
import positionFunc
class Sprite:
    """
    用于绘制精灵图的工具类
    """

    @staticmethod
    def draw(dest, source, x, y, cell_x, cell_y, cell_w=32, cell_h=32):
        """
        绘制精灵图中，指定x,y的图像
        :param dest: surface类型，要绘制到的目标surface
        :param source: surface类型，来源surface
        :param x: 绘制图像在dest中的坐标
        :param y: 绘制图像在dest中的坐标
        :param cell_x: 在精灵图中的格子坐标
        :param cell_y: 在精灵图中的格子坐标
        :param cell_w: 单个精灵的宽度
        :param cell_h: 单个精灵的高度
        :return:
        """
        dest.blit(source, (x, y), (cell_x * cell_w, cell_y * cell_h, cell_w, cell_h))

class CharWalk:
    """
    人物行走类 char是character的缩写
    """
    DIR_DOWN = 0
    DIR_LEFT = 1
    DIR_RIGHT = 2
    DIR_UP = 3

    def __init__(self, hero_surf, char_id, dir, mx, my, range,cost,camp,screen):
        """
        :param hero_surf: 精灵图的surface
        :param char_id: 角色id
        :param dir: 角色方向
        :param mx: 角色所在的小格子坐标
        :param my: 角色所在的小格子坐标
        :param range: 角色攻击范围
        :param camp: 角色所属阵营
        """

        self.hero_surf = hero_surf
        self.char_id = char_id
        self.dir = dir
        self.cost =cost
        self.mx = mx
        self.my = my
        self.range = range
        self.camp = camp #所属阵营
        self.screen = screen
        self.totalBulletNum = 10  # 总弹药量
        self.fireBulletNum=0
        self.health = 100 #现有血量
        self.max_health = 100 # 初始血量
        self.isSelect = False
        self.live = True #物体是否存活

        self.is_walking = False  # 角色是否正在移动
        self.frame = 1  # 角色当前帧
        self.x = mx * 32  # 角色相对于地图的坐标
        self.y = my * 32
        # 角色下一步需要去的格子
        self.next_mx = 0
        self.next_my = 0
        #终点
        self.dest_mx = 0
        self.dest_my = 0
        # 步长
        self.step = 2  # 每帧移动的像素
        # 寻路路径
        self.path = []
        # 当前路径下标
        self.path_index = 0
        self.set_dest = False
        #self.has_showed = False

        self.flag = False  # 标志发不发射子弹
        self.choose = False # 标志是否被选中
        self.bullet_list =[]
        self.shot_frequency = 0  # 射击频率

    def draw_bullet(self,dest_mx,dest_my):
        pass

    def draw_radius(self,win):
        # 点击需要查看范围的物体
        if self.isSelect:
            # draw range circle
            radius = self.range
            surface = pygame.Surface((self.range * 4, self.range * 4), pygame.SRCALPHA,32)
            pygame.draw.circle(surface, (128, 128, 128, 100), (radius, radius), radius, 0)

            win.blit(surface, (self.x+16 - radius, self.y+16 - radius))

    def draw_health_bar(self, win):
        """
        draw health bar above solder
        :param win: surface
        :return: None
        """
        #self.x,self.y为格子的左上位置

        centre_site = (self.x+16,self.y+16)#由于人物是在格子中，取中心位置
        length = 32 #血条长度
        move_by = length / self.max_health
        health_bar = move_by * self.health#剩余血量

        pygame.draw.rect(win, (255,0,0), (centre_site[0]-length/2, centre_site[1]-22, length, 5), 0)#需要根据实际微调
        pygame.draw.rect(win, (0, 255, 0), (centre_site[0]-length/2, centre_site[1] - 22, health_bar, 5), 0)

    def draw(self, screen_surf, map_x, map_y):
        cell_x = self.char_id % 12 + int(self.frame)
        cell_y = self.char_id // 12 + self.dir
        if self.choose:
            pygame.draw.rect(screen_surf,(255,0,0),(self.x,self.y,32,32),2)
        self.draw_radius(screen_surf)
        self.draw_health_bar(screen_surf)
        Sprite.draw(screen_surf, self.hero_surf, map_x + self.x, map_y + self.y, cell_x, cell_y)

    def show(self,x,y):
        self.mx = x
        self.my = y
        self.x = self.mx * 32  # 角色相对于地图的坐标
        self.y = self.my * 32

    def get_clicked(self,X,Y):
        if X <= self.x + 32 and X >= self.x:
            if Y <= self.y + 32 and Y >= self.y:
                return True
        return False

    def goto(self, x, y):
        """
        :param x: 目标点
        :param y: 目标点
        """
        self.next_mx = x
        self.next_my = y

        # 设置人物面向
        if self.next_mx > self.mx:
            self.dir = CharWalk.DIR_RIGHT
        elif self.next_mx < self.mx:
            self.dir = CharWalk.DIR_LEFT

        if self.next_my > self.my:
            self.dir = CharWalk.DIR_DOWN
        elif self.next_my < self.my:
            self.dir = CharWalk.DIR_UP

        self.is_walking = True

    #增加子弹射击函数 每次计数到阈值就增加一颗子弹
    def shot(self,t_x,t_y):
        self.shot_frequency+=1
        if  self.shot_frequency == 50 and self.totalBulletNum>0:
            self.bullet_list.append(bullet(self.mx,self.my,t_x,t_y))
            self.totalBulletNum -=1
            self.shot_frequency = 0

    def move(self):
        if not self.is_walking:
            return
        dest_x = self.next_mx * 32
        dest_y = self.next_my * 32
        # 向目标位置靠近
        if self.x < dest_x:
            self.x += self.step
            if self.x >= dest_x:
                self.x = dest_x
        elif self.x > dest_x:
            self.x -= self.step
            if self.x <= dest_x:
                self.x = dest_x

        if self.y < dest_y:
            self.y += self.step
            if self.y >= dest_y:
                self.y = dest_y
        elif self.y > dest_y:
            self.y -= self.step
            if self.y <= dest_y:
                self.y = dest_y

        # 改变当前帧
        self.frame = (self.frame + 0.1) % 3
        # 角色当前位置
        self.mx = int(self.x / 32)
        self.my = int(self.y / 32)

        # 到达了目标点
        if self.x == dest_x and self.y == dest_y:
            self.is_walking = False


    def logic(self):

        self.move()
        # 如果角色正在移动，就不管它了
        if self.is_walking:
            return

        # 如果寻路走到终点了
        if self.path_index == len(self.path) :
            #print("ifff")
            self.path = []
            self.frame = 1
            self.path_index = 0
        elif self.path_index!= 0 and  self.path_index+1 == len(self.path):
            self.path = []
            self.frame = 1
            self.path_index = 0

        else:  # 如果没走到终点，就往下一个格子走
            self.goto(self.path[self.path_index].x, self.path[self.path_index].y)


            #zmy 判断当前格子是否在攻击范围内
            dis = positionFunc.distanceCal(self.x,self.y,self.path[-1].x*32,self.path[-1].y*32)
            t_x =self.path[-1].x
            t_y = self.path[-1].y
            if dis <= self.range:
                while len(self.path) > self.path_index+1:
                    self.path.pop()
                self.flag=True
                self.is_walking = False
                if self.path and self.bullet_list is not []:
                    #修改了一下此处触发事件
                    self.shot(t_x,t_y)
                    #self.bullet_list=(self.mx,self.my,t_x,t_y)
            self.path_index += 1

    def find_path(self, map2d, end_point,screen):
        """
        :param map2d: 地图
        :param end_point: 寻路终点
        """


        #print("end_point",end_point)
        start_point = (self.mx, self.my)

        #print("start_point",start_point)
        path = AStar(map2d, start_point, end_point).start()

        if path is None:
            return

        self.path = path
        self.path_index = 0
