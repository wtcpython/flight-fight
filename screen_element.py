"""
    显示屏幕元素
"""
# pylint: disable=c-extension-no-member
# pylint: disable=no-name-in-module

import const
from plane_utils import screen, render_text, load_img

life_img = load_img("./images/life.png")
life_rect = life_img.get_rect()

bomb_img = load_img("./images/bomb.png")
bomb_rect = bomb_img.get_rect()


def show_score(score: int):
    """
    显示当前分数
    """
    render_score = render_text(f"Score: {score}", (255, 255, 255))
    rect = render_score.get_rect()
    rect.left, rect.top = (
        (const.WINDOW_WIDTH - rect.width) // 2,
        const.WINDOW_FRAME_WIDTH)
    screen.blit(render_score, rect)


def show_bomb_info(bomb_num: int):
    """
    显示当前炸弹数量
    """
    # 全屏炸弹

    screen.blit(bomb_img, (
        const.WINDOW_FRAME_WIDTH,
        const.WINDOW_HEIGHT - const.WINDOW_FRAME_WIDTH - bomb_rect.height))

    bomb_num_render = render_text(f"X {bomb_num}", (255, 255, 255))
    rect = bomb_num_render.get_rect()
    screen.blit(
        bomb_num_render, (
            bomb_rect.width + 10,
            const.WINDOW_HEIGHT - const.WINDOW_FRAME_WIDTH - rect.height))


def show_life_num_info(life_num: int):
    """
    显示当前生命数量
    """
    for i in range(life_num):
        screen.blit(life_img, (
            const.WINDOW_WIDTH-10-(i % 5 + 1)*life_rect.width,
            const.WINDOW_HEIGHT - 10 - life_rect.height * (i // 5 + 1)))
