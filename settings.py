class Settings():
    '''存储《外星人入侵》的所有设置'''

    def __init__(self):
        # *初始化游戏静态设置
        # 屏幕及飞船设置
        self.screen_height = 800
        self.screen_width = 1200
        self.bg_color = (230, 230, 230)
        self.ship_limit = 1
        # 子弹设置
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 20
        # 外星人设置
        self.fleet_drop_speed = 10

        # 加快游戏节奏
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # *初始化游戏中的变量
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        # 设置外星人的移动方向，-1为左，1为右
        self.fleet_direction = 1

    def increase_speed(self):
        # 提高速度设置
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
