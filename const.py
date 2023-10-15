"""
    常量定义
"""

WINDOW_TITLE = "飞机大战V0.1"

WINDOW_WIDTH = 658
WINDOW_HEIGHT = 960

WINDOW_FRAME_WIDTH = 10

MY_PLANE_SPEED = 8
SUPPLY_SPEED = 6

# 基础伤害
BOMB_DAMAGE_MIN = 15
BOMB_DAMAGE_MAX = 25

# 暴击率
CRIT_RATE = 0.2

# 暴击伤害
CRIT_DAMAGE = 2.4


BULLET1_SPEED = 8
BULLET2_SPEED = 10


# 音乐和音效
BG_MUSIC_MAIN = "./sound/bgm.mp3"
BULLET_SOUND = "./sound/bullet.ogg"
BOMB_SOUND = "./sound/bomb.ogg"
SUPPLY_SOUND = "./sound/supply.ogg"
GET_BOMB_SOUND = "./sound/get_bomb.ogg"
GET_BULLET_SOUND = "./sound/get_bullet.ogg"
UPGRADE_SOUND = "./sound/upgrade.ogg"
LARGE_ENEMY_FLY_SOUND = "./sound/large_enemy_flying.ogg"
ME_DOWN_SOUND = "./sound/me_down.ogg"


class Status:
    """
    玩家当前状态
    """
    PLAY = 0
    PAUSE = 1
    LOGIN = 2


class BulletType:
    """
    子弹类型
    """
    NORMAL = 0
    PLUS = 1


class Enemy:
    """
    敌机固定参数
    """

    class Type:
        """
        种类
        """
        SMALL = 0
        MID = 1
        LARGE = 2

    class Small:
        """
        小飞机
        """
        KILLSCORE = 120
        SPEED = 2
        BLOOD = 20 * 3
        ENEMY_DOWN_MUSIC = "./sound/small_enemy_down.ogg"
        IMAGES = [
            "./images/enemy_small.png"]
        DESTROY_IMAGES = [
            "./images/enemy_small_down1.png",
            "./images/enemy_small_down2.png",
            "./images/enemy_small_down3.png",
            "./images/enemy_small_down4.png"]

    class Mid:
        """
        中飞机
        """
        KILLSCORE = 230
        SPEED = 1.2
        BLOOD = 20 * 7
        ENEMY_DOWN_MUSIC = "./sound/mid_enemy_down.ogg"
        IMAGES = [
            "./images/enemy_mid.png"]
        DESTROY_IMAGES = [
            "./images/enemy_mid_down1.png",
            "./images/enemy_mid_down2.png",
            "./images/enemy_mid_down3.png",
            "./images/enemy_mid_down4.png"]

    class Large:
        """
        大飞机
        """
        KILLSCORE = 700
        SPEED = 1
        BLOOD = 20 * 18
        ENEMY_DOWN_MUSIC = "./sound/large_enemy_down.ogg"
        IMAGES = [
            "./images/enemy_large_1.png",
            "./images/enemy_large_2.png"]
        DESTROY_IMAGES = [
            "./images/enemy_large_down1.png",
            "./images/enemy_large_down2.png",
            "./images/enemy_large_down3.png",
            "./images/enemy_large_down4.png",
            "./images/enemy_large_down5.png",
            "./images/enemy_large_down6.png"]
