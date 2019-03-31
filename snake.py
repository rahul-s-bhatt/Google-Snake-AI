from random import *
from time import *

import cv2
import numpy as np
import pyautogui
import pyscreenshot as ImageGrab


def goUp():
    pyautogui.keyDown('w')
    pyautogui.keyUp('w')

def goLeft():
    pyautogui.keyDown('a')
    pyautogui.keyUp('a')

def goRight():
    pyautogui.keyDown('d')
    pyautogui.keyUp('d')


def goDown():
    pyautogui.keyDown('s')
    pyautogui.keyUp('s')


box_cords = [439, 228, 981, 706]


STATE = 'RIGHT'

while True:

    screen = np.array(ImageGrab.grab(bbox=box_cords))
    screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

    imgray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    img_hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)


    # apple masking
    lower_bound = np.array([0, 50, 50])
    higher_bound = np.array([10, 255, 255])

    # Snake Masking
    lower_bound_snake = np.array([104, 117, 222])
    higher_bound_snake = np.array([121, 255, 255])

    # Apple Masking mask
    mask = cv2.inRange(img_hsv, lower_bound, higher_bound)
    # Snake masking mask
    mask1 = cv2.inRange(img_hsv, lower_bound_snake, higher_bound_snake)

    res = cv2.bitwise_and(screen, screen, mask=mask)
    res1 = cv2.bitwise_and(screen, screen, mask=mask1)


    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours1, hierarchy1 = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Drawing Contours on APPLE


    contour_sizes = [(cv2.contourArea(contour), contour)for contour in contours]
    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    x, y, w, h = cv2.boundingRect(biggest_contour)
    # determine the most extreme points along the contour
    extLeft = tuple(biggest_contour[biggest_contour[:, :, 0].argmin()][0])
    x, y = np.add(extLeft[0], 12), np.subtract(extLeft[1], 1)

    # Drawing Contours on SNAKE


    contour_sizes1 = [(cv2.contourArea(contour), contour)
                        for contour in contours1]
    biggest_contour1 = max(contour_sizes1, key=lambda x1: x1[0])[1]
    # determine the most extreme points along the contour
    extRight = tuple(biggest_contour1[biggest_contour1[:, :, 0].argmax()][0])
    x1, y1 = extRight[0], np.subtract(extRight[1], 5)


    ''' NOW Y1 Y are SAME, LET'S GOOOOOO!!!!!! '''


    ''' SNAKE MOVEMENTS '''

    if x1 < x:
        if STATE == 'LEFT':
            if y1 > y:
                goUp()
                STATE = 'UP'
            elif y > y1:
                goDown()
                STATE = 'DOWN'
        else:
            goRight()
            STATE = 'RIGHT'

    elif x1 > x:
        if STATE == 'RIGHT':
            if y1 > y:
                goUp()
                STATE = 'UP'
            elif y > y1:
                goDown()
                STATE = 'DOWN'
        else:
            goLeft()
            STATE = 'LEFT'

    elif y < y1:
        if STATE == 'DOWN':
            if x1 > x:
                goLeft()
                STATE = 'LEFT'
            elif x > x1:
                goRight()
                STATE = 'RIGHT'
        else:
            goUp()
            STATE = 'UP'

    elif y > y1:
        if STATE == 'UP':
            if x1 > x:
                goLeft()
                STATE = 'LEFT'
            elif x > x1:
                goRight()
                STATE = 'RIGHT'
        else:
            goDown()
            STATE = 'DOWN'
    
    # TERMINATE THE CONSOLE
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
