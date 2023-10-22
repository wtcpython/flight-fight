"""
    敌机基类
"""
# pylint: disable=no-name-in-module
import random
import pygame

import const

from plane_utils import screen, load_music, load_img


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

        self.kill_score = self.enemy_type.KILLSCORE

        self.index = 0

        self.rect = self.images[0].get_rect()
        self.speed = self.enemy_type.SPEED
        self.active = True

        self.set_enemy_location()

        self.mask = pygame.mask.from_surface(self.images[0])

        self.const_blood = self.blood = self.enemy_type.BLOOD

        self.hit = False

    def move(self):
        """
        敌机移动
        """
        if self.rect.top < const.WINDOW_HEIGHT:
            self.rect.top += self.speed
        else:
            self.reset()

    def set_enemy_location(self):
        """
        设置敌机位置
        """
        self.rect.left, self.rect.top = \
            random.randint(20, const.WINDOW_WIDTH - self.rect.width - 20), \
            random.randint(-10 * self.rect.height, 0)

    def reset(self):
        """
        重置敌机数据
        """
        self.active = True
        self.blood = self.const_blood
        self.set_enemy_location()

    def draw(self, switch, delay) -> int:
        """
        绘制敌机

        switch: 切换大型战机运行时图片
        delay: 控制延迟

        返回值为敌机存活状态
        """
        if self.active and self.blood > 0:
            self.move()
            if self.hit:
                if hasattr(self, "image_hit"):
                    screen.blit(self.image_hit, self.rect)
                self.hit = False
            else:
                # 只有大型战机有两张图片
                if len(self.images) > 1:
                    screen.blit(self.images[switch], self.rect)
                else:
                    screen.blit(self.images[0], self.rect)
            pygame.draw.line(
                screen, (0, 0, 0),
                (self.rect.left, self.rect.top - 5),
                (self.rect.right, self.rect.top - 5), 2)

            energy_remain = self.blood / self.const_blood
            pygame.draw.line(
                screen, (0, 255, 0),
                (self.rect.left, self.rect.top - 5),
                (self.rect.left + self.rect.width * energy_remain,
                    self.rect.top - 5), 2)

            # (仅限大型战机) 即将出现在画面中，播放音效
            # 只有大型战机有音乐
            if hasattr(self, "fly_sound"):
                if self.rect.bottom == -50:
                    self.fly_sound.play()
        else:
            if not delay % 3:
                if self.index == 0:
                    self.down_music.play()
                screen.blit(
                    self.destroy_images[self.index], self.rect)
                self.index = (self.index + 1) % len(self.destroy_images)
                if self.index == 0:
                    if hasattr(self, "fly_sound"):
                        self.fly_sound.stop()
                    self.reset()
                    return self.kill_score
        return 0

    def set_music_volume(self, vol: int):
        """
        设置音量
        """
        self.down_music.set_volume(vol)
