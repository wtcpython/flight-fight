"""
    用于文本显示模块
"""
# pylint: disable=c-extension-no-member
import pygame

from utils import screen

class TextRect:
    """
    Pygame 文本显示
    """
    def __init__(self, text: str,
                 color: pygame.Color = pygame.Color("White"),
                 center_postition: tuple[int, int] = (0, 0),
                 font_size: int = 32):
        self.font = pygame.font.Font("./msyhbd.ttc", font_size)
        self.text = text
        self.color = color

        self.center_position = center_postition
        self.__rect = self.get_rect()
        self.pos = self.__rect.topleft

        self.font_size = font_size

        self.render = None

    def set_text(self, text: str):
        """
        设置文本内容
        """
        self.text = text

    def set_color(self, color: pygame.Color):
        """
        设置文本颜色
        """
        self.color = color

    def get_rect(self) -> pygame.rect.Rect:
        """
        返回 pygame.rect.Rect 用于绘制
        """
        self.render = self.font.render(self.text, True, self.color)
        return self.render.get_rect(center=self.center_position)

    def blit(self, pos: tuple[int, int] = ()):
        """
        绘制文本
        """
        if pos == ():
            pos = self.pos
        screen.blit(self.font.render(self.text, True, self.color), pos)
