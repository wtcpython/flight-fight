"""
    用于文本显示模块
"""
# pylint: disable=c-extension-no-member
import pygame

import const

font = pygame.font.Font("./msyhbd.ttc", 32)


class TextRect:
    """
    Pygame 文本显示
    """
    def __init__(self, text: str, color: const.Color | pygame.Color,
                 center_postition: tuple[int, int]):
        self.text = text
        self.color = color

        self.center_position = center_postition

        self.render = None

    def set_text(self, text: str):
        """
        设置文本内容
        """
        self.text = text

    def set_color(self, color: const.Color | pygame.Color):
        """
        设置文本颜色
        """
        self.color = color

    def render_text(self):
        """
        字体渲染
        """
        self.render = font.render(self.text, True, self.color)

    def get_surface(self) -> pygame.surface.Surface:
        """
        转换为 pygame.surface.Surface 用于绘制
        """
        self.render_text()
        return self.render

    def get_rect(self) -> pygame.rect.Rect:
        """
        返回 pygame.rect.Rect 用于绘制
        """
        self.render_text()
        return self.render.get_rect(center=self.center_position)
