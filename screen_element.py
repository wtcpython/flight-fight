"""
    显示屏幕元素
"""
# pylint: disable=c-extension-no-member
# pylint: disable=no-name-in-module
import pygame

import const
from utils import screen, load_img
from text_rect import TextRect

life_img = load_img("./images/life.png")
life_rect = life_img.get_rect()

bomb_img = load_img("./images/bomb.png")
bomb_rect = bomb_img.get_rect()


def show_score(score: int):
    """
    显示当前分数
    """
    render_score = TextRect(
        f"Score: {score}", pygame.Color("White"),
        (const.Window.Width // 2, const.Window.Margin * 3))
    render_score.blit()


def show_bomb_info(bomb_num: int):
    """
    显示当前炸弹数量
    """
    screen.blit(bomb_img, (
        const.Window.Margin,
        const.Window.Height - const.Window.Margin - bomb_rect.height))

    bomb_num_render = TextRect(
        f"X {bomb_num}", pygame.Color("White"), (0, 0))
    rect = bomb_num_render.get_rect()
    bomb_num_render.blit((
        bomb_rect.width + 10,
        const.Window.Height - const.Window.Margin - rect.height))


def draw_blood_line(rect: pygame.Rect, offset: int, percent: float):
    """
    绘制血条
    """
    pygame.draw.line(
        screen, (0, 0, 0), (rect.left, rect.top + offset),
        (rect.right, rect.top + offset), 2)

    pygame.draw.line(
        screen, (0, 255, 0), (rect.left, rect.top + offset),
        (rect.left + rect.width * percent, rect.top + offset), 2)


def show_blood_num(blood: float, const_blood: float):
    """
    显示血量数值
    """
    text = TextRect(f"{round(blood, 2)} / {const_blood}",
                    pygame.Color("Black"), (0, 0), 16)
    rect = text.get_rect()
    rect.left, rect.top = (
        const.Window.Width - rect.width - const.Window.Margin,
        const.Window.Height - rect.height - const.Window.Margin)
    screen.blit(text.render, rect)


def show_small_skill_charge(percent: int):
    """
    显示E技能剩余时间
    """
    radius = 50

    center_pos = (
        const.Window.Width - radius - 10,
        const.Window.Height - radius * 4 - 10)

    text = TextRect("E", pygame.Color("Black"), center_pos, 20)
    rect = (const.Window.Width - radius * 2 - 10,
            const.Window.Height - radius * 5 - 10,
            radius * 2, radius * 2)

    pygame.draw.arc(screen, pygame.Color("Black"), rect,
                    0, 3.14 * 2, 1)

    pygame.draw.arc(screen, pygame.Color("Red"), rect,
                    0, 3.14 * percent / 50, 2)

    text.blit()


def show_final_charge(load_charge: int):
    """
    显示充能
    """
    radius = 50

    center_pos = (
        const.Window.Width - radius - 10,
        const.Window.Height - radius * 2)

    text = TextRect("Q", pygame.Color("Black"), center_pos, 20)
    rect = (const.Window.Width - radius * 2 - 10,
            const.Window.Height - radius * 3,
            radius * 2, radius * 2)

    pygame.draw.arc(screen, pygame.Color("Black"), rect,
                    0, 3.14 * 2, 1)

    pygame.draw.arc(screen, pygame.Color("Red"), rect,
                    0, 3.14 * load_charge / 50, 2)

    text.blit()
