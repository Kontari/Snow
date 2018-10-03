import random as r
import sys, curses, time
'''
TODO:
snowman
clock?
trees
debug wind force?
'''

class Snow:
	def __init__(self, max_y, max_x):
		self.x = r.randint(0,max_x-1)
		self.y = r.randint(0,max_y-1)
		self.sprite = r.choice(['*','+',"."])
		self.speed = r.randint(1,3)
		self.wind = r.randint(-1,1)



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
	for i in range(0,max_y):
		ground += (r.randint(1,6)*".")
		ground += (r.randint(1,4)*r.choice(["-","_"]))

	'''
	Generate a backround image. Stored in a list this will be parsed
	and written behind the snow layer.
	'''
	background = []

	for x in range(0,max_x):
		temp = []

		for y in range(0,max_y):
			temp.append(" ")
		background.append(temp)


	try:
		snowflakes=[]

		# Generating snowflakes
		for i in range(0,100):
			snowflakes.append(Snow(max_y,max_x))

		while 1:
			for s in snowflakes:

				'''
				Overwrite old flake position with corresponding
				background x,y character
				'''
				stdscr.addch(s.y, s.x, background[s.x][s.y])
				#stdscr.addch(s.y, s.x, ' ')

				# Bounds checking for vertical movement
				if (s.y + s.speed < max_y):
					s.y += s.speed
				else: # reset flake if out of bounds
					s.y = 0
					s.x = r.randint(abs(s.wind),max_x-abs(s.wind))

				# Bounds checking for horizontal movement
				if ((s.x + s.wind < max_x-2) and (s.x - s.wind > 2)):
					s.x += s.wind
				else: # reset flake if out of bounds
					s.y = 0
					s.x = r.randint(abs(s.wind),max_x-abs(s.wind))

				# Draw new snowflake position
				stdscr.addch(s.y, s.x, s.sprite)

			# Draw the ground
			stdscr.addnstr(max_y-2,0,ground*100,max_x)

			# For slower computers this line can be commented out
			time.sleep(0.1)

			stdscr.refresh()

	except KeyboardInterrupt:
		print("Exiting.")

	finally:
		curses.endwin()

main()
