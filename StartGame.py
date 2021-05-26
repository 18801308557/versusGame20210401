import sys
import os
import pygame
import random
from gameDemo import Game
import pygame_menu

def set_difficulty(value, difficulty):
    pass


def start_the_game():
    Game("versus", 710, 550)


if __name__ == '__main__':
    """
    pygame.init()
    surface = pygame.display.set_mode((710,550))
    menu = pygame_menu.Menu(300,400,'welcome',theme=pygame_menu.themes.THEME_BLUE)
    menu.add_text_input('Name :', default='John Doe')
    menu.add_selector('Difficulty :', [('Hard', 1), ('Easy', 2)],
                      onchange=set_difficulty)
    menu.add_button('Play', start_the_game)
    #menu.add.toggle_switch('range:',False)
    menu.add_button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(surface)
    """


    pygame.init()
    surface = pygame.display.set_mode((710,550))
    mymenu = pygame_menu.Menu(300,400,'welcome',theme=pygame_menu.themes.THEME_BLUE)
    mymenu.add.text_input('Name :', default='BJTU')
    mymenu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)],
                      onchange=set_difficulty)
    mymenu.add.button('Play', start_the_game)
    #menu.add.toggle_switch('range:',False)
    mymenu.add.button('Quit', pygame_menu.events.EXIT)

    while True:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if mymenu.is_enabled():
            mymenu.update(events)
            mymenu.draw(surface)


        pygame.display.update()



