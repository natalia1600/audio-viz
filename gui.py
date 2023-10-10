import pygame
import random
import numpy as np

from log import setup_logger

logger = setup_logger("gui ")

COLOR_BG = (28, 28, 28)
NUM_BARS = 100


class Visualizer:
    def __init__(self, screen_width=1280, screen_height=720):
        self.screen_width = screen_width
        self.screen_height = screen_height

        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        
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


    def draw_bar(self, x, y, width, height, color):
        pygame.draw.rect(self.screen, color, pygame.Rect(x, y - height, width, height))


    def draw_bars(self, xs, ys):
        print("xs ", xs[:20])
        print("ys", ys[:20])

        num_points = xs.size
        step = num_points // NUM_BARS
        bar_width = self.screen_width // NUM_BARS
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
        xs = np.arange(0, self.screen_width, self.screen_width // NUM_BARS)

        self.max_amplitude = max(self.max_amplitude, np.max(ys_samples))
        scale_factor = self.screen_height / self.max_amplitude
        ys_samples_scaled = ys_samples * scale_factor

        for x, y in zip(xs, ys_samples_scaled):
            color = (255, 255, 255)
            self.draw_bar(x, self.screen_height // 2, bar_width, y, color)



    def update(self, xs, ys):
        logger.info("Creating new frame")

        # Set background
        self.screen.fill(COLOR_BG)

        # Window contents
        self.draw_bars(xs, ys)

        # Commit changes
        logger.info("Committing new frame")
        pygame.display.flip()
