"""
    敌军基类
"""
# pylint: disable=no-name-in-module

import const
from enemy_base import EnemyBase
from plane_utils import load_img, load_music


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
        self.image_hit = load_img("./images/enemy_mid_hit.png")

        super().__init__(const.Enemy.Mid)


class LargeEnemy(EnemyBase):
    """
    大型敌机器
    """

    def __init__(self) -> None:

        self.image_hit = load_img("./images/enemy_large_hit.png")

        super().__init__(const.Enemy.Large)

        self.fly_sound = load_music(const.LARGE_ENEMY_FLY_SOUND)

    def set_music_volume(self, vol: int):
        """
        追加大型战机入场的音乐
        """
        super().set_music_volume(vol)
        self.fly_sound.set_volume(vol)
