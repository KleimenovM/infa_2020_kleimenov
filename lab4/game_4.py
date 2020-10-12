import pygame
from pygame.draw import *
from random import *


def pythagorean(x, y):
    length = (x**2 + y**2)**0.5
    return round(length)


def define_vel(dim):
    velocity = randint(dim // 200, dim // 35) * (-1)**randint(1, 2)
    return velocity


def create_square(screen):
    length, height = screen.get_size()
    diagonal = pythagorean(length, height)
    size = randint(diagonal//50, diagonal//10)
    x = randint(0 + size, length - size)
    y = randint(0 + size, height - size)
    vel_x = define_vel(length)
    vel_y = define_vel(height)

    color = [randint(200, 255), 0, 0]

    rect(screen, color, (x, y, size, size))
    return x, y, size, vel_x, vel_y, color


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

    return [x, y, r, vel_x, vel_y, color]


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


def square_shift(screen, square_params):
    x, y, size, vel_x, vel_y, color = square_params
    s_x, s_y = screen.get_size()
    if x - size <= 0 or x + size >= s_x:
        vel_x = int(-random() * randint(1, 3) * vel_x)
    if y - size <= 0 or y + size >= s_y:
        vel_y = int(-random() * randint(1, 3) * vel_y)

    if random() > 0.37:
        vel_x = vel_x + randint(-5, 5)
        vel_y = vel_y + randint(-5, 5)

    if x < 0 or x > s_x:
        x = s_x // 2
    if y < 0 or y > s_y:
        y = s_y // 2

    square_params = x + vel_x, y + vel_y, size, vel_x, vel_y, color

    rect(screen, color, (x, y, size, size))
    return square_params


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
    b_q = int(input('Сколько шаров? '))
    s_q = int(input('А квадратов? '))

    pygame.init()

    fps = 24
    screen = pygame.display.set_mode((1200, 750))

    pygame.display.update()
    clock = pygame.time.Clock()
    finished = False
    counter = 0
    print(counter)
    ball_params = [create_ball(screen) for i in range(b_q)]
    square_params = [create_square(screen) for i in range(s_q)]

    while not finished:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for s in range(len(ball_params)):
                    prev_counter = counter
                    counter += click(event, ball_params[s])
                    if counter != prev_counter:
                        print(counter)

        for i in range(len(ball_params)):
            ball_params[i] = ball_shift(screen, ball_params[i])
        for j in range(len(square_params)):
            square_params[j] = square_shift(screen, square_params[j])
        pygame.display.update()
        screen.fill((255, 255, 255))

    pygame.quit()
    return


main()
