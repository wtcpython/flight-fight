"""
    敌军基类
"""
# pylint: disable=no-name-in-module

import const
from enemy_base import EnemyBase


class SmallEnemy(EnemyBase):
    """
    小型敌机器
    """

    def __init__(self) -> None:

        super().__init__(const.Enemy.Small)


class MidEnemy(EnemyBase):
    """
    中型敌机器
    """

    def __init__(self) -> None:
        super().__init__(const.Enemy.Mid)

        self.set_image_hit(const.Enemy.Mid.ImageHit)


class LargeEnemy(EnemyBase):
    """
    大型敌机器
    """

    def __init__(self) -> None:
        super().__init__(const.Enemy.Large)

        self.set_image_hit(const.Enemy.Large.ImageHit)
        self.set_fly_sound(const.Enemy.Large.FlySound)

    def set_music_volume(self, vol: int):
        """
        追加大型战机入场的音乐
        """
        super().set_music_volume(vol)
        self.fly_sound.set_volume(vol)
