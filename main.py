"""
    飞机大战主文件
"""
# pylint: disable=c-extension-no-member
# pylint: disable=no-name-in-module

# python 自带模块加载
import sys
import random

# 第三方模块加载
import pygame

# 自己的模块加载
import const

from enemy import SmallEnemy, MidEnemy, LargeEnemy

from plane_utils import (
    screen, load_music, load_img, read_json, write_json)

from bullet_base import BulletBase
from plane_base import Plane
from supply_base import BulletSupply, BombSupply
from screen_element import show_score, show_bomb_info, show_life_num_info
from volume_control import VolumeControlBase
from login_box import LoginBox
from text_rect import TextRect

pygame.base.init()
pygame.mixer.init()

bullet_sound = load_music("./sound/bullet.ogg")
bomb_sound = load_music("./sound/use_bomb.ogg")
supply_sound = load_music("./sound/supply.ogg")

sound_list = [bullet_sound, bomb_sound, supply_sound]


class Main:
    """
    plft
    """
    def __init__(self):
        pygame.display.set_caption(const.WINDOW_TITLE)
        # 基本框架

        self.background = load_img("./images/background.png")
        pygame.display.set_icon(load_img("./icon.ico"))

        # 战机初始化
        self.my_plane = Plane()
        self.enemies = pygame.sprite.Group()
        self.small_enemies = pygame.sprite.Group()
        self.mid_enemies = pygame.sprite.Group()
        self.big_enemies = pygame.sprite.Group()

        # 特殊事件
        self.bullet_supply = BulletSupply()
        self.bomb_supply = BombSupply()

        self.supply_time = pygame.constants.USEREVENT
        self.double_bullet_time = pygame.constants.USEREVENT + 1
        self.invincible_time = pygame.constants.USEREVENT + 2
        self.switch_image = True

        # 暂停初始化
        self.pause_images = [
            load_img("./images/pause.png"),
            load_img("./images/pause_pressed.png"),
            load_img("./images/continue.png"),
            load_img("./images/continue_pressed.png"),
        ]

        self.pause_rect = self.pause_images[0].get_rect()

        self.pause_rect.left, self.pause_rect.top = \
            const.WINDOW_WIDTH - self.pause_rect.width - 10, 10

        self.current_pause_image = self.pause_images[0]
        self.clock = pygame.time.Clock()

        # 登录输入框
        self.login_box = LoginBox()

        # 是否超级子弹
        self.super_bullet = False

        self.status = const.Status.LOGIN

        self.account = ""
        self.loggedin = False

        # 统计得分
        self.score = 0
        self.bomb_num = 0
        self.life_num = 0

        # 音量
        self.snd = self.vol = 0.2

    def init_game(self, data_mode):
        """
        游戏数据初始化
        """

        self.my_plane.reset()
        self.my_plane.invincible = False

        # 清空敌机里现有的飞机
        self.enemies.empty()
        self.small_enemies.empty()
        self.mid_enemies.empty()
        self.big_enemies.empty()

        # 增加飞机数量，顺序：小、中、大
        self.increase_enemies(15, 6, 2)

        self.score = 0

        # 游戏主音乐加载
        pygame.mixer.music.load("./sound/bgm.mp3")
        pygame.mixer.music.set_volume(self.vol)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause()

        # 全屏炸弹
        self.bomb_num = data_mode["BombNum"]

        # 生命数量
        self.life_num = data_mode["LifeNum"]

    def main(self):
        """
        主函数
        """
        if self.loggedin:
            text = f"Welcome,{self.account} !"
        else:
            text = "登   录"

        login_title = TextRect(
            text, const.Color.WHITE,
            (const.WINDOW_WIDTH // 2, const.WINDOW_FRAME_WIDTH * 5))

        data = read_json("./userdata/all_users.json")

        # 生成普通子弹、超级子弹
        bullet_length = 30
        normal_bullet = [BulletBase(self.my_plane.rect.midtop,
                                    const.BulletType.NORMAL)
                         for _ in range(bullet_length)]

        plus_bullet = [[
            BulletBase((self.my_plane.rect.centerx - 33,
                        self.my_plane.rect.centery), const.BulletType.PLUS),
            BulletBase(self.my_plane.rect.midtop, const.BulletType.PLUS),
            BulletBase((self.my_plane.rect.centerx + 30,
                        self.my_plane.rect.centery), const.BulletType.PLUS)]
                       for _ in range(bullet_length)]
        bullet_index = 0

        # 高级暂停操作、音量调节
        volume_control = VolumeControlBase(
            "音量", self.vol, 0, const.WINDOW_HEIGHT // 3)
        sound_control = VolumeControlBase(
            "音效", self.snd, 0, const.WINDOW_HEIGHT // 3 + 60)

        # 用于阻止重复打开记录文件
        recorded = False

        # 游戏结束画面
        again_img = load_img("./images/again.png")
        again_rect = again_img.get_rect()
        exit_img = load_img("./images/exit.png")
        exit_rect = exit_img.get_rect()

        # 用于延迟
        delay = 100

        # Easy,Mid,Hard 三种类型关卡随机选择
        mode = "Easy"

        self.init_game(data[mode])

        while True:
            self.clock.tick(60)

            screen.fill((195, 200, 201))
            screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                match event.type:
                    case pygame.constants.QUIT:
                        pygame.base.quit()
                        sys.exit()
                    case pygame.constants.MOUSEBUTTONDOWN:
                        if self.loggedin and \
                                self.pause_rect.collidepoint(event.pos):
                            if self.status == const.Status.PLAY:
                                self.status = const.Status.PAUSE
                            else:
                                self.status = const.Status.PLAY

                        self.check_paused()

                        if self.status == const.Status.PLAY:
                            if self.life_num <= 0:
                                if again_rect.collidepoint(event.pos):
                                    self.init_game(data[mode])
                                    self.status = const.Status.PLAY
                                elif exit_rect.collidepoint(event.pos):
                                    pygame.base.quit()
                                    sys.exit()

                        elif self.status == const.Status.PAUSE:
                            volume_control.check(event.pos)
                            if sound_control.check(event.pos):
                                for i in sound_list:
                                    i.set_volume(self.snd)

                        elif self.status == const.Status.LOGIN:
                            self.login_box.check_event(event)

                    # 定义超级炸弹的伤害
                    case pygame.constants.KEYDOWN:
                        if self.status == const.Status.PLAY:
                            key = pygame.key.name(event.key)
                            if key == "space" and self.bomb_num:
                                self.bomb_num -= 1
                                bomb_sound.play()
                                for each in self.enemies:
                                    if each.rect.bottom > 0:
                                        each.blood -= 20*7
                            elif key == "h" and self.life_num >= 2:
                                self.life_num -= 1
                                self.bomb_num += 3
                            elif key == "r":
                                self.init_game(data[mode])
                                self.status = const.Status.PLAY
                        elif self.status == const.Status.LOGIN:
                            if event.key in [pygame.constants.K_RETURN, pygame.constants.K_KP_ENTER]:
                                self.account = self.login_box.check_enter()
                                login_title.set_text(
                                    f"Welcome,{self.account} !")
                                # login_title = render_text(
                                #     f"Welcome,{self.account} !",
                                #     (255, 255, 255))
                                self.loggedin = True
                                self.status = const.Status.PLAY
                                self.current_pause_image = self.pause_images[0]
                            self.login_box.check_event(event)
                    case self.supply_time:
                        supply_sound.play()
                        if random.randint(0, 1):
                            self.bomb_supply.reset()
                        else:
                            self.bullet_supply.reset()
                    case self.double_bullet_time:
                        self.super_bullet = False
                        pygame.time.set_timer(self.double_bullet_time, 0)
                    case self.invincible_time:
                        self.my_plane.invincible = False
                        pygame.time.set_timer(self.invincible_time, 0)

            match self.status:
                case const.Status.PLAY:
                    # 播放音乐
                    if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.unpause()

                    # 每28秒发放一个补给包
                    pygame.time.set_timer(self.supply_time, 2 * 1000)
                    screen.blit(self.current_pause_image, self.pause_rect)

                    # 分数信息
                    show_score(self.score)

                    if self.life_num > 0:
                        self.my_plane.move()

                        # 绘制全屏炸弹补给并检测是否获得
                        if self.bomb_supply.check_active(self.my_plane):
                            # 有小概率加2个
                            bomb_get = random.randint(0, 20)
                            self.bomb_num += 2 if bomb_get <= 7 else 1
                            self.bomb_supply.active = False

                        # 绘制超级子弹补给并检测是否获得
                        if self.bullet_supply.check_active(self.my_plane):
                            self.super_bullet = True
                            pygame.time.set_timer(
                                self.double_bullet_time, 25 * 1000)
                            self.bullet_supply.active = False

                        # 发射子弹
                        if not delay % 10 or "normal_bullet" not in locals():
                            bullet_sound.play()
                            bullet_index = (bullet_index + 1) % 30
                            if self.super_bullet:
                                plus_bullet[bullet_index][0].reset(
                                    (self.my_plane.rect.centerx - 33,
                                        self.my_plane.rect.centery))
                                plus_bullet[bullet_index][1].reset(
                                    self.my_plane.rect.midtop)
                                plus_bullet[bullet_index][2].reset(
                                    (self.my_plane.rect.centerx + 30,
                                        self.my_plane.rect.centery))
                            else:
                                normal_bullet[bullet_index].reset(
                                    self.my_plane.rect.midtop)

                        # 检测子弹是否击中敌机
                        for b in normal_bullet:
                            b.check_hit(self.enemies)

                        for bs in plus_bullet:
                            for b in bs:
                                b.check_hit(self.enemies)

                        # 绘制大型敌机
                        for each in self.big_enemies:
                            self.score += each.draw(self.switch_image, delay)

                        # 绘制中型敌机：
                        for each in self.mid_enemies:
                            self.score += each.draw(self.switch_image, delay)

                        # 绘制小型敌机：
                        for each in self.small_enemies:
                            self.score += each.draw(self.switch_image, delay)

                        # 绘制我方战机：
                        if self.my_plane and not self.my_plane.check_active(
                                self.switch_image, delay, self.enemies):
                            self.life_num -= 1
                            self.my_plane.reset()
                            pygame.time.set_timer(
                                self.invincible_time, 3 * 1000)

                        # 显示当前炸弹数量
                        show_bomb_info(self.bomb_num)

                        # 绘制剩余生命数量
                        show_life_num_info(self.life_num)
                    else:
                        # 背景音乐停止
                        pygame.mixer.music.fadeout(500)
                        # 停止全部音效
                        pygame.mixer.fadeout(500)
                        # 停止发放补给
                        pygame.time.set_timer(self.supply_time, 0)
                        if not recorded:
                            recorded = True
                            # 读取历史最高得分
                            save = read_json(
                                f"userdata/{self.account}.json")
                            record_score = save["BestScore"]
                            # 如果玩家得分高于历史最高得分，则存档
                            record_score = max(self.score, record_score)
                            save["BestScore"] = self.score
                            write_json(f"userdata/{self.account}.json", save)

                        # 绘制结束画面
                        game_over = TextRect(
                            "Win!" if self.score >= data[mode]["MinimumScore"]
                            else "Lose!", const.Color.WHITE,
                            (const.WINDOW_WIDTH // 2, 150))
                        game_over_rect = game_over.get_rect()
                        screen.blit(game_over.get_surface(), game_over_rect)

                        best_score = TextRect(
                            f"Best : {record_score}", const.Color.WHITE,
                            (const.WINDOW_WIDTH // 2, 100))
                        screen.blit(best_score.get_surface(),
                                    best_score.get_rect())

                        again_rect.left, again_rect.top = (
                            (const.WINDOW_WIDTH - again_rect.width) // 2,
                            (const.WINDOW_HEIGHT - again_rect.height)
                            // 2 - 30)
                        screen.blit(again_img, again_rect)

                        exit_rect.left, exit_rect.top = (
                            (const.WINDOW_WIDTH - exit_rect.width) // 2,
                            (const.WINDOW_HEIGHT - exit_rect.height) // 2 + 30)
                        screen.blit(exit_img, exit_rect)

                case const.Status.PAUSE:
                    self.check_paused()
                    volume_control.draw()
                    sound_control.draw()

                    screen.blit(self.current_pause_image, self.pause_rect)

                case const.Status.LOGIN:
                    self.login_box.update()
                    self.login_box.draw()
                    screen.blit(login_title.get_surface(),
                                login_title.get_rect())

            # 切换图片
            if not delay % 5:
                self.switch_image = not self.switch_image
            delay -= 1
            if not delay:
                delay = 100
            pygame.display.flip()

    def increase_enemies(self, s_num: int, m_num: int, b_num: int):
        for _ in range(s_num):
            e_1 = SmallEnemy()
            self.small_enemies.add(e_1)
            self.enemies.add(e_1)
        for _ in range(m_num):
            e_2 = MidEnemy()
            self.mid_enemies.add(e_2)
            self.enemies.add(e_2)
        for _ in range(b_num):
            e_3 = LargeEnemy()
            self.big_enemies.add(e_3)
            self.enemies.add(e_3)

    def check_paused(self):
        if self.status != const.Status.PLAY:
            self.current_pause_image = self.pause_images[3]
            pygame.time.set_timer(self.supply_time, 0)
            pygame.mixer.music.pause()
            pygame.mixer.pause()
        else:
            self.current_pause_image = self.pause_images[1]
            pygame.time.set_timer(self.supply_time, 2 * 1000)
            pygame.mixer.music.unpause()
            pygame.mixer.unpause()


if __name__ == "__main__":
    m = Main()
    m.main()
