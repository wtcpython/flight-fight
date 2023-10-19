"""
    飞机基类
"""
# pylint: disable=no-name-in-module
import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN

import const
from plane_utils import screen, load_img, load_music


class Plane(pygame.sprite.Sprite):
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

        self.down_music = load_music(const.ME_DOWN_SOUND)

        # 移动速度
        self.speed = const.MY_PLANE_SPEED

        self.active = True

        self.invincible = False
        self.mask = pygame.mask.from_surface(self.images[0])

    def move(self):
        """
        键盘控制移动
        """
        pressed = pygame.key.get_pressed()
        if pressed[K_UP] and self.rect.top > self.speed:
            self.rect.top -= self.speed
        elif pressed[K_DOWN] and \
                self.rect.bottom < const.WINDOW_HEIGHT - self.speed:
            self.rect.top += self.speed
        elif pressed[K_LEFT] and \
                self.rect.left > self.speed:
            self.rect.left -= self.speed
        elif pressed[K_RIGHT] and \
                self.rect.right < const.WINDOW_WIDTH - self.speed:
            self.rect.right += self.speed

    def set_plane_location(self):
        """
        将我方飞机放置于屏幕正中央下方
        """
        self.rect.center = (const.WINDOW_WIDTH // 2,
                            const.WINDOW_HEIGHT - self.rect.height // 2)

    def reset(self):
        """
        重置飞机
        """
        self.active = True
        self.invincible = True
        self.set_plane_location()

    def check_active(self, switch, delay, enemies):
        """
        检查我方飞机是否存活
        """
        # 检测我方飞机是否被撞
        enemies_down = pygame.sprite.spritecollide(
            self, enemies,
            False, pygame.sprite.collide_mask)
        if enemies_down and not self.invincible:
            self.active = False
            for enemy in enemies_down:
                enemy.active = False

        # 绘制我方飞机
        if self.active:
            if switch:
                screen.blit(self.images[0], self.rect)
            else:
                screen.blit(self.images[1], self.rect)
        else:
            # 毁灭
            if not delay % 3:
                if self.index == 0:
                    self.down_music.play()
                screen.blit(
                    self.destroy_images[self.index], self.rect)
                self.index = (self.index + 1) % len(self.destroy_images)
                if self.index == 0:
                    return False
        return True
