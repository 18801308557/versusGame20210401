import sys
import os
import pygame

from mobile_carrier.solder_new import GameMap, CharWalk, Sprite
from menu.menu import horizontalMenu

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


class Game:
    def __init__(self, title, width, height, fps=60):
        """
        :param title: 游戏窗口的标题
        :param width: 游戏窗口的宽度
        :param height: 游戏窗口的高度
        :param fps: 游戏每秒刷新次数
        """
        self.title = title
        self.width = width
        self.height = height
        self.screen_surf = None
        self.fps = fps

        self.__init_pygame()
        self.__init_game()

        #wzq水平菜单的初始化
        self.horizonMenu = horizontalMenu(0, self.height - side_img.get_height(), side_img,'horizon')
        #水平菜单添加按键
        self.horizonMenu.add_btn(Blue_solder, "Blue_solder", 200)
        self.horizonMenu.add_btn(Blue_weapon2, "Blue_weapon2", 200)
        self.horizonMenu.add_btn(Blue_weapon3, "Blue_weapon3", 200)
        self.horizonMenu.add_btn(Red_solder, "Red_solder", 200)
        self.horizonMenu.add_btn(Red_weapon1, "Red_weapon1", 200)
        self.horizonMenu.add_btn(Red_weapon2, "Red_weapon2", 200)

        #增加游戏的垂直主菜单，开始暂停
        self.verticalMenu = horizontalMenu(self.width-vertical_img.get_width(),0,vertical_img,'vertical')
        #垂直菜单增加按键
        self.verticalMenu.add_btn(Start_button,"start",0)
        self.verticalMenu.add_btn(pause_button,"pause",0)
        self.verticalMenu.add_btn(other_button,"other",0)
        #初始化角色列表
        self.role_list = []
        #初始化武器列表
        self.weapon_list = []
        #初始化当前正在寻路的物体列表
        self.candidate_list = []
        #我们的攻击操作是先点击攻击者，再点击攻击目标，此处为是否有未设置目标的攻击者
        self.moving_candidate = None

        self.moving_object = None #此处存放ui拖拽的物体

        self.update()

    def __init_pygame(self):
        """
        pygame相关的初始化操作
        """
        pygame.init()
        pygame.display.set_caption(self.title)
        self.screen_surf = pygame.display.set_mode([self.width, self.height])
        self.clock = pygame.time.Clock()

    def __init_game(self):
        """
        我们游戏的一些初始化操作
        """
        self.hero = pygame.image.load('./source/img/character/hero.png').convert_alpha()
        self.map_bottom = pygame.image.load('./source/img/map/1.png').convert_alpha()
        self.map_top = pygame.image.load('./source/img/map/0_top.png').convert_alpha()
        self.game_map = GameMap(self.map_bottom, self.map_top, 0, 0)
        self.game_map.load_walk_file('./source/img/map/1.map')

        # zmy 添加range参数,range = 70
        self.role = CharWalk(self.hero, 48, CharWalk.DIR_DOWN, 5, 10,70, 'None',self.screen_surf)

    def update(self):
        while True:
            self.clock.tick(self.fps)


            # 逻辑更新
            for mobile in self.role_list:
                mobile.logic()
            self.event_handler()
            # 画面更新
            self.game_map.draw_bottom(self.screen_surf)

            #是否有正在拖拽的物体
            if self.moving_object:

                m_x, m_y = pygame.mouse.get_pos()#获取鼠标点击位置
                mx = (m_x - self.game_map.x) // 32 #获取位置对应的二维数组下标
                my = (m_y - self.game_map.y) // 32
                self.moving_object.show(mx, my)#重新设置物体的格子位置
                self.moving_object.draw(self.screen_surf, self.game_map.x, self.game_map.y)
            # else:
            #如果没有正在拖拽的物体，就不断刷新当前场上的物体
            for mobile in self.role_list:
                mobile.draw(self.screen_surf, self.game_map.x, self.game_map.y)
                # mobile.has_showed = True

            # self.game_map.draw_top(self.screen_surf)
            #self.game_map.draw_grid(self.screen_surf)

            self.horizonMenu.draw(self.screen_surf)#绘制UI
            self.verticalMenu.draw(self.screen_surf)#绘制UI
            pygame.display.update()

    #处理触发的事件
    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            #如果鼠标点击了
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                #获取当前鼠标所在格子
                mx = (mouse_x - self.game_map.x) // 32
                my = (mouse_y - self.game_map.y) // 32

                #如果当前拖拽的物体放置下来了
                if self.moving_object:
                    print("check1")
                    if self.moving_object.camp == 'blue':
                        pygame.draw.circle(self.screen_surf,(255,0,0),(mx,my),200,width=10)
                    print("画图结束")

                    #已放置好，将其添加到角色列表
                    self.role_list.append(self.moving_object)
                    # self.role.show(mx,my)
                    #将拖拽ui物体重新置为空
                    self.moving_object = None


                #如果当前没有在拖拽物体，这是一个基本状态
                else:
                    #判断当前是否在点击水平按钮
                    side_menu_button = self.horizonMenu.get_clicked(mouse_x, mouse_y)
                    #判断当前是否在点击垂直按钮
                    verti_menu_button = self.verticalMenu.get_clicked(mouse_x,mouse_y)

                    #判断当前是否在点击一个物体
                    candidate_role = self.choose_role(mouse_x, mouse_y)

                    # 如果点击了一个空地
                    if candidate_role is None:
                        #如果当前存在一个未设置目标的攻击者，就把当前点击的空地位置传给他
                        #此处也就完成了我们的攻击方式第二步，设置攻击的目标位置
                        #因此需要将moving_candidate置为空，方便对下一个点击的物体操作
                        if self.moving_candidate and self.moving_candidate.set_dest is False:
                            self.moving_candidate.dest_mx = mx
                            self.moving_candidate.dest_my = my
                            self.moving_candidate.set_dest = True
                            self.moving_candidate = None

                    #如果当前点击了一个物体，就该给他分配攻击对象了
                    else:
                        #我们将所有正在去攻击对象的路上的物体存放在candidate_list中
                        #因为我们可能再一次点击他，表示要重新给他分配攻击对象
                        #因此标志位set_dest置为false
                        if candidate_role in self.candidate_list:
                            candidate_role.set_dest = False
                        #如果当前选择的是没有攻击过别人的物体，就加入列表
                        else:
                            self.candidate_list.append(candidate_role)
                        #将点击的物体作为待分配攻击对象的候选者moving_candidate
                        self.moving_candidate = candidate_role

                    # 菜单的点击
                    if side_menu_button:
                        print(side_menu_button)
                        #点击的是水平菜单中的按钮就触发相应事件
                        self.add_weapon(side_menu_button)

                    #如果是垂直菜单按钮
                    if verti_menu_button:
                        print(verti_menu_button)

                    #对当前有了攻击对象的物体，进行寻路分配
                    for set_role in self.candidate_list:
                        print(set_role.next_mx, set_role.next_my)
                        set_role.find_path(self.game_map, (set_role.dest_mx, set_role.dest_my),self.screen_surf)

    def add_weapon(self, name):
        x, y = pygame.mouse.get_pos()
        name_list = ["Blue_solder", "Blue_weapon3", "Blue_weapon2", "Red_weapon2", "Red_weapon1", "Red_solder"]
        role_index_list = [6, 9, 48, 51, 54, 57]
        mx = (x - self.game_map.x) // 32
        my = (y - self.game_map.y) // 32

        # 这里就是涉及到武器，人物的初始化了
        object_list = []

        try:
            role = pygame.image.load('./source/img/character/hero.png').convert_alpha()


            #zmy 添加range,range = 100
            if (name =='Blue_solder') | (name=="Blue_weapon3") | (name=="Blue_weapon2") :
                obj = CharWalk(role, role_index_list[name_list.index(name)], CharWalk.DIR_DOWN, mx, my, 70, 'blue',self.screen_surf)
            else :
                obj = CharWalk(role, role_index_list[name_list.index(name)], CharWalk.DIR_DOWN, mx, my, 70, 'red',self.screen_surf)

            self.moving_object = obj
            # obj.moving = True
        except Exception as e:
            print(str(e) + "NOT VALID NAME")

    def add(self, name):
        x, y = pygame.mouse.get_pos()
        name_list = ["Blue_solder", "Blue_weapon3", "Blue_weapon2", "Red_weapon2", "Red_weapon1", "Red_solder"]

        # 这里就是涉及到武器，人物的初始化了
        object_list = []
        # object_list = [ArcherTowerLong(x,y), ArcherTowerShort(x,y), DamageTower(x,y), RangeTower(x,y)]

        try:
            obj = object_list[name_list.index(name)]
            self.moving_object = obj
            obj.moving = True
        except Exception as e:
            print(str(e) + "NOT VALID NAME")

    def choose_role(self, x, y):
        for candidate_role in self.role_list:
            if candidate_role.get_clicked(x, y):
                return candidate_role
        return None


if __name__ == '__main__':
    Game("versus", 710, 550)
