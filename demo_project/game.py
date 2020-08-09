from tkinter import *

from tkinter import font
import time
import random

class GameOfLife(Frame):

	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		self.grid(row = 0, column = 0)
		self.cell_buttons = []
		self.generate_next = True

	def set_Grid_Size(self,x,y):
		self.size_x = x
		self.size_y = y

#the state(live or dead) is stored in bg color.
	def make_frame(self):	
		self.parent.title("Game of Life")	
		self.title_frame = Frame(self.parent)
		self.title_frame.grid(row = 0, column = 0, columnspan = 5)
		self.titleFont = font.Font(family="Helvetica", size=14)
		title = Label(self.title_frame, text = "Game of Life", font = self.titleFont)
		title.pack(side = TOP, expand = True)
		prompt = Label(self.title_frame, text = "Click the cells to create the starting configuration, the press Start Game:")
		prompt.pack(side = BOTTOM)
		self.start_button = Button(self.parent, text = "Start Game", command = self.simulate_game)
		self.start_button.grid(row = 1, column = 1, sticky = E)
		self.reset_button = Button(self.parent, text = "Reset", state = DISABLED, command = self.reset_game)
		self.reset_button.grid(row =1 , column = 2, sticky = W)
		self.randomize_start_button = Button(self.parent, text = "Randomize", command = self.r)
		self.randomize_start_button.grid(row =1 , column = 3, sticky = W)
		self.build_grid()

	def r(self):
		for i in range(1, self.size_y + 1):
			for j in range(1, self.size_x + 1):	
				self.cell_buttons[i][j].grid(row = i, column = j)
		
				t = random.choice([0,1])
				if(t):
					self.cell_toggle(self.cell_buttons[i][j])

	def build_grid(self):
		self.game_frame = Frame(
			self.parent, width = self.size_x + 2, height = self.size_y + 2, borderwidth = 0)
		self.game_frame.grid(row = 2, column = 0, columnspan = 5)
		self.cell_buttons = [[Button(self.game_frame, bg = "ghost white", width = 1, height = 1) for i in range(self.size_x + 2)] for j in range(self.size_y + 2)]
		for i in range(1, self.size_y + 1):
			for j in range(1, self.size_x + 1):	
				self.cell_buttons[i][j].grid(row = i, column = j,sticky = N+E+S+W)
				self.cell_buttons[i][j]['command'] = lambda i=i, j=j:self.cell_toggle(self.cell_buttons[i][j])

	def simulate_game(self):
		self.disable_buttons()
		buttons_to_toggle = []
		for i in range(1, self.size_y + 1):
			for j in range(1, self.size_x + 1):
				coord = (i, j)
				
				if self.cell_buttons[i][j]['bg'] == "ghost white" and self.neighbor_count(i, j) == 3:
					buttons_to_toggle.append(coord)
				
				elif self.cell_buttons[i][j]['bg'] == "midnight blue" and self.neighbor_count(i, j) != 3 and self.neighbor_count(i, j) != 2:
					buttons_to_toggle.append(coord)
		for coord in buttons_to_toggle:
			self.cell_toggle(self.cell_buttons[coord[0]][coord[1]])			

		if self.generate_next:
			self.after(60, self.simulate_game)
		else:
			self.enable_buttons()

	def disable_buttons(self):

		if self.cell_buttons[1][1] != DISABLED:
			for i in range(0, self.size_y + 2):
				for j in range(0, self.size_x + 2):
					self.cell_buttons[i][j].configure(state = DISABLED)

			self.reset_button.configure(state = NORMAL)
			self.start_button.configure(state = DISABLED)
			self.randomize_start_button.configure(state =  DISABLED)

	def enable_buttons(self):
		for i in range(0, self.size_y + 2):
			for j in range(0, self.size_x + 2):
				self.cell_buttons[i][j]['bg'] = "ghost white"
				self.cell_buttons[i][j].configure(state = NORMAL)

		self.reset_button.configure(state = DISABLED)
		self.start_button.configure(state = NORMAL)
		self.randomize_start_button.configure(state = NORMAL)
		self.generate_next = True

	def neighbor_count(self, x_coord, y_coord):
		count = 0
		for i in range(x_coord - 1, x_coord + 2):
			for j in range(y_coord - 1, y_coord + 2):
				#continue when i = x_coord and j = y_coord and check for live neighbors
				if (i != x_coord or j != y_coord) and self.cell_buttons[i][j]['bg'] == "midnight blue":
					count = count+1
		return count

	def cell_toggle(self, cell):
		if cell['bg'] == "ghost white":
			cell['bg'] = "midnight blue"
		else:
			cell['bg'] = "ghost white"

	def reset_game(self):
		self.generate_next = False
