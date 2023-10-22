"""
    补给基类
"""
# pylint: disable=no-name-in-module
# pylint: disable=c-extension-no-member
import random
import pygame

import const

from plane_utils import screen, load_img, load_music


class SupplyBase(object):
    """
    游戏内所有补给的框架基类
    """
    def __init__(self,
                 image: pygame.surface.Surface,
                 get_supply_music) -> None:

        self.image = image
        self.rect = self.image.get_rect()
        self.get_supply = load_music(get_supply_music)

        self.set_supply_location()

        # 设置移动速度
        self.speed = const.SUPPLY_SPEED
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        """
        补给移动
        """
        if self.rect.top < const.WINDOW_HEIGHT:
            self.rect.top += self.speed
        else:
            self.active = False

    def set_supply_location(self):
        """
        设置补给初始化位置
        """
        self.rect.left, self.rect.bottom = (
            random.randint(0, const.WINDOW_WIDTH - self.rect.width), -10)

    def reset(self):
        """
        重置补给
        """
        self.active = True
        self.set_supply_location()

    def check_active(self, my_plane) -> bool:
        """
        检测补给获取情况并绘制
        """
        if self.active:
            self.move()
            screen.blit(self.image, self.rect)
            if pygame.sprite.collide_mask(
                    self, my_plane):
                self.get_supply.play()
                return True
        return False

    def set_music_volume(self, vol: int):
        """
        设置音量
        """
        self.get_supply.set_volume(vol)


class BulletSupply(SupplyBase):
    """
    子弹补给
    """
    def __init__(self):
        self.image = load_img("./images/bullet_supply.png")
        super().__init__(self.image, const.GET_BULLET_SOUND)


class BombSupply(SupplyBase):
    """
    炸弹补给
    """
    def __init__(self):
        self.image = load_img("./images/bomb_supply.png")
        super().__init__(self.image, const.GET_BOMB_SOUND)
