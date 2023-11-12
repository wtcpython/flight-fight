"""
    显示屏幕元素
"""
# pylint: disable=c-extension-no-member
# pylint: disable=no-name-in-module
import pygame

import const
from plane_utils import screen, load_img
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
        f"Score: {score}", const.Color.WHITE,
        (const.WINDOW_WIDTH // 2, const.WINDOW_FRAME_WIDTH * 3))
    screen.blit(render_score.get_surface(), render_score.get_rect())


def show_bomb_info(bomb_num: int):
    """
    显示当前炸弹数量
    """
    screen.blit(bomb_img, (
        const.WINDOW_FRAME_WIDTH,
        const.WINDOW_HEIGHT - const.WINDOW_FRAME_WIDTH - bomb_rect.height))

    bomb_num_render = TextRect(
        f"X {bomb_num}", const.Color.WHITE, (0, 0))
    rect = bomb_num_render.get_rect()
    screen.blit(
        bomb_num_render.get_surface(), (
            bomb_rect.width + 10,
            const.WINDOW_HEIGHT - const.WINDOW_FRAME_WIDTH - rect.height))


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
                    const.Color.BLACK, (0, 0))
    text.render_text()
    rect = text.render.get_rect()
    rect.left, rect.top = (
        const.WINDOW_WIDTH - rect.width, const.WINDOW_HEIGHT - rect.height)
    screen.blit(text.render, rect)


def show_small_skill_charge(percent: int):
    """
    显示E技能剩余时间
    """
    radius = 50

    center_pos = (
        const.WINDOW_WIDTH - radius - 10,
        const.WINDOW_HEIGHT - radius * 4 - 10)

    text = TextRect("E", const.Color.BLACK, center_pos, 20)
    rect = (const.WINDOW_WIDTH - radius * 2 - 10,
            const.WINDOW_HEIGHT - radius * 5 - 10,
            radius * 2, radius * 2)

    pygame.draw.arc(screen, const.Color.BLACK, rect,
                    0, 3.14 * 2, 1)

    pygame.draw.arc(screen, const.Color.RED, rect,
                    0, 3.14 * percent / 50, 2)

    screen.blit(text.get_surface(), text.get_rect())


def show_final_charge(load_charge: int):
    """
    显示充能
    """
    radius = 50

    center_pos = (
        const.WINDOW_WIDTH - radius - 10,
        const.WINDOW_HEIGHT - radius * 2)

    text = TextRect("Q", const.Color.BLACK, center_pos, 20)
    rect = (const.WINDOW_WIDTH - radius * 2 - 10,
            const.WINDOW_HEIGHT - radius * 3,
            radius * 2, radius * 2)

    pygame.draw.arc(screen, const.Color.BLACK, rect,
                    0, 3.14 * 2, 1)

    pygame.draw.arc(screen, const.Color.RED, rect,
                    0, 3.14 * load_charge / 50, 2)

    screen.blit(text.get_surface(), text.get_rect())
