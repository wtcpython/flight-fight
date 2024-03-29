"""
    子弹基类
"""
# pylint: disable=no-name-in-module
import random
import pygame

import const

from utils import screen, load_img
from enemy_base import EnemyBase


class BulletBase:
    """
    己方飞机子弹基类
    """
    def __init__(self, pos, bullet_type: const.BulletType):
        if bullet_type == const.BulletType.Normal:
            self.image = load_img("./images/bullet1.png")
        elif bullet_type == const.BulletType.Plus:
            self.image = load_img("./images/bullet2.png")

        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.speed = const.BULLET_SPEED
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def damage(self) -> int:
        """
        计算子弹所造成的伤害
        """
        base_damage = const.Player.Damage
        is_crit = random.random() < const.Player.CritRate
        if is_crit:
            base_damage *= const.Player.CritDamage
        return base_damage

    def move(self):
        """
        子弹移动
        """
        self.rect.top -= self.speed

        if self.rect.top < self.speed:
            self.active = False

    def reset(self, pos):
        """
        重置子弹
        """
        self.rect.topleft = pos
        self.active = True

    def check_hit(self, enemies):
        """
        检查子弹命中情况
        """
        if self.active:
            self.move()
            screen.blit(self.image, self.rect)
            enemy_hit = pygame.sprite.spritecollide(
                self, enemies, False, pygame.sprite.collide_mask)
            if enemy_hit:
                self.active = False
                for enemy in enemy_hit:
                    self.bullet_hit_event(enemy)

    def bullet_hit_event(self, enemy: EnemyBase):
        """
        子弹击中事件
        """
        enemy.hit = True
        enemy.blood -= self.damage()
