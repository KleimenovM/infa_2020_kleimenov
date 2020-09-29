import pygame
from pygame.draw import *
import numpy as np


# - SPECIAL FUNCTIONS - SPECIAL FUNCTIONS - SPECIAL FUNCTIONS - SPECIAL FUNCTIONS -

# draw an ellipse using its center and size parameters
def draw_ellipse(screen, color, center, size):
    point = (int(center[0] - size[0]/2), int(center[1] - int(size[1]/2)))
    rectangle = [point[0], point[1], int(size[0]), int(size[1])]
    ellipse(screen, color, rectangle)
    pass


# defines coordinates of a triangle
def triangle_points(position, width, height):
    points = [(position[0], position[1] + height),
              (position[0] - int(width/2), position[1]),
              (position[0] + int(width/2), position[1])]
    return points


# returns the length of a cut AB with A -> a and B -> b
def cut_length(a, b):
    x = a[0] - b[0]
    y = a[1] - b[1]
    s = x**2 + y**2
    return s**0.5


# returns the vector of moving the point
def shift(radius, alpha):
    vx = radius * np.sin(np.radians(alpha))
    vy = radius * np.cos(np.radians(alpha))
    return int(vx), int(vy)


# - FACE - FACE - FACE - FACE - FACE - FACE - FACE - FACE - FACE -


# EYES. Are 2 light-blue colored ellipses
def draw_eyes(screen, position, face_radius, eye_color):
    pupil_color = (0, 0, 0)  # black
    eye_size = [int(0.425 * face_radius), int(0.375 * face_radius)]
    pupil_size = [int(0.125 * face_radius), int(0.1 * face_radius)]
    horizontal_shift = int(0.375 * face_radius)
    vertical_shift = int(0.25 * face_radius)
    vertical_coordinate = position[1] - vertical_shift
    centers = [(position[0] - horizontal_shift, vertical_coordinate),
               (position[0] + horizontal_shift, vertical_coordinate)]

    for center in centers:
        draw_ellipse(screen, eye_color, center, eye_size)  # one eye
        draw_ellipse(screen, pupil_color, center, pupil_size)  # one pupil

    pass


# get coordinates of a hair-triangle
def get_hair_coordinates(hair_angle, hair_quantity, position, radius):
    coordinates = []
    for i in range(int(hair_quantity/2)):
        alpha = hair_angle / 2 - i * hair_angle / hair_quantity
        ax, ay = shift(radius, alpha)
        bx, by = shift(radius, alpha - hair_angle / hair_quantity)

        x1, x4 = position[0] - ax, position[0] + ax
        x2, x5 = position[0] - bx, position[0] + bx

        y14, y25 = position[1] - ay, position[1] - by

        # here I create the third point for a triangle
        rad = (cut_length((x1, y14), (x2, y25))) * np.sin(np.pi / 3)
        cx, cy = shift(rad, alpha - hair_angle/hair_quantity / 2)
        x3, x6 = int((x1 + x2)/2 - cx), int((x4 + x5)/2 + cx)
        y36 = int((y14 + y25)/2 - cy)

        points = [(x1, y14), (x2, y25), (x3, y36), (x4, y14), (x5, y25), (x6, y36)]
        for j in points:
            coordinates.append(j)

    return coordinates


# NOSE and MOUTH are just triangles in the middle of the face
def draw_mouth_and_nose(screen, position, face_radius):
    # NOSE
    nose_width = int(0.18 * face_radius)
    nose_height = int(0.15 * face_radius)
    nose_color = (150, 75, 0)  # brown
    nose_points = triangle_points(position, nose_width, nose_height)
    polygon(screen, nose_color, nose_points)  # NOSE

    # MOUTH
    mouth_width = int(0.9 * face_radius)
    mouth_height = int(0.3 * face_radius)
    vertical_shift = int(0.3 * face_radius)
    mouth_color = (240, 50, 50)  # light red
    mouth_points = triangle_points((position[0], position[1] + vertical_shift), mouth_width, mouth_height)
    polygon(screen, mouth_color, mouth_points)  # MOUTH

    pass


# hair consists of a number of purple triangles
def draw_hair(screen, position, face_radius, hair_color):
    hair_angle = 160  # degrees
    hair_quantity = 10
    coordinates = get_hair_coordinates(hair_angle, hair_quantity, position, face_radius)
    for i in range(0, len(coordinates), 3):
        points = [coordinates[i], coordinates[i+1], coordinates[i+2]]
        polygon(screen, hair_color, points)
    pass


# face is a big skin-colored circle in the center of the picture
def draw_face(screen, position, face_radius, skin_color, eyes_color, hair_color):

    circle(screen, skin_color, position, face_radius)

    draw_eyes(screen, position, face_radius, eyes_color)

    draw_mouth_and_nose(screen, position, face_radius)

    draw_hair(screen, position, face_radius, hair_color)

    return


# - BODY - BODY - BODY - BODY - BODY - BODY - BODY - BODY - BODY -


def draw_sleeve(screen, shirt_color, shirt_radius, sleeve, shirt):
    pentagon_radius = int(shirt_radius * 0.3)
    pentagon_angle = 360 / 5
    alpha = 90  # common first point angle from vertical line
    # define first point angle from horizontal line
    if sleeve[0] > shirt[0]:
        alpha += 180

    points = []
    for i in range(5):
        x_shift, y_shift = shift(pentagon_radius, alpha + pentagon_angle * i)
        points.append((sleeve[0] + x_shift, sleeve[1] + y_shift))  # append pentagon point

    polygon(screen, shirt_color, points)
    pass


# shirt is a big orange circle under the face
def draw_shirt_and_arms(screen, face_center, face_radius, skin_color, shirt_color):
    # SHIRT is a big orange circle
    shirt_radius = int(1.25 * face_radius)
    shirt_center = (face_center[0], face_center[1] + int(1.5 * shirt_radius))
    circle(screen, shirt_color, shirt_center, shirt_radius)

    # SLEEVES are two pentagons
    sleeve_angle = 60  # degrees between sleeve-vector and vertical line
    sleeve_x_shift, sleeve_y_shift = shift(1.1 * shirt_radius, sleeve_angle)
    left_sleeve_x, right_sleeve_x = shirt_center[0] - sleeve_x_shift, shirt_center[0] + sleeve_x_shift
    sleeve_y = shirt_center[1] - sleeve_y_shift
    sleeves = [(left_sleeve_x, sleeve_y), (right_sleeve_x, sleeve_y)]  # but we'll draw sleeves after arms

    # ARMS consist of wide lines and two ellipses
    canvas_size = pygame.Surface.get_size(screen)
    hand_y = int(0.15 * canvas_size[1])
    hands_x_shift = int(0.2 * canvas_size[0])
    left_hand_x, right_hand_x = face_center[0] - hands_x_shift, face_center[0] + hands_x_shift
    hands = [(left_hand_x, hand_y), (right_hand_x, hand_y)]
    hand_size = (0.4 * face_radius, 0.5 * face_radius)
    for i in range(2):
        line(screen, skin_color, sleeves[i], hands[i], int(0.2 * face_radius))  # arm
        draw_ellipse(screen, skin_color, hands[i], hand_size)  # hand

    # High time to draw sleeves
    for pair in sleeves:
        draw_sleeve(screen, shirt_color, shirt_radius, pair, shirt_center)

    pass


# - LABEL - LABEL - LABEL - LABEL - LABEL - LABEL - LABEL - LABEL - LABEL - LABEL -
def draw_label(screen):
    # Label is a colored rectangle
    canvas_size = pygame.Surface.get_size(screen)
    indent = 0.01
    label_color = (0, 240, 0)
    label_left_top = (int(indent * canvas_size[0]), 0)
    label_width = int((1 - 2 * indent) * canvas_size[0])
    label_height = int(0.13 * canvas_size[1])
    rectangle = [label_left_top[0], label_left_top[1], label_width, label_height]
    rect(screen, label_color, rectangle)

    # Now we should write a phrase on it!
    text_position = (int(label_left_top[0] + label_width/2), int(label_left_top[1] + label_height/2))
    f = pygame.font.Font(None, 80)
    text = f.render('PYTHON is REALLY AMAZING!', 1, (0, 0, 0))
    place = text.get_rect(center=text_position)
    screen.blit(text, place)
    pass


# - THE WHOLE GUY - THE WHOLE GUY - THE WHOLE GUY - THE WHOLE GUY - THE WHOLE GUY -
def draw_guy(screen, face_center, face_radius, params):
    skin_color = (233, 192, 159)
    draw_shirt_and_arms(screen, face_center, face_radius, skin_color, shirt_color=params[0])
    draw_face(screen, face_center, face_radius, skin_color, hair_color=params[1], eyes_color=params[2])
    draw_label(screen)

    pass


def main():
    # let the program begin
    pygame.init()
    width = 1027
    height = 539
    screen = pygame.display.set_mode((width, height))

    # main settings
    fps = 30

    position1 = (int(width/4), int(height/2))
    params1 = [(0, 150, 0),  # t-shirt color
               (200, 200, 0),  # hair color
               (135, 214, 185)]  # eyes color

    position2 = (int(3 * width/4), int(height/2))
    params2 = [(200, 200, 0),  # t-shirt color
               (200, 0, 200),  # hair color
               (200, 225, 255)]  # eyes color

    face_radius = int(height/3.5)
    draw_guy(screen, position1, face_radius, params1)
    draw_guy(screen, position2, face_radius, params2)

    # final part of the program
    pygame.display.update()
    clock = pygame.time.Clock()
    finished = False

    while not finished:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

    pygame.quit()

    pass


main()
