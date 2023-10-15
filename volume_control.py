"""
    音量控制类
"""
import pygame

from plane_utils import screen, render_text


class VolumeControlBase():
    """
    音量控制基类
    """
    def __init__(self, content: str, volume, left, top):
        self.volume_text = render_text(content, (255, 255, 255))
        self.volume_rect = self.volume_text.get_rect()
        self.volume_rect.left, self.volume_rect.top = left, top

        self.volume_frame = pygame.Rect(
            0 + self.volume_rect.width + 10,
            self.volume_rect.top,
            301, self.volume_rect.height)

        self.volume_full = pygame.Rect(
            0 + self.volume_rect.width + 10,
            self.volume_rect.top,
            volume * 300, self.volume_rect.height)

        self.percent_show = render_text(
            f"{int(volume * 100)}", (255, 255, 255))
        self.percent_show_rect = self.percent_show.get_rect()
        self.percent_show_rect.left, self.percent_show_rect.top = (
            0 + self.volume_rect.width + 320,
            self.volume_rect.top)

    def set_volume(self, volume):
        """
        设置当前音量
        """
        self.volume_full = pygame.Rect(
            0 + self.volume_rect.width + 10,
            self.volume_rect.top,
            volume * 300, self.volume_rect.height)

        self.percent_show = render_text(
            f"{int(volume * 100)}", (255, 255, 255))

    def draw(self):
        """
        绘制音量控制
        """
        pygame.draw.rect(screen, (255, 0, 0), self.volume_frame, 2, 15)
        pygame.draw.rect(screen, (255, 0, 0), self.volume_full, 0, 15)
        screen.blit(self.volume_text, self.volume_rect)
        screen.blit(self.percent_show, self.percent_show_rect)

    def check(self, pos) -> bool:
        """
        检查鼠标点击状态
        """
        if self.volume_frame.collidepoint(pos):
            vol = (pos[0] - (0 + self.volume_rect.width + 10)) / 300
            self.set_volume(vol)
            return True
        return False
