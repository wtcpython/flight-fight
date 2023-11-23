"""
    飞机大战主文件
"""
# pylint: disable=c-extension-no-member
# pylint: disable=no-name-in-module

# python 自带模块加载
import sys
import random
import time

# 第三方模块加载
import pygame

# 自己的模块加载
import const

from enemy import SmallEnemy, MidEnemy, LargeEnemy

from plane_utils import (
    screen, load_music, load_img, read_json, write_json)

from bullet_base import BulletBase
from plane_base import Plane
from screen_element import (
    show_final_charge, show_score, show_bomb_info, show_blood_num,
    show_small_skill_charge)
from volume_control import VolumeControlBase
from login_box import LoginBox
from text_rect import TextRect

pygame.base.init()
pygame.mixer.init()

bullet_sound = load_music("./sound/bullet.ogg")
bomb_sound = load_music("./sound/use_bomb.ogg")
skill_e_sound = load_music("./sound/skill_e.ogg")
skill_q_sound = load_music("./sound/skill_q.ogg")

sound_list = [bullet_sound, bomb_sound, skill_e_sound, skill_q_sound]


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
        self.super_bullet_event = pygame.constants.USEREVENT
        self.add_bullet_damage_event = pygame.constants.USEREVENT + 1
        self.old_charge = 0
        self.charge = 0
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

        self.time = 0
        self.e_percent = 0

    def init_game(self, data_mode):
        """
        游戏数据初始化
        """

        self.my_plane.reset()

        # 清空敌机里现有的飞机
        self.enemies.empty()
        self.small_enemies.empty()
        self.mid_enemies.empty()
        self.big_enemies.empty()

        # 增加飞机数量，顺序：小、中、大
        self.increase_enemies(15, 6, 2)

        self.score = 0
        self.charge = 0

        # 游戏主音乐加载
        pygame.mixer.music.load("./sound/bgm.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause()

        # 全屏炸弹
        self.bomb_num = data_mode["BombNum"]

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
        volume_control = VolumeControlBase("音量", const.WINDOW_HEIGHT // 3)
        sound_control = VolumeControlBase("音效", const.WINDOW_HEIGHT // 3 + 60)

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
                            if self.my_plane.cur_blood <= 0:
                                if again_rect.collidepoint(event.pos):
                                    self.init_game(data[mode])
                                    self.status = const.Status.PLAY
                                elif exit_rect.collidepoint(event.pos):
                                    pygame.base.quit()
                                    sys.exit()

                        elif self.status == const.Status.PAUSE:
                            # 设置音量
                            if volume_control.check(event.pos):
                                pygame.mixer.music.set_volume(
                                    volume_control.get_volume())

                            # 设置音效
                            if sound_control.check(event.pos):
                                snd = sound_control.get_volume()
                                self.my_plane.set_music_volume(snd)
                                for enemy in self.enemies:
                                    enemy.set_music_volume(snd)

                                for i in sound_list:
                                    i.set_volume(snd)

                        elif self.status == const.Status.LOGIN:
                            self.login_box.check_event(event)

                    # 定义超级炸弹的伤害
                    case pygame.constants.KEYDOWN:
                        if self.status == const.Status.PLAY:
                            key = pygame.key.name(event.key)
                            if key == "space" and self.bomb_num:
                                count = 0
                                self.bomb_num -= 1
                                bomb_sound.play()
                                for each in self.enemies:
                                    if each.rect.bottom > \
                                            const.WINDOW_HEIGHT // 3:
                                        each.blood -= 20*7
                                        if each.blood <= 0:
                                            count += 1
                                count = min(10, count)
                                self.my_plane.cur_blood += \
                                    self.my_plane.BLOOD * count / 250
                                self.my_plane.cur_blood = min(
                                    self.my_plane.cur_blood,
                                    self.my_plane.BLOOD)

                            elif key == "e":
                                if self.e_percent == 100:
                                    self.e_percent = 0

                                    self.time = time.time()
                                    skill_e_sound.play()
                                    add = random.choice([10, 16, 22])
                                    self.charge = min(100, self.charge + add)
                                    self.my_plane.cur_blood *= 0.7
                                    pygame.time.set_timer(
                                        self.add_bullet_damage_event, 7 * 1000)
                                    const.Player.DAMAGE *= 4

                            elif key == "f" and self.charge > 35:
                                self.charge -= 35
                                for enemy in self.enemies:
                                    if enemy.rect.bottom > 0:
                                        enemy.move_center()

                            elif key == "q":
                                if not self.super_bullet and \
                                        self.charge == 100:
                                    self.super_bullet = True
                                    skill_q_sound.play()
                                    self.charge = 0
                                    pygame.time.set_timer(
                                        self.super_bullet_event, 14 * 1000)

                        elif self.status == const.Status.LOGIN:
                            if event.key in [
                                    pygame.constants.K_RETURN,
                                    pygame.constants.K_KP_ENTER]:
                                self.account = self.login_box.check_enter()
                                login_title.set_text(
                                    f"Welcome,{self.account} !")
                                self.loggedin = True
                                self.status = const.Status.PLAY
                                self.current_pause_image = self.pause_images[0]
                                self.time = time.time()
                            self.login_box.check_event(event)

                    case self.super_bullet_event:
                        self.super_bullet = False
                        pygame.time.set_timer(self.super_bullet_event, 0)
                    case self.add_bullet_damage_event:
                        const.Player.DAMAGE //= 4
                        pygame.time.set_timer(self.add_bullet_damage_event, 0)

            match self.status:
                case const.Status.PLAY:
                    # 播放音乐
                    if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.unpause()

                    screen.blit(self.current_pause_image, self.pause_rect)

                    # 分数信息
                    show_score(self.score)

                    if self.my_plane.cur_blood > 0:
                        self.my_plane.move()

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
                            add_score = \
                                each.draw(self.switch_image, delay)
                            if add_score:
                                self.score += add_score
                                r = random.random()
                                if r < 0.3:
                                    self.bomb_num += 1
                                elif r < 0.4:
                                    self.charge = min(100, self.charge + 10)

                        # 绘制中型敌机：
                        for each in self.mid_enemies:
                            self.score += each.draw(self.switch_image, delay)

                        # 绘制小型敌机：
                        for each in self.small_enemies:
                            self.score += each.draw(self.switch_image, delay)

                        # 绘制我方战机：
                        self.my_plane.check_active(
                            self.switch_image, self.enemies)

                        # 显示当前炸弹数量
                        show_bomb_info(self.bomb_num)

                        # 绘制剩余血量数值
                        show_blood_num(
                            self.my_plane.cur_blood, self.my_plane.BLOOD)

                        self.e_percent = int(
                            (time.time() - self.time) /
                            const.Player.E_LOAD_TIME * 100)
                        self.e_percent = min(self.e_percent, 100)

                        load_charge = int(
                            (self.charge - self.old_charge) *
                            (time.time() - self.time) /
                            const.Player.Q_SHOW_ANI_TIME + self.old_charge)

                        show_small_skill_charge(self.e_percent)
                        show_final_charge(load_charge)
                        if load_charge >= self.charge:
                            self.old_charge = self.charge
                    else:
                        # 背景音乐停止
                        pygame.mixer.music.fadeout(500)
                        # 停止全部音效
                        pygame.mixer.fadeout(500)

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

            pygame.mixer.music.pause()
            pygame.mixer.pause()
        else:
            self.current_pause_image = self.pause_images[1]

            pygame.mixer.music.unpause()
            pygame.mixer.unpause()


if __name__ == "__main__":
    m = Main()
    m.main()
