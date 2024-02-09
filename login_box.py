"""
    输入框文件
"""
# pylint: disable=c-extension-no-member
# pylint: disable=no-name-in-module

from pathlib import Path
from shutil import copyfile

import pygame

import const
from utils import screen
from text_rect import TextRect

COLOR_ACTIVE = pygame.color.Color("#0AFFE9")
COLOR_INACTIVE = pygame.color.Color("#D2FFFA")


class LoginBox:
    """
    输入框
    """
    def __init__(self):
        self.tip_text = TextRect(
            "输入你的ID:", pygame.Color("White"), (0, 0))
        self.tip_rect = self.tip_text.get_rect()
        self.login_box = pygame.Rect(0, 0, 200, self.tip_rect.height)

        self.tip_rect.left, self.tip_rect.top = ((
            const.Window.Width - self.tip_rect.width -
            self.login_box.width) // 2,
            (const.Window.Height - self.tip_rect.height) // 3)
        self.login_box.left, self.login_box.top = (
            self.tip_rect.right + 10, self.tip_rect.top)

        self.current_color = COLOR_INACTIVE
        self.text = ""
        self.render_text = TextRect(self.text, self.current_color, (0, 0))

        self.active = False
        self.account = None

    def check_enter(self):
        """
        检查输入内容
        """
        if 6 <= len(self.text) < 16:
            if (path := Path(f'./userdata/{self.text}.json')).exists():
                self.account = self.text
                self.text = ""
                return self.account
            copyfile("./userdata/all_users.json", path)
            self.account = self.text
            self.text = ""
            return self.account

        self.text = '输入6-16个字符!'
        return None

    def check_event(self, event):
        """
        检查事件
        """
        if event.type == pygame.constants.MOUSEBUTTONDOWN:
            if self.login_box.collidepoint(event.pos):
                self.active = True
                self.current_color = COLOR_ACTIVE
            else:
                self.active = False
                self.current_color = COLOR_INACTIVE
        elif event.type == pygame.constants.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < 16 and (uni := event.unicode).isascii()\
                        and uni not in ["\\", "/", r"\r"]:
                    self.text += uni
        self.render_text.set_text(self.text.strip())
        self.render_text.set_color(self.current_color)

    def update(self):
        """
        更新
        """
        self.login_box.width = max(200, self.render_text.get_rect().width+10)

    def draw(self):
        """
        绘制
        """
        self.tip_text.blit((self.tip_rect.left, self.tip_rect.top))
        self.render_text.blit((self.login_box.x+2, self.login_box.y+2))
        pygame.draw.rect(screen, self.current_color,
                         self.login_box, 2, border_radius=10)
