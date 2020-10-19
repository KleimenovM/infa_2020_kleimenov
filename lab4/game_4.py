import pygame
from pygame.draw import *
from random import *


def pythagorean(x, y):
    """

    :param x:
    :param y:
    :return:
    """
    length = (x**2 + y**2)**0.5
    return round(length)


def define_vel(dim):
    """

    :param dim:
    :return:
    """
    velocity = randint(dim // 200, dim // 35) * (-1)**randint(1, 2)
    return velocity


def create_square(screen):
    """

    :param screen:
    :return:
    """
    length, height = screen.get_size()
    diagonal = pythagorean(length, height)
    size = randint(diagonal//50, diagonal//20)
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
    """

    :param screen:
    :param ball_params:
    :return:
    """
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
    """

    :param screen:
    :param square_params:
    :return:
    """
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


def click_square(event, square_params):
    """

    :param event:
    :param square_params:
    :return:
    """
    s_x, s_y, size, vel_x, vel_y, color = square_params
    x, y = event.pos
    if s_x - size <= x <= s_x + size and s_y - size <= y <= s_y + size:
        return 5
    else:
        return 0


def work_with_data(data):
    """

    :param data:
    :return:
    """
    all_participants = []

    next_lev = []
    for part in data:
        if part.strip()[:2] == '- ':
            if len(next_lev) != 0:
                all_participants.append(next_lev)
            next_lev = [len(all_participants) + 1]
        else:
            part = part.strip().split(': ')
            next_lev.append([part[0], int(part[1])])
    all_participants.append(next_lev)

    return all_participants


def organize_data(level):
    """

    :param level:
    :return:
    """
    writing_data = ['- level ' + str(level[0]) + ' -']
    level.remove(level[0])
    level.sort(key=lambda i: i[1], reverse=1)
    if len(level) > 4:
        for i in range(len(level)):
            level.remove(level[len(level) - 1 - i])
    level.insert(0, writing_data)
    return level


def write_data(name, counter, level):
    """

    :param name:
    :param counter:
    :param level:
    :return:
    """
    x = open('rating.txt', 'r')
    data = x.readlines()
    x.close()

    data.remove(data[0])  # cross out info-line
    data = work_with_data(data)

    data[level-1].append([name, counter])

    x = open('rating.txt', 'w')
    x.write('# --- Rating file ---' + '\n')

    for level in data:
        level = organize_data(level)
        for j in level:
            if len(j) == 1:
                x.write(j[0] + '\n')
            else:
                x.write(j[0] + ': ' + str(j[1]) + '\n')

    x.close()

    pass


def show_time_and_count(screen, time, ticks, counter):
    """

    :param screen:
    :param time:
    :param ticks:
    :param counter:
    :return:
    """
    counter_font = pygame.font.Font(None, 70)
    counter_text = counter_font.render(str(counter), 1, (0, 0, 0))
    place = counter_text.get_rect(center=(round(screen.get_width()*0.015), 20))
    screen.blit(counter_text, place)

    time_font = pygame.font.Font(None, 70)
    time_what = str((time - ticks)//1000) + ':' + str((time - ticks) % 1000)
    time_text = time_font.render(time_what, 1, (0, 0, 0))
    place = time_text.get_rect(center=(round(screen.get_width()*0.95), 20))
    screen.blit(time_text, place)
    pass


def last_text(screen, counter):
    """

    :param screen:
    :param counter:
    :return:
    """
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 100)
    text = font.render('Game over. Your score is ' + str(counter), 1, (0, 0, 0))
    place = text.get_rect(center=(round(screen.get_width() * 0.5), round(screen.get_height() * 0.5)))
    screen.blit(text, place)
    pygame.display.update()
    pygame.time.delay(1500)
    pass


def game(fps, screen, b_q, s_q):
    """

    :param fps:
    :param screen:
    :param b_q:
    :param s_q:
    :return:
    """
    pygame.display.update()
    clock = pygame.time.Clock()
    finished = False
    counter = 0
    ball_params = [create_ball(screen) for i in range(b_q)]
    square_params = [create_square(screen) for i in range(s_q)]

    time = 10 * 1000

    while not finished:
        clock.tick(fps)
        show_time_and_count(screen, time, pygame.time.get_ticks(), counter)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for s in range(len(ball_params)):
                    add = click(event, ball_params[s])
                    counter += add
                    time += 100 * add
                for o in range(len(square_params)):
                    add = click_square(event, square_params[o])
                    counter += add
                    time += 100 * add

        for p in range(len(ball_params)):
            ball_params[p] = ball_shift(screen, ball_params[p])
        for j in range(len(square_params)):
            square_params[j] = square_shift(screen, square_params[j])
        pygame.display.update()
        screen.fill((255, 255, 255))
        if pygame.time.get_ticks() > time:
            finished = True

    clock.tick(fps)
    last_text(screen, counter)

    return counter


def main():
    name = input('Enter your name: ')
    level = int(input('Level (5 - the hardest, 1 - the easiest): '))
    if level > 5:
        level = 5
    elif level < 1:
        level = 1
    b_q = (6 - level) * 3
    s_q = (6 - level)

    pygame.init()

    fps = 24
    screen = pygame.display.set_mode((1200, 800))

    counter = game(fps, screen, b_q, s_q)

    write_data(name, counter, level)

    print(name + ', your result: ' + str(counter) + '\n')

    pygame.quit()
    return


main()
