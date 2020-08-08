import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien
import json


def check_events(ai_setting, aliens, screen, a_ship, bullets, stats, play_button, sb):
    """响应鼠标和键盘事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_score(stats)
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_kdown_event(event, ai_setting, aliens, a_ship,
                              screen, bullets, stats)

        elif event.type == pygame.KEYUP:
            check_kup_event(event, a_ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets,
                              ai_setting, screen, a_ship, sb)


def check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets,
                      ai_setting, screen, a_ship, sb):
    """在玩家单击play按钮时开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ai_setting.initialize_dynamic_settings()

        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 开始游戏
        start_game(stats, aliens, bullets, ai_setting, screen, a_ship)


def start_game(stats, aliens, bullets, ai_setting, screen, a_ship):
    # 隐藏鼠标
    pygame.mouse.set_visible(False)

    # 重置游戏统计信息
    stats.reset_stats()
    stats.game_active = True

    # 清空外星人列表
    aliens.empty()
    bullets.empty()

    # 创建一群新的外星人
    create_fleet(ai_setting, screen, a_ship, aliens)
    a_ship.center_ship()


def check_kdown_event(event, ai_setting, aliens, a_ship, screen, bullets, stats):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        a_ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        a_ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_setting, screen, a_ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p and not stats.game_active:
        start_game(stats, aliens, bullets, ai_setting, screen, a_ship)


def check_kup_event(event, a_ship):
    """按键松开"""
    if event.key == pygame.K_RIGHT:
        a_ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        a_ship.moving_left = False


def update_screen(ai_setting, screen, a_ship, aliens, bullets, stats, play_button, sb):
    """更新屏幕"""
    # 每次循环更新屏幕
    screen.fill(ai_setting.bg_color)
    # 再飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    a_ship.blitme()
    aliens.draw(screen)

    # 显示得分
    sb.show_score()

    # 如果游戏处于非活动状态，绘制play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_setting, screen, a_ship, aliens, bullets, sb, stats):
    """管理子弹"""
    # 更新子弹位置
    bullets.update()

    # 删除消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_setting, screen, a_ship, aliens, bullets, stats
                                  , sb)


def check_bullet_alien_collisions(ai_setting, screen, a_ship, aliens, bullets, stats
                                  , sb):
    """检查是否有子弹击中外星人"""
    # 如果击中，删除相应的子弹及外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_setting.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # 删除子弹并创建新的外星人，加快游戏节奏, 更新等级
        bullets.empty()
        ai_setting.increase_speed()
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_setting, screen, a_ship, aliens)


def fire_bullets(ai_setting, screen, a_ship, bullets):
    """发射子弹"""
    # 创建一个子弹并写入到bullets编组中
    if len(bullets) < ai_setting.bullet_allow:
        new_bullet = Bullet(ai_setting, screen, a_ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_setting, alien_width):
    """计算每行可以容纳多少外星人"""
    available_apace_x = ai_setting.screen_width - 2 * alien_width
    number_aliens_x = int(available_apace_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_setting, ship_height, alien_height):
    """计算可容纳多少行外星人"""
    available_space_y = (ai_setting.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_setting, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_setting, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_setting, screen, a_ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可容纳多少外星人
    alien = Alien(ai_setting, screen)
    number_aliens_x = get_number_aliens_x(ai_setting, alien.rect.width)
    number_aliens_y = get_number_rows(ai_setting, a_ship.rect.height, alien.rect.height)
    
    # 创建一群外星人
    for row_number in range(number_aliens_y):
        for alien_number in range(number_aliens_x):
            create_alien(ai_setting, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_setting, aliens):
    """检测到外星人到达边界时采取措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_setting, aliens)
            break


def change_fleet_direction(ai_setting, aliens):
    """将外星人群下移，并改变方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_setting.fleet_drop_speed
    ai_setting.fleet_direction *= -1


def ship_hit(ai_setting, stats, screen, a_ship, aliens, bullets, sb):
    """响应被外星人撞到的飞船"""
    # 将飞船命数减少1
    if stats.ships_left > 0:
        stats.ships_left -= 1

        # 更新记分牌
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船至于底部中央
        create_fleet(ai_setting, screen, a_ship, aliens)
        a_ship.center_ship()
        sleep(0.6)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def update_aliens(ai_setting, aliens, a_ship, stats, screen, bullets, sb):
    """检测外星人是否位于边界，并更新外星人群中所有外星人位置"""
    check_fleet_edges(ai_setting, aliens)
    aliens.update()

    # 检测外星人与飞船的碰撞
    if pygame.sprite.spritecollideany(a_ship, aliens):
        ship_hit(ai_setting, stats, screen, a_ship, aliens, bullets, sb)

    # 检测是否到达屏幕底端
    check_alien_bottom(ai_setting, stats, screen, a_ship, aliens, bullets, sb)


def check_alien_bottom(ai_setting, stats, screen, a_ship, aliens, bullets, sb):
    """检测外星人到达屏幕底端"""
    for alien in aliens.sprites():
        screen_rect = screen.get_rect()
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_setting, stats, screen, a_ship, aliens, bullets, sb)


def check_high_score(stats, sb):
    """检测最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def save_score(stats):
    """保存最高分"""
    with open('abc.json', 'w') as obj:
        json.dump(stats.high_score, obj)


def score_load():
    """装载最高分"""
    with open('abc.json') as obj:
        score = json.load(obj)
        return score










