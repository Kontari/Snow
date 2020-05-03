#/usr/bin/env python
import datetime
import random as r
import sys
import time

import curses

tree = """
              v .   ._, |_  .,
           `-._\/  .  \ /    |/_
               \\  _\, y | \//
         _\_.___\\, \\/ -.\||
           `7-,--.`._||  / / ,
           /'     `-. `./ / |/_.'
                     |    |//
                     |_    /
                     |-   |
                     |   =|
                     |    |
-..----._.---.___---/ ,  . \--._"""


X_SPEED_LIM = 2
Y_SPEED_LIM = 3
NUM_SNOWFLAKES = 100


class Snow:
    def __init__(self, max_y, max_x):
        self.x = r.randint(X_SPEED_LIM, max_x - X_SPEED_LIM)
        self.y = r.randint(Y_SPEED_LIM, max_y - Y_SPEED_LIM)
        self.sprite = r.choice(['*', '+', "."])
        self.speed = r.randint(1, Y_SPEED_LIM)
        self.wind = r.randint(-1 * X_SPEED_LIM, X_SPEED_LIM)


def main():

    # Configure window
    stdscr = curses.initscr()
    curses.noecho()
    curses.curs_set(0)

    max_y, max_x = stdscr.getmaxyx()

    '''
	Generate a ground pattern resembling snow
	by alternating patterns of ..__ and ..--
	'''
    ground = ""
    for i in range(0, max_y):
        ground += (r.randint(1, 6) * ".")
        ground += (r.randint(1, 4) * r.choice(["-", "_"]))

    '''
	Generate a backround image. Stored in a list this will be parsed
	and written behind the snow layer.
	'''
    background = []

    for x in range(0, max_x):
        temp = []

        for y in range(0, max_y):
            temp.append(' ')

        background.append(temp)

    '''
        Logic to continually draw snowflakes on the screen
        '''
    try:
        snowflakes = []

        # Generating snowflakes
        for i in range(0, NUM_SNOWFLAKES):
            snowflakes.append(Snow(max_y, max_x))

        # Draw the background at first
        for x in range(0, max_x-1):
            for y in range(0, max_y-1):
                stdscr.addch(y, x, background[x][y])

        while True:
            # Draw the ground
            stdscr.addnstr(max_y-2, 0, ground * 100, max_x)

            # Draw the tree
            stdscr.addstr(max_y-14, max_x-50, tree)

            for s in snowflakes:
                '''
                Overwrite old flake position with corresponding
                background x,y character
                '''
                stdscr.addch(s.y, s.x, background[s.x][s.y])

                # Bounds checking for vertical movement
                if (s.y + s.speed < max_y):
                    s.y += s.speed
                else:  # reset flake if out of bounds
                    s.y = 1
                    s.x = r.randint(X_SPEED_LIM, max_x - X_SPEED_LIM)

                # Bounds checking for horizontal movement
                if (2 < s.x + s.wind < max_x-2):
                    s.x += s.wind
                else:  # reset flake if out of bounds
                    s.y = 1
                    s.x = r.randint(X_SPEED_LIM, max_x - X_SPEED_LIM)

                # Draw new snowflake position
                stdscr.addch(s.y, s.x, s.sprite)

            # Draw the time
            time_raw = datetime.datetime.now().strftime("%I:%M:%S")
            stdscr.addstr(int(max_y/2), int(max_x/2)-8, str(time_raw))

            time.sleep(0.2)

            stdscr.refresh()

    except KeyboardInterrupt:
        print("Exiting.")

    finally:
        curses.endwin()


main()
