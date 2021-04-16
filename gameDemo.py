import sys
import os
import pygame

from core import GameMap, CharWalk, Sprite
from menu.menu import horizontalMenu

side_img = pygame.transform.scale(pygame.image.load("./source/img/menu/bg1.png"), (640, 70))
Blue_solder = pygame.transform.scale(pygame.image.load("./source/img/menu/Blue_solder.png"), (64, 64))
Blue_weapon2 = pygame.transform.scale(pygame.image.load("./source/img/menu/Blue_weapon2.png"), (64, 64))
Blue_weapon3 = pygame.transform.scale(pygame.image.load("./source/img/menu/Blue_weapon3.png"), (64, 64))
Red_solder = pygame.transform.scale(pygame.image.load("./source/img/menu/Red_solder.png"), (64, 64))
Red_weapon2 = pygame.transform.scale(pygame.image.load("./source/img/menu/Red_weapon2.png"), (64, 64))
Red_weapon1 = pygame.transform.scale(pygame.image.load("./source/img/menu/weapon1.png"), (64, 64))


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
        self.menu = horizontalMenu(self.width - side_img.get_width(), self.height - side_img.get_height(), side_img)
        self.menu.add_btn(Blue_solder, "Blue_solder", 200)
        self.menu.add_btn(Blue_weapon2, "Blue_weapon2", 200)
        self.menu.add_btn(Blue_weapon3, "Blue_weapon3", 200)
        self.menu.add_btn(Red_solder, "Red_solder", 200)
        self.menu.add_btn(Red_weapon1, "Red_weapon1", 200)
        self.menu.add_btn(Red_weapon2, "Red_weapon2", 200)
        self.role_list = []
        self.weapon_list = []
        self.candidate_list = []
        self.moving_candidate = None
        self.moving_object = None

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
        self.role = CharWalk(self.hero, 48, CharWalk.DIR_DOWN, 5, 10)

    def update(self):
        while True:
            self.clock.tick(self.fps)

            # 逻辑更新
            for mobile in self.role_list:
                mobile.logic()
            self.event_handler()
            # 画面更新
            self.game_map.draw_bottom(self.screen_surf)

            if self.moving_object:
                m_x, m_y = pygame.mouse.get_pos()
                mx = (m_x - self.game_map.x) // 32
                my = (m_y - self.game_map.y) // 32
                self.moving_object.show(mx, my)
                self.moving_object.draw(self.screen_surf, self.game_map.x, self.game_map.y)
            # else:
            for mobile in self.role_list:
                mobile.draw(self.screen_surf, self.game_map.x, self.game_map.y)
                # mobile.has_showed = True

            # self.game_map.draw_top(self.screen_surf)
            #self.game_map.draw_grid(self.screen_surf)
            self.menu.draw(self.screen_surf)
            pygame.display.update()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mx = (mouse_x - self.game_map.x) // 32
                my = (mouse_y - self.game_map.y) // 32
                if self.moving_object:
                    print("check1")
                    self.role_list.append(self.moving_object)
                    # self.role.show(mx,my)
                    self.moving_object = None
                else:
                    side_menu_button = self.menu.get_clicked(mouse_x, mouse_y)
                    candidate_role = self.choose_role(mouse_x, mouse_y)

                    # 判断是否选择相应的角色移动
                    if candidate_role is None:
                        if self.moving_candidate and self.moving_candidate.set_dest is False:
                            self.moving_candidate.dest_mx = mx
                            self.moving_candidate.dest_my = my
                            self.moving_candidate.set_dest = True
                            self.moving_candidate = None
                    else:
                        if candidate_role in self.candidate_list:
                            candidate_role.set_dest = False
                        else:
                            self.candidate_list.append(candidate_role)
                        self.moving_candidate = candidate_role

                    # 菜单的点击
                    if side_menu_button:
                        print(side_menu_button)
                        self.add_weapon(side_menu_button)

                    for set_role in self.candidate_list:
                        print(set_role.next_mx, set_role.next_my)
                        set_role.find_path(self.game_map, (set_role.dest_mx, set_role.dest_my))

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
            obj = CharWalk(role, role_index_list[name_list.index(name)], CharWalk.DIR_DOWN, mx, my)
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
    Game("versus", 640, 550)
