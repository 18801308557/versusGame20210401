import pygame
from weapons.bullet import bullet


class BaseBuild:


    def __init__(self, hero_surf, char_id,  mx, my, range,camp,screen):
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

        self.mx = mx
        self.my = my
        #终点
        self.dest_mx = 0
        self.dest_my = 0
        self.range = range
        self.camp = camp #所属阵营
        self.screen = screen
        self.totalBulletNum = 10  # 总弹药量
        self.fireBulletNum=0
        self.health = 100 #现有血量
        self.max_health = 100 # 初始血量
        self.isSelect = True
        self.live = True #物体是否存活

        self.x = mx * 32  # 角色相对于地图的坐标
        self.y = my * 32

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

        self.draw_radius(screen_surf)
        self.draw_health_bar(screen_surf)
        print(self.mx,self.my)
        screen_surf.blit(self.hero_surf,(self.mx*32,self.my*32))

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



    #增加子弹射击函数 每次计数到阈值就增加一颗子弹
    def shot(self,t_x,t_y):
        self.shot_frequency+=1
        if  self.shot_frequency == 50 and self.totalBulletNum>0:
            self.bullet_list.append(bullet(self.mx,self.my,t_x,t_y))
            self.totalBulletNum -=1
            self.shot_frequency = 0

    def logic(self):
            pass

