class Settings():
    '''存储《外星人入侵》的所有设置'''

    def __init__(self):
        # 屏幕及飞船设置
        self.screen_height = 800
        self.screen_width = 1200
        self.bg_color = (230, 230, 230)
        self.ship_speed_factor = 1.5
        # 子弹设置
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 20
        # 外星人设置
