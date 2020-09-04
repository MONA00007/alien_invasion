import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    # 创建一艘飞船和子弹组
    ship = Ship(ai_settings, screen)
    bullets = Group()

    # 开始游戏的主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(bullets)

        # 每次循环时都重绘屏幕
        # 让最近绘制的屏幕可见
        gf.update_screen(ai_settings, screen, ship, bullets)
       

<<<<<<< HEAD

=======
nmslnmsl
>>>>>>> 57675d46de3908b3bcc0fca0ff3f19bb5213fbd1
run_game()
