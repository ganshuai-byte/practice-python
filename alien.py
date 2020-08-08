import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_setting, screen):
        """初始化外星人并设置其启示位置"""
        super(Alien, self).__init__()
        self.ai_setting = ai_setting
        self.screen = screen

        # 加载外星人图像，设置rect属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # 设置外星人在左上角的初始位置
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人准确位置
        self.x = float(self.rect.x)

    def update(self):
        """向右移动外星人"""
        self.x += (self.ai_setting.alien_speed_factor
                   * self.ai_setting.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """检测外星人位于边缘时，返回ture"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)

