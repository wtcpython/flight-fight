"""
    飞机基类
"""
# pylint: disable=no-name-in-module
import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN

import const
from plane_utils import screen, load_img, load_music
from screen_element import draw_blood_line


class Plane(pygame.sprite.Sprite, const.Player):
    """
    我方飞机
    """
    def __init__(self):
        super().__init__()

        # 我方飞机正常情况图片
        self.images = [
            load_img("./images/me1.png"),
            load_img("./images/me2.png")]

        # 我方飞机死亡图片
        self.destroy_images = [
            load_img("./images/me_destroy_1.png"),
            load_img("./images/me_destroy_2.png"),
            load_img("./images/me_destroy_3.png"),
            load_img("./images/me_destroy_4.png")]

        self.rect = self.images[0].get_rect()

        self.set_plane_location()

        self.index = 0

        self.collide_music = load_music(const.ME_COLLIDE_SOUND)

        self.active = True

        self.mask = pygame.mask.from_surface(self.images[0])

        self.cur_blood = self.Blood

    def move(self):
        """
        键盘控制移动
        """
        pressed = pygame.key.get_pressed()
        if pressed[K_UP] and self.rect.top > self.Speed:
            self.rect.top -= self.Speed
        elif pressed[K_DOWN] and \
                self.rect.bottom < const.Window.Height - self.Speed:
            self.rect.top += self.Speed
        elif pressed[K_LEFT] and \
                self.rect.left > self.Speed:
            self.rect.left -= self.Speed
        elif pressed[K_RIGHT] and \
                self.rect.right < const.Window.Width - self.Speed:
            self.rect.right += self.Speed

    def set_plane_location(self):
        """
        将我方飞机放置于屏幕正中央下方
        """
        self.rect.center = (const.Window.Width // 2,
                            const.Window.Height - self.rect.height // 2)

    def reset(self):
        """
        重置飞机
        """
        self.active = True
        self.set_plane_location()
        self.cur_blood = self.Blood

    def check_active(self, switch, enemies):
        """
        检查我方飞机是否存活
        """
        # 检测我方飞机是否被撞
        enemies_down = pygame.sprite.spritecollide(
            self, enemies,
            False, pygame.sprite.collide_mask)
        if enemies_down:
            for enemy in enemies_down:
                if enemy.active:
                    enemy.active = False
                    self.collide_music.play()
                    self.cur_blood -= enemy.damage
                    if self.cur_blood <= 0:
                        self.active = False

        # 绘制我方飞机
        if self.active:
            if switch:
                screen.blit(self.images[0], self.rect)
            else:
                screen.blit(self.images[1], self.rect)

            # 绘制血条
            draw_blood_line(self.rect, 95, self.cur_blood / self.Blood)

    def set_music_volume(self, vol: int):
        """
        设置音量
        """
        self.collide_music.set_volume(vol)
