import pygame
import settings
import ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_setting = settings.Setting()
    screen = pygame.display.set_mode((
        ai_setting.screen_width, ai_setting.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 创建一个用于存储游戏统计数据的实例， 并创建记分牌
    stats = GameStats(ai_setting)
    sb = Scoreboard(ai_setting, screen, stats)

    # 创建一艘飞船，一个子弹编组，一个外星人编组
    a_ship = ship.Ship(ai_setting, screen)
    bullets = Group()
    aliens = Group()

    # 创建外星人群
    gf.create_fleet(ai_setting, screen, a_ship, aliens)

    # 创建play按钮
    play_button = Button(ai_setting, screen, 'Play')

    # 开始游戏的主循环
    while True:
        gf.check_events(ai_setting, aliens, screen, a_ship,
                        bullets, stats, play_button, sb)

        if stats.game_active:
            a_ship.update()
            gf.update_bullets(ai_setting, screen, a_ship, aliens, bullets, sb, stats)
            gf.update_aliens(ai_setting, aliens, a_ship, stats, screen, bullets, sb)

        gf.update_screen(ai_setting, screen, a_ship, aliens,
                         bullets, stats, play_button, sb)


run_game()
