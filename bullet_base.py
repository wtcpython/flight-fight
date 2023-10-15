"""
    子弹基类
"""
# pylint: disable=no-name-in-module
import random
import pygame

import const

from plane_utils import screen, load_img


class BulletBase:
    """
    己方飞机子弹基类
    """
    def __init__(self, pos, bullet_type: const.BulletType):
        if bullet_type == const.BulletType.NORMAL:
            self.image = load_img("./images/bullet1.png")
        elif bullet_type == const.BulletType.PLUS:
            self.image = load_img("./images/bullet2.png")

        self.rect = self.image.get_rect()
        self.init_pos = pos
        self.set_bullet_location(pos)
        self.speed = 7
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)
        self.penetrate = False

    def damage(self) -> int:
        """
        计算子弹所造成的伤害
        """
        base_damage = random.randint(
            const.BOMB_DAMAGE_MIN, const.BOMB_DAMAGE_MAX)
        is_crit = random.random() < const.CRIT_RATE
        if is_crit:
            base_damage = base_damage * const.CRIT_DAMAGE
        return base_damage

    def move(self):
        """
        子弹移动
        """
        self.rect.top -= self.speed

        if self.rect.top < self.speed:
            self.active = False

    def set_bullet_location(self, pos):
        """
        设置子弹生成位置
        """
        self.rect.left, self.rect.top = pos

    def reset(self, pos):
        """
        重置子弹
        """
        self.set_bullet_location(pos)
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
                self.active = self.penetrate
                for enemy in enemy_hit:
                    enemy.hit = True
                    enemy.blood -= self.damage()
