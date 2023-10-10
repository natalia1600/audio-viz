import pygame
import random
import numpy as np

import state
from log import setup_logger

logger = setup_logger("gui")

COLOR_BG = (28, 28, 28)

# class Visualizer:
#     def __init__(self):
#         self.screen = TODO
#         self.max_amplitude = TODO


pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen_width, screen_height = screen.get_size()
running = True


# bottom left corner of rectangle at (x, y)
def draw_bar(x, y, width, height, color):
    pygame.draw.rect(screen, color, pygame.Rect(x, y - height, width, height))


NUM_BARS = 100


def draw_bars(xs, ys):
    num_points = xs.size
    step = num_points // NUM_BARS
    bar_width = screen_width // NUM_BARS
    logger.info(f"Number of points provided to draw bars {num_points}")

    # start = math.log(1, 10)
    # stop = math.log(24000, 10)
    # ys_to_sample = np.logspace(start, stop, num=NUM_BARS)

    # print("ys_to sample", ys_to_sample)

    # ys_logspace = []
    # print("ys shape", ys.shape)
    # print("xs shape", xs.shape)
    # for i in ys_to_sample:
    #     ys_logspace.append(ys[int(i)])

    # print(len(ys_logspace))
    # print(ys_logspace)
    # exit(1)

    # VALID NO TOUCH
    ys_samples = ys[::step]
    xs = np.arange(0, screen_width, screen_width // NUM_BARS)

    state.max_amplitude = max(state.max_amplitude, np.max(ys_samples))
    scale_factor = screen_height / state.max_amplitude
    ys_samples_scaled = ys_samples * scale_factor

    for x, y in zip(xs, ys_samples_scaled):
        color = get_random_color()
        draw_bar(x, screen_height // 2, bar_width, y, color)


def get_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)


def draw_frame(xs, ys):
    logger.info("Creating new frame")

    # Set background
    screen.fill(COLOR_BG)

    # Window contents
    draw_bars(xs, ys)

    # Commit changes
    logger.info("Committing new frame")
    pygame.display.flip()
