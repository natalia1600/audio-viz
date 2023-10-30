import pygame
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
from log import setup_logger

logger = setup_logger("gui ")

COLOR_BG = (28, 28, 28)
NUM_BARS = 120
COLORS = ["#FFCC99", "#FFDAB9", "#77DD77",
          "#FDFD96", "#99CCFF", "#77B5FE", "#FFEB3B"]


class Visualizer:
    def __init__(self, screen_width=1280, screen_height=720):
        self.screen_width = screen_width
        self.screen_height = screen_height

        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        # save previous wave heights for smoothing
        self.prev_ys = np.full(
            shape=NUM_BARS,
            fill_value=screen_height // 4,
            dtype=np.int64
        )

        self.max_amplitude = 0

    def should_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                return True
        return False

    def quit(self):
        pygame.quit()

    def draw_bar(self, x, y, width, height):
        # colormap = plt.cm.get_cmap('cubehelix')
        colormap = plt.cm.tab20b
        print('colormap', colormap)
        color = colormap(height / (self.screen_height / 2))
        rgb = mcolors.to_rgb(color)
        pygame_color = tuple(int(round(c * 255)) for c in rgb)
        # convert color to RGB
        print(pygame_color)
        pygame.draw.rect(self.screen, pygame_color, pygame.Rect(
            x, y - height, width, height), border_radius=width//2)

    def draw_bars(self, xs, ys):
        print("xs ", xs[:20])
        print("ys", ys[:20])
        print(xs)
        print(ys)
        num_points = xs.size
        xs = np.arange(NUM_BARS)
        # num xs points per NUM_BARS
        step = num_points // NUM_BARS

        # size of each bar according to screen width
        bar_width = (self.screen_width // NUM_BARS) * 2

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

        # Set ys to ys point at step intervals
        # xs = np.logspace(0, np.log10(self.screen_width), NUM_BARS)

        EXTRA_SPACE = NUM_BARS // 20
        y_logspace = np.logspace(0, np.log10(
            len(ys)), num=NUM_BARS + EXTRA_SPACE)
        y_logspace = y_logspace[EXTRA_SPACE //
                                2: len(y_logspace) - (EXTRA_SPACE // 2)][:NUM_BARS]
        indices = np.floor(y_logspace).astype(int)
        y_exp = np.arange(0, NUM_BARS) ** 1.5

        # Make sure indices are within the range of ys_samples
        indices = np.clip(indices, 0, len(ys) - 1)
        ys_samples = ys[indices]

        print(ys_samples, 'ys_samples1')

        ys_samples = ys_samples * y_exp

        print(ys_samples, 'ys_samples * y_exp')
        print(ys_samples, 'ys_samples_logged')
        print(indices, 'indices')
        print("ys_samples_logged", ys_samples)
        print("ys_samples_logged size:", len(ys_samples))

        # set xs to NUM_BARS evenly spaced points accross the screen
        xs = np.arange(0, self.screen_width, self.screen_width // NUM_BARS)
        # set max_amplitude to the larger value between curr max_amplitude
        # and the max amplitude of ys
        self.max_amplitude = max(self.max_amplitude, np.max(ys_samples))

        # calculates scale factor to ensure the y-values will fit
        # within the screen height
        # add 1 to max amplitude to avoid zero division
        # Leave room for edges of screen by scaling (max_amplitude + 1) by 1.5
        scale_factor = (self.screen_height * 0.5) / (self.max_amplitude + 1)

        # scales the values in the ys_samples array by a factor of scale_factor
        ys_samples_scaled = ys_samples * scale_factor

        # maybe num is num_bars?
        values = np.logspace(0, np.log10(scale_factor), num=num_points)

        # print("xs", xs)
        print("xs size", len(xs))

        # print("ys_samples_scaled", ys_samples_scaled)
        print("ys_samples_scaled size", len(ys_samples_scaled))

        # print("values", values)
        print("values size", len(values))

        ys_smoothed = np.average(
            np.vstack((ys_samples_scaled, self.prev_ys)), axis=0, weights=[0.5, 0.5])

        self.prev_ys = ys_smoothed

        xs = xs[4::4]
        ys_smoothed = ys_smoothed[4::4]

        for x, y in zip(xs, ys_smoothed):
            self.draw_bar(x + (bar_width / 2), (self.screen_height // 2) + y,
                          bar_width, y * 2)

    def update(self, xs, ys):
        logger.info("Creating new frame")

        # Set background
        self.screen.fill('BLACK')

        # Window contents
        self.draw_bars(xs, ys)

        # Commit changes
        logger.info("Committing new frame")
        pygame.display.flip()
