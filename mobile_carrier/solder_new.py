import pygame

from astar import AStar


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


class Array2D:
    """
        说明：
            1.构造方法需要两个参数，即二维数组的宽和高
            2.成员变量w和h是二维数组的宽和高
            3.使用：‘对象[x][y]’可以直接取到相应的值
            4.数组的默认值都是0
    """

    def __init__(self, w, h, default=0):
        self.w = w
        self.h = h
        self.data = []
        self.data = [[default for y in range(h)] for x in range(w)]

    def show_array2d(self):
        for y in range(self.h):
            for x in range(self.w):
                print(self.data[x][y], end=' ')
            print("")

    def __getitem__(self, item):
        return self.data[item]


class GameMap(Array2D):
    """
    游戏地图类
    """

    def __init__(self, bottom, top, x, y):
        # 将地图划分成w*h个小格子，每个格子32*32像素
        w = int(bottom.get_width() / 32)
        h = int(bottom.get_height() / 32)
        super().__init__(w, h)
        self.bottom = bottom
        self.top = top
        self.x = x
        self.y = y

    def draw_bottom(self, screen_surf):
        screen_surf.blit(self.bottom, (self.x, self.y))

    def draw_top(self, screen_surf):
        screen_surf.blit(self.top, (self.x, self.y))

    def draw_grid(self, screen_surf):
        """
        画网格
        """
        for x in range(self.w):
            for y in range(self.h):
                if self[x][y] == 0:  # 不是障碍，画空心的矩形
                    pygame.draw.rect(screen_surf, (255, 255, 255), (self.x + x * 32, self.y + y * 32, 32, 32), 1)
                else:  # 是障碍，画黑色实心的矩形
                    pygame.draw.rect(screen_surf, (0, 0, 0), (self.x + x * 32 + 1, self.y + y * 32 + 1, 30, 30), 0)

    def load_walk_file(self, path):
        """
        读取可行走区域文件
        """
        with open(path, 'r') as file:
            for x in range(self.w):
                for y in range(self.h+1):

                    v = int(file.readline())
                    if y!=self.h:
                        self[x][y] = v
        # self.show_array2d()


class CharWalk:
    """
    人物行走类 char是character的缩写
    """
    DIR_DOWN = 0
    DIR_LEFT = 1
    DIR_RIGHT = 2
    DIR_UP = 3

    def __init__(self, hero_surf, char_id, dir, mx, my, range,camp):
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
        self.mx = mx
        self.my = my
        self.range = range
        self.camp = camp #所属阵营
        self.totalBulletNum = 100  # 总弹药量

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
        self.has_showed = False

    def draw(self, screen_surf, map_x, map_y):
        cell_x = self.char_id % 12 + int(self.frame)
        cell_y = self.char_id // 12 + self.dir
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
        if self.path_index == len(self.path):
            self.path = []
            self.frame = 1
            self.path_index = 0
        else:  # 如果没走到终点，就往下一个格子走
            self.goto(self.path[self.path_index].x, self.path[self.path_index].y)
            self.path_index += 1

    def find_path(self, map2d, end_point):
        """
        :param map2d: 地图
        :param end_point: 寻路终点
        """
        mrange = int(self.range/32) #半径由像素点转换为格子


        print("end_point",end_point)
        print("攻击范围",mrange)
        if end_point[1]+mrange<map2d.h:
            target = (end_point[0],end_point[1]+mrange)
        elif end_point[1] - mrange > 0 :
            target = (end_point[0], end_point[1] - mrange)
        elif end_point[0]-mrange > 0 :
            terget = (end_point[0]-mrange,end_point[1])
        elif end_point[0]+ mrange < map2d.w :
            target = (end_point[0]+mrange,end_point[1])

        start_point = (self.mx, self.my)

        print("start_point",start_point)
        path = AStar(map2d, start_point, target).start()


        if path is None:

            return

        self.path = path

        self.path_index = 0
