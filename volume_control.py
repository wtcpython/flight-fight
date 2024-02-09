"""
    音量控制类
"""
import pygame

import const
from utils import screen
from text_rect import TextRect


class VolumeControlBase():
    """
    音量控制基类，居中显示
    """
    def __init__(self, content: str, top):
        # 默认音量为 20%
        self.value = 0.2

        self.volume_text = TextRect(content, pygame.Color("White"), (0, 0))
        self.volume_rect = self.volume_text.get_rect()

        self.volume_frame = pygame.Rect(0, 0, 301, self.volume_rect.height)

        self.volume_full = pygame.Rect(
            0, 0, self.value * 300, self.volume_rect.height)

        self.percent_show = TextRect(
            f"{int(self.value * 100)}", pygame.Color("White"), (0, 0))
        self.percent_show_rect = self.percent_show.get_rect()

        self.width = (
            self.volume_rect.width +
            self.volume_frame.width +
            self.percent_show_rect.width)

        self.volume_rect.left, self.volume_rect.top = (
            (const.Window.Width - self.width) // 2, top)
        self.volume_frame.left, self.volume_frame.top = (
            self.volume_rect.right + 10, self.volume_rect.top)
        self.volume_full.left, self.volume_full.top = (
            self.volume_rect.right + 10, self.volume_rect.top)
        self.percent_show_rect.left, self.percent_show_rect.top = (
            self.volume_frame.right + 10, self.volume_rect.top)

    def set_volume(self):
        """
        设置当前音量
        """
        self.volume_full = pygame.Rect(
            self.volume_rect.right + 10, self.volume_rect.top,
            self.value * 300, self.volume_rect.height)

        self.percent_show.set_text(f"{int(self.value * 100)}")

    def get_volume(self) -> float:
        """
        获取当前音量
        """
        return self.value

    def draw(self):
        """
        绘制音量控制
        """
        pygame.draw.rect(screen, (255, 0, 0), self.volume_frame, 2, 15)
        pygame.draw.rect(screen, (255, 0, 0), self.volume_full, 0, 15)
        self.volume_text.blit((self.volume_rect.left, self.volume_rect.top))
        self.percent_show.blit((self.percent_show_rect.left, self.percent_show_rect.top))

    def check(self, pos) -> bool:
        """
        检查鼠标点击状态
        """
        if self.volume_frame.collidepoint(pos):
            self.value = (pos[0] - self.volume_frame.left) / 300
            self.set_volume()
            return True
        return False
