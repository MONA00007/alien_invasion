import sys

import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens,
                         bullets):
    # * 按下事件
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # 创建一个子弹，并将其加入到bullets编组中(少于限制数量内)
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p and not stats.game_active:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # 上下移动
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True


def check_keyup_events(event, ship):
    # * 松开事件
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    # 上下移动
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets):
    # *监视键盘和鼠标事件
    for event in pygame.event.get():
        # 关闭游戏事件
        if event.type == pygame.QUIT:
            sys.exit()
        # 键盘左右移动事件
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings,
                                 screen, stats, sb, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        # 开始游戏按钮
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  play_button):
    # *更新屏幕上的图像，并切换到新屏幕
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # 显示得分
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # * 更新子弹的位置和删除消失的子弹
    bullets.update()
    # 删除消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(
        ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens,
                                  bullets):
    # *检查是否有外星人被子弹击中
    # *击中则删除子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points*len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    # 如果外星人被消灭完则再新建一群外星人,并加速和提高等级
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        # 提高等级
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets):
    # * 没达到限制，就发射一发子弹
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(ai_settings, screen, ship, aliens):
    # *创建外星人群
    # 计算外星人间距
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens(ai_settings, alien.rect.width)
    number_rows = get_number_rows(
        ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        # 创建一群外星人
        # 创建第一行外星人
        for alien_number in range(number_aliens_x):
            # 创建一个外星人并将其加入当前行
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_aliens(ai_settings, alien_width):
    # *计算外星人间距

    avaiable_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(avaiable_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # *创建第一行外星人
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height+2+alien.rect.height*row_number
    aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_height):
    # *屏幕可容纳多少行外星人
    avaiable_space_y = (ai_settings.screen_height -
                        (3 * alien_height) - ship_height)
    number_rows = int(avaiable_space_y / (2 * alien_height))
    return number_rows


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # *检查外星人是否到达边境，更新外星人群的设置
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # 检查是否有外星人到达屏幕底部
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def change_fleet_direction(ai_settings, aliens):
    # * 将外星人群下移，并改变方向
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= - 1


def check_fleet_edges(ai_settings, aliens):
    # * 外星人到达边缘后采取措施
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # *飞船撞击外星人事件
    # 被外星人撞到飞船数减一，并清空子弹和外星人
    if stats.ships_left > 0:
        stats.ships_left -= 1
        # 更新记分牌
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        # 新建外星人和飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # * 检查外星人是否到达屏幕底部
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if screen_rect.bottom <= alien.rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                      aliens, bullets, mouse_x, mouse_y):
    # * 按下Play按钮开始游戏
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        # *隐藏光标
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)


def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # *开始游戏
    pygame.mouse.set_visible(False)
    # 重置游戏统计数据
    stats.reset_stats()
    stats.game_active = True
    # 重置计分牌图像
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    aliens.empty()
    bullets.empty()
    # 新建外星人和飞船居中
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def check_high_score(stats, sb):
    # *检查是否诞生了最高分
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
