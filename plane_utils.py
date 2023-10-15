"""
    定义一些接口函数
"""
# pylint: disable=c-extension-no-member
import json
import pygame

import const

pygame.base.init()

screen = pygame.display.set_mode((const.WINDOW_WIDTH, const.WINDOW_HEIGHT))


def load_img(path: str) -> pygame.surface.Surface:
    """
    加载图片
    """
    return pygame.image.load(path).convert_alpha()


def read_json(path: str) -> dict:
    """
    读取json文件内容
    """
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


def write_json(path: str, data: dict) -> None:
    """
    写入json文件
    """
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def load_music(path: str) -> pygame.mixer.Sound:
    """
    加载音乐
    """
    return pygame.mixer.Sound(path)


def render_text(content: str, color: tuple) -> pygame.surface.Surface:
    """
    渲染文本
    """
    font = pygame.font.Font("./msyhbd.ttc", 32)
    render = font.render(content, True, color)
    return render
