import pygame
from pygame.draw import *

pygame.init()
Screen = pygame.display.set_mode((400, 400))


def draw_circle(col, cent, rad, width=0, surf=Screen):
    circle(surf, col, cent, rad, width)
    return


def draw_body():
    body_color = (255, 255, 0)
    body_center = (200, 200)
    body_radius = 100
    draw_circle(body_color, body_center, body_radius)
    return body_center


def draw_eyebrows(eyes_centers, eyes_radius):
    brows_color = (0, 0, 0)
    brows_position = [(eyes_centers[0][0] - 30, eyes_centers[0][1] - 20 - eyes_radius),
                      (eyes_centers[0][0] + 20, eyes_centers[0][1] - eyes_radius),
                      (eyes_centers[1][0] + 30, eyes_centers[0][1] - 20 - eyes_radius),
                      (eyes_centers[1][0] - 20, eyes_centers[0][1] - eyes_radius)]
    line(Screen, brows_color, brows_position[0], brows_position[1], 10)
    line(Screen, brows_color, brows_position[2], brows_position[3], 10)
    return


def draw_eyes(center):
    # define eyes actually
    horizontal_shift = 50
    vertical_shift = -25
    eyes_centers = [(center[0] - horizontal_shift, center[1] + vertical_shift),
                    (center[0] + horizontal_shift, center[1] + vertical_shift)]
    eyes_radius = 20
    eyes_color = (230, 0, 0)

    # define eye pupil
    pupil_color = (0, 0, 0)
    k = 0.45  # relation between pupil radius and eye radius
    pupil_centers = eyes_centers
    pupil_radius = int(eyes_radius * k)

    for i in range(len(eyes_centers)):
        draw_circle(eyes_color, eyes_centers[i], eyes_radius)
        draw_circle(pupil_color, pupil_centers[i], pupil_radius)

    draw_eyebrows(eyes_centers, eyes_radius)

    return


def draw_mouth(center):
    vertical_shift = -50
    width = 90
    height = 8
    color = (0, 0, 0)
    dot = (center[0] + int(width/2), center[1] + vertical_shift)
    rect(Screen, color, (400-dot[0], 400-dot[1], width, height))
    return


def main():
    # 'head'-part begins here
    fps = 30
    rect(Screen, (220, 220, 220), (0, 0, 400, 400))

    # body of the program begins here
    center = draw_body()
    draw_eyes(center)
    draw_mouth(center)

    # end of the program begins here
    pygame.display.update()
    clock = pygame.time.Clock()
    finished = False

    while not finished:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

    pygame.quit()
    return


main()
