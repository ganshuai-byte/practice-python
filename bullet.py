import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """对子弹管理的类"""

    def __init__(self, ai_setting, screen, a_ship):
        """在飞船所在位置创建一个子弹对象"""
        super().__init__()
        self.screen = screen

        # 在（0，0）处创建一个子弹矩形，再设置到正确位置
        self.rect = pygame.Rect(0, 0, ai_setting.bullet_width, ai_setting.bullet_height)
        self.rect.centerx = a_ship.rect.centerx
        self.rect.top = a_ship.rect.top

        # 存储小数表示子弹位置
        self.y = float(self.rect.y)

        self.color = ai_setting.bullet_color
        self.speed_factor = ai_setting.bullet_speed_factor

    def update(self):
        """向上移动子弹"""
        # 更新子弹位置的小数值
        self.y -= self.speed_factor
        # 更新表示子弹rect位置
        self.rect.y = self.y

    def draw_bullet(self):
        """绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)





