import pygame
from pygame.draw import *
from random import *

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


def define_vel(dim):
    velocity = randint(dim // 200, dim // 35) * (-1)**randint(1, 2)
    return velocity


def create_ball(screen):
    """
    Creates a new ball on screen
    :param screen: surface where a ball will be drawn
    :return: ball_parameters - center x, y, radius, color
    """

    length, height = screen.get_size()
    diagonal = pythagorean(length, height)

    r = randint(diagonal // 100, diagonal // 20)
    x = randint(0 + r, length - r)
    y = randint(0 + r, height - r)
    vel_x = define_vel(length)
    vel_y = define_vel(height)

    color = [randint(150, 200), randint(150, 200), randint(150, 200)]

    circle(screen, color, (x, y), r)

    return x, y, r, vel_x, vel_y, color


def ball_shift(screen, ball_params):
    x, y, rad, vel_x, vel_y, color = ball_params
    s_x, s_y = screen.get_size()
    if x - rad <= 0 or x + rad >= s_x:
        vel_x = -vel_x
    if y - rad <= 0 or y + rad >= s_y:
        vel_y = -vel_y
    ball_params = x + vel_x, y + vel_y, rad, vel_x, vel_y, color

    circle(screen, color, (x, y), rad)
    return ball_params


def click(event, ball_xyr):
    """
    Processes clicks of a mouse
    :param event:
    :param ball_xyr:
    :return:
        1 if click was inside the ball
        0 if click was out of the ball
    """
    b_x, b_y, b_r, b_vel_x, b_vel_y, color = ball_xyr
    x, y = event.pos
    if pythagorean(x - b_x, y - b_y) > b_r:
        return 0
    else:
        return 1


def main():
    ball_quantity = int(input('Сколько шаров? '))

    pygame.init()

    fps = 30
    screen = pygame.display.set_mode((800, 600))

    pygame.display.update()
    clock = pygame.time.Clock()
    finished = False
    ball_params = []
    for i in range(ball_quantity):
        ball_params.append(create_ball(screen))

    while not finished:
        clock.tick(fps)
        to_del = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for s in range(len(ball_params)):
                    if click(event, ball_params[s]) == 1:
                        to_del.append(s)
        new_params = []
        for t in range(len(ball_params)):
            if to_del.count(t) == 0:
                new_params.append(ball_shift(screen, ball_params[t]))
        ball_params = new_params
        pygame.display.update()
        screen.fill(BLACK)

        if len(ball_params) == 0:
            finished = True

    pygame.quit()
    return


main()