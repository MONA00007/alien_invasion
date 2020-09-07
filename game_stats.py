class GameStats():
    # *记录跟踪游戏统计信息
    def __init__(self, ai_settings):
        # * 初始化统计信息
        self.ai_settings = ai_settings
        self.reset_stats()
        # 游戏刚启动时处于非活跃状态
        self.game_active = False
        # 在任何情况下都不应该重置最高得分
        self.high_score = 0

    def reset_stats(self):
        # *初始化会变化的统计数据
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
