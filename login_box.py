"""
    输入框文件
"""
# pylint: disable=c-extension-no-member
# pylint: disable=no-name-in-module

from pathlib import Path
from shutil import copyfile

import pygame

from plane_utils import screen, render_text

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')


class LoginBox():
    """
    输入框
    """
    def __init__(self):
        self.tip_text = render_text("输入你的ID:", (255, 255, 255))
        self.tip_rect = self.tip_text.get_rect()

        self.login_box = pygame.Rect(0, 0, 200, self.tip_rect.height)

        self.current_color = COLOR_INACTIVE
        self.text = ""
        self.render_text = render_text(self.text, self.current_color)

        self.active = False
        self.account = None

    def set_pos(self, left: int, top: int):
        """
        设置控件位置
        """
        self.tip_rect.left, self.tip_rect.top = left, top
        self.login_box.left, self.login_box.top = self.tip_rect.right + 10, top

    def width(self) -> int:
        """
        获取输入框的宽度
        """
        return self.tip_rect.width + self.login_box.width

    def height(self) -> int:
        """
        获取输入框的高度
        """
        return self.tip_rect.height

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
        else:
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
        self.render_text = render_text(self.text.strip(), self.current_color)

    def update(self):
        """
        更新
        """
        self.login_box.width = max(200, self.render_text.get_width()+10)

    def draw(self):
        """
        绘制
        """
        screen.blit(self.tip_text, self.tip_rect)
        screen.blit(self.render_text,
                    (self.login_box.x+2, self.login_box.y+2))
        pygame.draw.rect(screen, self.current_color,
                         self.login_box, 2, border_radius=10)
