import sys
import os
import pygame
import random
from Map import  GameMap
from mobile_carrier.solder_new import  CharWalk, Sprite
from menu.menu import horizontalMenu
from  mobile_carrier.BaseBuild import BaseBuild
import positionFunc
import pygame_menu

side_img = pygame.transform.scale(pygame.image.load("./source/img/menu/bg1.png"), (640, 70))
vertical_img = pygame.transform.scale(pygame.image.load("./source/img/menu/vbg.png"), (70,640))
Blue_solder = pygame.transform.scale(pygame.image.load("./source/img/menu/Blue_solder.png"), (64, 64))
Blue_weapon2 = pygame.transform.scale(pygame.image.load("./source/img/menu/Blue_weapon2.png"), (64, 64))
Blue_weapon3 = pygame.transform.scale(pygame.image.load("./source/img/menu/Blue_weapon3.png"), (64, 64))
Red_solder = pygame.transform.scale(pygame.image.load("./source/img/menu/Red_solder.png"), (64, 64))
Red_weapon2 = pygame.transform.scale(pygame.image.load("./source/img/menu/Red_weapon2.png"), (64, 64))
Red_weapon1 = pygame.transform.scale(pygame.image.load("./source/img/menu/weapon1.png"), (64, 64))
Start_button = pygame.transform.scale(pygame.image.load("./source/img/menu/start.png"), (64, 64))
pause_button = pygame.transform.scale(pygame.image.load("./source/img/menu/pause.png"), (64, 64))
other_button = pygame.transform.scale(pygame.image.load("./source/img/menu/othersetting.png"), (64, 64))

building = pygame.transform.scale(pygame.image.load("./source/Buildings/Academy/mageguild2.png"), (32, 32))

class Game:
    def __init__(self, title, width, height, fps=60):
        """
        :param title: 游戏窗口的标题
        :param width: 游戏窗口的宽度
        :param height: 游戏窗口的高度
        :param fps: 游戏每秒刷新次数
        :param status: 游戏状态
        """
        self.show_attack =True;
        self.score = 0#得分
        self.source = 10000#可用资源数
        self.title = title
        self.width = width
        self.height = height
        self.screen_surf = None
        self.fps = fps
        self.status = 'stop'#游戏状态默认为暂停
        self.__init_pygame()
        self.__init_game()


        self.main_menu = None
        #wzq水平菜单的初始化
        self.horizonMenu = horizontalMenu(0, self.height - side_img.get_height(), side_img,'horizon')
        #水平菜单添加按键
        self.horizonMenu.add_btn(Blue_solder, "Blue_solder", 200)
        self.horizonMenu.add_btn(Blue_weapon2, "Blue_weapon2", 200)
        self.horizonMenu.add_btn(Blue_weapon3, "Blue_weapon3", 200)
        self.horizonMenu.add_btn(Red_solder, "Red_solder", 80)
        self.horizonMenu.add_btn(Red_weapon1, "Red_weapon1", 120)
        self.horizonMenu.add_btn(Red_weapon2, "Red_weapon2", 200)

        #增加游戏的垂直主菜单，开始暂停
        self.verticalMenu = horizontalMenu(self.width-vertical_img.get_width(),0,vertical_img,'vertical')
        #垂直菜单增加按键
        self.verticalMenu.add_btn(Start_button,"start",0)#开始按钮
        self.verticalMenu.add_btn(pause_button,"pause",0)#暂停按钮
        self.verticalMenu.add_btn(other_button,"other",0)#其他按钮
        #初始化角色列表
        #self.role_list = []

        self.red_list = []#初始化红方角色列表
        self.blue_list = []#初始化蓝方角色列表
        self.weapon_list = []#初始化武器列表
        #self.candidate_list = []#初始化当前正在寻路的物体列表

        #我们的攻击操作是先点击攻击者，再点击攻击目标，此处为是否有未设置目标的攻击者
        self.moving_candidate = None

        self.moving_object = None #此处存放ui拖拽的物体
        self.update()


    def __init_pygame(self):
        """
        pygame相关的初始化操作
        """
        pygame.init()#pygmae包导入
        pygame.display.set_caption(self.title)#设置标题
        self.screen_surf = pygame.display.set_mode([self.width, self.height])#设置显示窗口大小
        self.clock = pygame.time.Clock()#设置时钟

    def __init_game(self):
        """
        我们游戏的一些初始化操作
        """
        #导入角色图片，包括8种角色的各个方向显示
        self.hero = pygame.image.load('./source/img/character/hero.png').convert_alpha()
        #地图背景图片的放置
        self.map_bottom = pygame.image.load('./source/img/map/1.png').convert_alpha()

        self.game_map = GameMap(self.map_bottom, 0, 0) # 根据当前地图相关参数进行地图初始化
        self.game_map.load_walk_file('./source/img/map/1.map')#根据地图的显示，我们规定了一些不可到达的区域，导入该文件。

#
    # 直接将红蓝双方进行一一配对，在之后的策略中需要改进该函数
    def init_stratege(self):
        #将红方蓝方目标体一一对应（也就是之后需要做的策略）
        for red_army,blue_army in zip(self.red_list,self.blue_list):
            #看是否设置过了目标
            #if not red_army.set_dest:
                #print(red_army,blue_army)
            red_army.dest_mx = blue_army.mx
            red_army.dest_my = blue_army.my
                #red_army.set_dest  =True

    # 将阵营中物体显示出来 并更新是否存活
    def load_camp(self,camp):
        for army in camp:# 遍历所有阵营
            if army.live:#如果存活就将其绘制在屏幕上
                army.draw(self.screen_surf, self.game_map.x, self.game_map.y)
            else:#如果不存活，就将其删除
                camp.remove(army)
                if(army.camp == "blue"):#如果删除的是蓝方阵营的物体，得分就增加200
                   self.score += 200  # 目标销毁，得分自动加200

    # 红方子弹绘制  将子弹显示出来，并更新子弹是否需要继续发射
    def load_bullet_red(self):
        for role in self.red_list:#遍历红方阵营
            for b in role.bullet_list:#对于每一个士兵其存有一个子弹list
                target = self.choose_role(self.blue_list,b.targetX,b.targetY)#需要攻击的位置是否存在物体
                if b.live and target:#如果当前子弹没有到目标位置（也就是存活） 且目标地址存在物体（因为蓝方是静止的，如果不存在物体说明已经消灭）
                    b.displayBullet(self.screen_surf)#绘制子弹
                    b.moveBullet()#子弹移动的逻辑
                    b.hit_target(target)#检测子弹是否和物体碰撞
                else:
                    role.bullet_list.remove(b)#子弹发生碰撞后 或目标物体毁灭 子弹就该消失了


    #蓝方子弹绘制  将子弹显示出来，并更新子弹是否需要继续发射
    def load_bullet_blue(self):
        for role in self.blue_list:#遍历蓝方阵营
            for b in role.bullet_list:#对于每一个士兵其存有一个子弹list
                target = self.choose_role(self.red_list,b.targetX,b.targetY)#需要攻击的位置是否存在物体
                if b.live:#与红方判断条件区别开来（目前的设定是不跟踪的，因为红方是移动方，所以子弹不一定会打中红方）
                    b.displayBullet(self.screen_surf)#绘制子弹
                    b.moveBullet()#子弹移动的逻辑
                    if target:#如果有目标在，就需要考虑是否碰撞了（此处存在一点问题，物体在移动过程中发生碰撞，是否也需要考虑？）
                        b.hit_target(target)
                else:
                    role.bullet_list.remove(b)#子弹发生碰撞后 或目标物体毁灭 子弹就该消失了

    # 考虑在何种情况下需要创造蓝方的子弹
    def set_bullet_blue(self):
        for src in self.blue_list:#遍历蓝方阵营
            for dst in self.red_list:#遍历红方阵营
                if positionFunc.distanceInR(src.x,src.y,src.range,dst.x,dst.y): # 检测是否有物体存在于可攻击范围内
                    #print(dst.x,dst.y)
                    src.shot(dst.mx,dst.my)#如果范围内存在物体，就攻击他（此处也需要考虑一些问题，比如是否先毁灭范围内一个物体，还是每个都打）

    #初始化蓝方阵营，随机在地图的格子中放3个蓝方
    def random_set_blue(self):
        index=[]
        while len(index)<= 2 :
            x = random.randint(2,self.game_map.w/2-2) #规定蓝方的位置在地图左半部分
            y = random.randint(2,self.game_map.h-2) #为了保证让生成的3个位置距离至少是2个格子，在if判断中使用了[x+2,y+2],-2就是为了保证+2时不超过边界
            if self.game_map[x][y] == 0 & ([x,y] not in index)&([x+2,y+2] not in index): #不能放置在有障碍的格子中，格子也不能重复
                index.append([x,y])
        #role = pygame.image.load('./source/img/character/hero.png').convert_alpha()
        role = pygame.transform.scale(pygame.image.load("./source/Buildings/Academy/mageguild2.png"), (64, 64))
        role_index_list = [6, 9, 48, 51, 54, 57]
        for arr in index :
            obj = BaseBuild(building, role_index_list[0], arr[0], arr[1], 150, 'blue', self.screen_surf)
            #obj = CharWalk(role, role_index_list[0], CharWalk.DIR_DOWN, arr[0], arr[1], 100, 'blue',self.screen_surf)
            self.blue_list.append(obj)

    def update(self):
        """
        更新相关事件
        :return:
        """
        self.random_set_blue()
        while True:
            self.clock.tick(self.fps)#更新时钟

            self.event_handler()#处理游戏点击等事件
            self.game_map.draw_bottom(self.screen_surf)# 画面更新
            if self.status == 'stop':#游戏暂停的时候可以进行布局
                #是否有正在拖拽的物体
                if self.moving_object:
                    m_x, m_y = pygame.mouse.get_pos()#获取鼠标点击位置
                    mx = (m_x - self.game_map.x) // 32 #获取位置对应的二维数组下标
                    my = (m_y - self.game_map.y) // 32
                    self.moving_object.show(mx, my)#重新设置物体的格子位置
                    self.moving_object.draw(self.screen_surf, self.game_map.x, self.game_map.y)


            elif self.status == 'start':#游戏开始的时候就进行物体的逻辑判断，移动等操作
                #self.bulletUpdate()#子弹的相关事件触发

                #之后策略的设置
                self.init_stratege()
                # 移动的过程中检测蓝方有没有物体
                for set_role in self.red_list:
                    for dst in self.blue_list:  # 遍历红方阵营
                        if positionFunc.distanceInR(set_role.x, set_role.y, set_role.range, dst.x, dst.y):  # 检测是否有物体存在于可攻击范围内
                            set_role.dest_mx = dst.mx
                            set_role.dest_my = dst.my
                    #print("路径",set_role.next_mx, set_role.next_my)
                    set_role.find_path(self.game_map, (set_role.dest_mx, set_role.dest_my),self.screen_surf)

                for mobile in self.red_list+self.blue_list:
                    mobile.logic()
                self.set_bullet_blue()
                self.load_bullet_red()
                self.load_bullet_blue()


            # 画面更新
            #如果没有正在拖拽的物体，就不断刷新当前场上的物体
            self.load_camp(self.red_list)
            self.load_camp(self.blue_list)
            """
            if self.main_menu and self.main_menu.is_enabled():
                self.main_menu.draw(self.screen_surf)
            """
            self.horizonMenu.draw(self.screen_surf)#绘制UI
            self.verticalMenu.draw(self.screen_surf)#绘制UI
            if self.status=='pause':
                if self.main_menu and self.main_menu.is_enabled():
                    self.main_menu.draw(self.screen_surf)
            pygame.display.update()

    #处理触发的事件
    def event_handler(self):
        """
        这个函数只检测是否有点击UI，拖拽物体等操作。
        :return:
        """
        if self.main_menu and self.main_menu.is_enabled():
            self.main_menu.update(pygame.event.get())
        for event in pygame.event.get():

            if event.type == pygame.QUIT:#如果触发了退出事件，则退出。
                sys.exit()

            #如果鼠标点击了
            elif event.type == pygame.MOUSEBUTTONDOWN and self.status != 'pause':
                mouse_x, mouse_y = pygame.mouse.get_pos()#获取鼠标点击的位置x,y

                #获取当前鼠标所在格子
                mx = (mouse_x - self.game_map.x) // 32
                my = (mouse_y - self.game_map.y) // 32
                #print("点击",mx,my )
                #如果当前拖拽的物体放置下来了
                if self.moving_object:
                    # 已放置好，将其添加到角色列表
                    if self.moving_object.camp == "blue":  # 如果是蓝方，就添加到蓝方列表
                        self.blue_list.append(self.moving_object)
                    elif self.moving_object.camp =="red" :  # 如果是红方，就添加到红方列表
                        self.red_list.append(self.moving_object)
                    # 将拖拽ui物体重新置为空，不影响下次拖拽
                    self.moving_object = None

                # 如果当前没有在拖拽物体，这是一个基本状态
                else:
                    # 判断当前是否在点击水平按钮
                    side_menu_button = self.horizonMenu.get_clicked(mouse_x, mouse_y)
                    # 判断当前是否在点击垂直按钮
                    verti_menu_button = self.verticalMenu.get_clicked(mouse_x,mouse_y)

                    # 菜单的点击
                    if side_menu_button:
                        #print("side_menu_button",side_menu_button)
                        # 点击的是水平菜单中的按钮就触发相应事件
                        self.add_weapon(side_menu_button)

                    # 如果是垂直菜单按钮
                    if verti_menu_button:
                        # 点击的是垂直主菜单中的按钮就触发相应事件
                        self.clicked_main_menu(verti_menu_button)



    def add_weapon(self, name):
        x, y = pygame.mouse.get_pos()
        name_list = ["Blue_solder", "Blue_weapon3", "Blue_weapon2", "Red_weapon2", "Red_weapon1", "Red_solder"]
        role_index_list = [6, 9, 48, 51, 54, 57]
        mx = (x - self.game_map.x) // 32
        my = (y - self.game_map.y) // 32

        try:
            role = pygame.image.load('./source/img/character/hero.png').convert_alpha()
            #zmy 添加range,range = 100
            if (name =='Blue_solder') | (name=="Blue_weapon3") | (name=="Blue_weapon2") :
                #obj = CharWalk(role, role_index_list[name_list.index(name)], CharWalk.DIR_DOWN, mx, my, 150, 'blue',self.screen_surf)
                obj = BaseBuild(building, 1, mx, my, 150, 'blue', self.screen_surf)
            elif (name == 'Red_solder'):   #士兵的攻击范围是50,需要消耗的资源数是80
                if(self.source <80):  #资源数不够80
                    pass
                else:
                     obj = CharWalk(role, role_index_list[name_list.index(name)], CharWalk.DIR_DOWN, mx, my, 50, 'red',self.screen_surf)
                     self.source -= 80
            elif (name == 'Red_weapon1'):  #weapon1的攻击范围是70，需要消耗的资源数是120
                if (self.source < 120):  # 资源数不够120
                    pass
                else:
                    self.source -= 120
                    obj = CharWalk(role, role_index_list[name_list.index(name)], CharWalk.DIR_DOWN, mx, my, 70, 'red',self.screen_surf)
            elif (name == 'Red_weapon2'):  # weapon2的攻击范围是100，，需要消耗的资源数是200
                if (self.source < 200):  # 资源数不够200
                    pass
                else:
                    self.source -= 200
                    obj = CharWalk(role, role_index_list[name_list.index(name)], CharWalk.DIR_DOWN, mx, my, 100, 'red',self.screen_surf)
            self.moving_object = obj
        except Exception as e:
            print(str(e) + "NOT VALID NAME")

    def clicked_main_menu(self, name):
        """
        主菜单点击触发事件
        :param name: 按键名称
        :return:
        """

        if name == "start" :
            self.status = name
        elif name == "pause":

            self.create_mainmenu()
            self.status = name

        print(name)

    def choose_role(self,role_list, x, y):
        for candidate_role in role_list:
            if candidate_role.get_clicked(x, y):
                return candidate_role
        return None

    def continueGame(self):

        if self.main_menu:
            self.status = 'start'
            #print("okokokkoko")
            self.main_menu.disable()


    def create_mainmenu(self):
        #print("hello")
        self.main_menu = pygame_menu.Menu(300,400,'Main Menu',theme=pygame_menu.themes.THEME_BLUE)
        score = 'score:  '+ str(self.score)
        source = 'source: ' +str(self.source)
        self.main_menu.add.toggle_switch('Attack Range',onchange=self.show_attackRange())
        self.main_menu.add.label(score,max_char=-1,font_size=20)
        self.main_menu.add.label(source,max_char=-1,font_size=20)
        self.main_menu.add.button('Continue',self.continueGame)
        self.main_menu.add.button('Quit', pygame_menu.events.EXIT)
    #wzq 更改显示状态
    def show_attackRange(self):
        #print("hello")
        self.show_attack = not self.show_attack
        for role in self.red_list+self.blue_list:
            #print(role.isSelect)
            role.isSelect = self.show_attack


"""
if __name__ == '__main__':
    Game("versus", 710, 550)
"""