from tkinter import *
from game import GameOfLife



if __name__ == '__main__':
	root = Tk()
	game = GameOfLife(root)
	x = input("length of the grid: ")
	y = input("breadth of the grid: ")

	game.set_Grid_Size(int(x),int(y))
	game.make_frame()

	root.mainloop()
