import pygame
from pygame.draw import *
from random import randint

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def pythagorean(x, y):
    length = (x**2 + y**2)**0.5
    return round(length)


def new_ball(screen):
    """
    Creates a new ball on screen
    :param screen: surface where a ball will be drawn
    :return: ball_parameters - center x, y, radius, color
    """

    length, height = screen.get_size()
    diagonal = pythagorean(length, height)

    x = randint(0 + length // 10, length - length // 10)
    y = randint(0 + height // 10, height - height // 10)
    r = randint(diagonal // 100, diagonal // 10)

    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)

    return x, y, r, color


def click(event, ball_xyr):
    """
    Processes clicks of a mouse
    :param event:
    :param ball_xyr:
    :return:
        1 if click was inside the ball
        0 if click was out of the ball
    """
    b_x, b_y, b_r, b_c = ball_xyr
    x, y = event.pos
    if pythagorean(x - b_x, y - b_y) > b_r:
        return 0
    else:
        return 1


def main():
    pygame.init()

    fps = 2
    screen = pygame.display.set_mode((800, 600))

    pygame.display.update()
    clock = pygame.time.Clock()
    finished = False
    counter = 0  # successful clicks counter
    ball_param = (0, 0, 0, (0, 0, 0))

    while not finished:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                prev_counter = counter
                counter += click(event, ball_param)
                if counter != prev_counter:
                    print(counter)

        ball_param = new_ball(screen)
        pygame.display.update()
        screen.fill(BLACK)

    pygame.quit()
    return


main()
