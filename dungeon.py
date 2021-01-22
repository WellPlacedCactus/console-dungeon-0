import os
import sys
import threading
import keyboard
from random import randint

class Player:
	def __init__(self, x, y, c):
		self.x = x
		self.y = y
		self.c = c
		self.vx = 0
		self.vy = 0

	def inp(self):
		if keyboard.is_pressed('up'):
			self.vy = -1
		elif keyboard.is_pressed('down'):
			self.vy = 1
		else:
			self.vy = 0

		if keyboard.is_pressed('left'):
			self.vx = -1
		elif keyboard.is_pressed('right'):
			self.vx = 1
		else:
			self.vx = 0

	def move(self):
		self.x += self.vx
		self.y += self.vy

	def collide(self, dungeon):
		if self.x < 0: self.x = dungeon.w - 1
		if self.y < 0: self.y = dungeon.h - 1
		if self.x > dungeon.w - 1: self.x = 0
		if self.y > dungeon.h - 1: self.y = 0

	def eat(self, dungeon):
		for y in range(dungeon.h):
			for x in range(dungeon.w):
				tile = dungeon.map[y][x]
				if tile == dungeon.fg:
					if self.x == x and self.y == y:
						dungeon.map[y][x] = dungeon.bg
						dungeon.apples -= 1

	def tick(self, dungeon):
		self.inp()
		self.move()
		self.collide(dungeon)
		self.eat(dungeon)

class Dungeon:
	def __init__(self, w, h, bg, fg, p):
		self.w = w
		self.h = h
		self.bg = bg
		self.fg = fg
		self.p = p
		self.map = []
		self.apples = 3
		self.gen()

	def gen(self):
		# field
		for y in range(self.h):
			row = []
			for x in range(self.w):
				row.append(self.bg)
			self.map.append(row)
		# apples
		for i in range(self.apples):
			x = randint(0, self.w - 1)
			y = randint(0, self.h - 1)
			self.map[y][x] = '#'

	def clear(self):
		os.system('cls')

	def log(self):
		for y in range(self.h):
			row = ''
			for x in range(self.w):
				if x == self.p.x and y == self.p.y:
					row += p.c
				else:
					row += self.map[y][x]
				row += ' '
			print(row)

	def score(self):
		if self.apples < 1:
			print('You win!')
		else:
			print(f'Hashtags left: {self.apples}')

	def tick(self):
		self.clear()
		self.log()
		self.score()

p = Player(5, 5, '@')
d = Dungeon(14, 14, '.', '#', p)

def loop():
	threading.Timer(1 / 16, loop).start()
	p.tick(d)
	d.tick()
loop()