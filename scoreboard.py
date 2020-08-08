import pygame.ftfont
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    """显示得分信息的类"""

    def __init__(self, ai_setting, screen, stats):
        """初始化显示得分涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_setting = ai_setting
        self.stats = stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # 准备初始得分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color
                                            , self.ai_setting.bg_color)

        # 将记分牌放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高得分转换为一幅渲染图像"""
        high_score = int(round(self.stats.high_score, -1))
        score_high_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(
            score_high_str, True,
            self.text_color, self.ai_setting.bg_color
        )

        # 将记分牌放在屏幕正上方
        self.score_high_rect = self.high_score_image.get_rect()
        self.score_high_rect.top = 20
        self.score_high_rect.centerx = self.screen_rect.centerx

    def prep_level(self):
        """将等级转换为一幅渲染图像"""
        self.level_image = self.font.render(('level:' + str(self.stats.level)), True,
                                            self.text_color, self.ai_setting.bg_color)

        # 将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """显示剩下的飞船数"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_setting, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.score_high_rect)
        self.screen.blit(self.level_image, self.level_rect)

        # 绘制飞船
        self.ships.draw(self.screen)