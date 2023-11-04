"""
    敌机基类
"""
# pylint: disable=no-name-in-module
import random
import pygame

import const

from plane_utils import screen, load_music, load_img
from screen_element import draw_blood_line


class EnemyBase(pygame.sprite.Sprite):
    """
    敌机基类
    """
    def __init__(self,
                 enemy_type: const.Enemy.Small |
                 const.Enemy.Mid | const.Enemy.Large):

        super().__init__()
        self.enemy_type = enemy_type

        self.images = list(map(load_img, self.enemy_type.IMAGES))
        self.destroy_images = list(map(
            load_img, self.enemy_type.DESTROY_IMAGES))

        self.down_music = load_music(self.enemy_type.ENEMY_DOWN_MUSIC)

        self.damage = self.enemy_type.DAMAGE
        self.kill_score = self.enemy_type.KILLSCORE

        self.index = 0

        self.rect = self.images[0].get_rect()
        self.speed = self.enemy_type.SPEED

        self.set_enemy_location()

        self.mask = pygame.mask.from_surface(self.images[0])

        self.const_blood = self.blood = self.enemy_type.BLOOD

        self.hit = False
        self.image_hit = None
        self.fly_sound = None

        self.active = True

    def move(self):
        """
        敌机移动
        """
        if self.rect.top < const.WINDOW_HEIGHT:
            self.rect.top += self.speed
        else:
            self.reset()

    def set_image_hit(self, path: str) -> None:
        """
        设置击中图片
        """
        self.image_hit = load_img(path)

    def set_fly_sound(self, path: str) -> None:
        """
        设置敌机飞行音乐
        """
        self.fly_sound = load_music(path)

    def set_enemy_location(self):
        """
        设置敌机位置
        """
        self.rect.left, self.rect.top = (
            random.randint(20, const.WINDOW_WIDTH - self.rect.width - 20),
            random.randint(-10 * self.rect.height, 0))

    def move_center(self):
        """
        敌机向屏幕中间移动
        """
        if self.enemy_type == const.Enemy.Large:
            return

        offset = self.enemy_type.OFFSET

        if self.rect.left > const.WINDOW_WIDTH // 2:
            self.rect.left = max(
                const.WINDOW_WIDTH // 2, self.rect.left - offset)

        else:
            self.rect.left = min(
                const.WINDOW_WIDTH // 2, self.rect.left + offset)

        if self.rect.top > const.WINDOW_HEIGHT // 3:
            self.rect.top = max(
                const.WINDOW_HEIGHT // 3, self.rect.top - offset)

        else:
            self.rect.top = min(
                const.WINDOW_HEIGHT // 3, self.rect.top + offset)

    def reset(self):
        """
        重置敌机数据
        """
        self.blood = self.const_blood
        self.set_enemy_location()
        self.active = True

    def draw(self, switch, delay) -> int:
        """
        绘制敌机

        switch: 切换大型战机运行时图片
        delay: 控制延迟

        返回值为敌机存活状态
        """
        if self.blood > 0 and self.active:
            self.move()
            if self.hit:
                if self.image_hit:
                    screen.blit(self.image_hit, self.rect)
                self.hit = False
            else:
                # 只有大型战机有两张图片
                if len(self.images) > 1:
                    screen.blit(self.images[switch], self.rect)
                else:
                    screen.blit(self.images[0], self.rect)

            # 绘制血条
            draw_blood_line(self.rect, -5, self.blood / self.const_blood)

            # (仅限大型战机) 即将出现在画面中，播放音效
            # 只有大型战机有音乐
            if self.fly_sound and self.rect.bottom == -50:
                self.fly_sound.play()
        else:
            if not delay % 3:
                if self.index == 0:
                    self.down_music.play()
                screen.blit(
                    self.destroy_images[self.index], self.rect)
                self.index = (self.index + 1) % len(self.destroy_images)
                if self.index == 0:
                    if self.fly_sound:
                        self.fly_sound.stop()
                    if self.blood <= 0:
                        self.reset()
                        return self.kill_score
                    self.reset()
        return 0

    def set_music_volume(self, vol: int):
        """
        设置音量
        """
        self.down_music.set_volume(vol)
