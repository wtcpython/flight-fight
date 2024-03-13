"""
    常量定义
"""

VERSION = 0.6

SUPPLY_SPEED = 6

# 子弹移动速度
BULLET_SPEED = 7


# 音乐和音效
BG_MUSIC_MAIN = "./sound/bgm.mp3"
BULLET_SOUND = "./sound/bullet.ogg"
BOMB_SOUND = "./sound/bomb.ogg"
UPGRADE_SOUND = "./sound/upgrade.ogg"
ME_COLLIDE_SOUND = "./sound/me_collide.ogg"
SKILL_E_SOUND = "./sound/skill_e.ogg"
SKILL_Q_SOUND = "./sound/skill_q.ogg"


class Window:
    """
    窗口属性
    """
    Height = 960
    Width = 658
    FrameWidth = 10
    Title = f"飞机大战 V{VERSION}"


class Player:
    """
    玩家数据
    """
    Blood = 10000  # 生命值
    Damage = 20  # 攻击力
    CritRate = 0.2  # 暴击率
    CritDamage = 2.4  # 暴击伤害
    Speed = 8  # 移动速度
    ELoadTime = 10  # E技能加载时间
    QShowAnimationTime = 2  # Q技能充能动画时间


class Status:
    """
    玩家当前状态
    """
    Play = 0
    Pause = 1
    Login = 2


class BulletType:
    """
    子弹类型
    """
    Normal = 0
    Plus = 1


class Enemy:
    """
    敌机固定参数
    """

    class Small:
        """
        小飞机
        """
        Damage = 500
        KillScore = 120
        Speed = 2
        Blood = 20 * 3
        EnemyDownMusic = "./sound/small_enemy_down.ogg"
        Images = [
            "./images/enemy_small.png"]
        DestroyImages = [
            "./images/enemy_small_down1.png",
            "./images/enemy_small_down2.png",
            "./images/enemy_small_down3.png",
            "./images/enemy_small_down4.png"]
        Offset = 100

    class Mid:
        """
        中飞机
        """
        Damage = 700
        KillScore = 230
        Speed = 1.2
        Blood = 20 * 7
        EnemyDownMusic = "./sound/mid_enemy_down.ogg"
        Images = [
            "./images/enemy_mid.png"]
        DestroyImages = [
            "./images/enemy_mid_down1.png",
            "./images/enemy_mid_down2.png",
            "./images/enemy_mid_down3.png",
            "./images/enemy_mid_down4.png"]
        ImageHit = "./images/enemy_mid_hit.png"
        Offset = 40

    class Large:
        """
        大飞机
        """
        Damage = 1200
        KillScore = 700
        Speed = 1
        Blood = 20 * 18
        EnemyDownMusic = "./sound/large_enemy_down.ogg"
        Images = [
            "./images/enemy_large_1.png",
            "./images/enemy_large_2.png"]
        DestroyImages = [
            "./images/enemy_large_down1.png",
            "./images/enemy_large_down2.png",
            "./images/enemy_large_down3.png",
            "./images/enemy_large_down4.png",
            "./images/enemy_large_down5.png",
            "./images/enemy_large_down6.png"]
        ImageHit = "./images/enemy_large_hit.png"
        FlySound = "./sound/large_enemy_flying.ogg"
        Offset = 0
