class GameStats():
    # *记录跟踪游戏统计信息
    def __init__(self, ai_settings):
        # 初始化统计信息
        self.ai_settings = ai_settings
        self.reset_stats()

    def reset_stats(self):
        # 初始化会变化的统计数据
        self.ships_left = self.ai_settings.ship_limit
