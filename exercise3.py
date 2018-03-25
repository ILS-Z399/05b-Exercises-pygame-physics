#!/usr/bin/env python
'''

The character is walking (running?) based on animations from the "adventurer.png" sprite sheet. A guide (frameGuide.png) to the sprite sheet is available.

When the character jumps (when the player presses the up button), use the jumping animation instead of the walking animation. You will need to change the update() method.

Add a scrolling background image, including a floor.

For extra credit, add something for him to jump over (and consequences for not jumping)

The animation was created by MoikMellah (https://opengameart.org/content/mv-platformer-male-32x64) and is provided under a Public Domain license.

'''
import sys, logging, pygame, random, os
assert sys.version_info >= (3,4), 'This script requires at least Python 3.4' 

logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

screen_size = (800,600)
FPS = 60
black = (0,0,0)
img_size = (32,64)
img_margin = (0,0)
starting_position = (200,400)
walking = [(1,0),(2,0),(3,0),(4,0),(5,0),(6,0)]
gravity = 0.6

class Runner(pygame.sprite.Sprite):
	def __init__(self, img, position):
		pygame.sprite.Sprite.__init__(self)
		self.sheet = pygame.image.load(os.path.join('.', img)).convert()	# load the image from the current folder and convert it so pygame.image can use it
		(self.width,self.height) = img_size			# the width and height of the image on the sprite sheet
		(self.margin_x,self.margin_y) = img_margin	# the space between the images on the sprite sheet

		self.rect = pygame.Rect((self.margin_x,self.margin_y,self.width,self.height))
		self.image = pygame.Surface(self.rect.size).convert()
		self.image.blit(self.sheet, (0,0), self.rect)	#from the sheet, grab the correct image
		
		(self.rect.x,self.rect.y) = position

		self.walking_animation = 0
		self.ground = position[1]
		self.jumping = False
		self.velocity = (0.0,0.0)
		self.jump_velocity = 10
		
	def update(self):
		(vx,vy) = self.velocity
		if not self.jumping:
			(i,j) = walking[self.walking_animation]
			x = (self.width + self.margin_x)*i + self.margin_x
			y = (self.height + self.margin_y)*j + self.margin_y
			self.image.blit(self.sheet, (0,0), (x,y,self.width,self.height))
			self.walking_animation += 1
			self.walking_animation %= len(walking)
		else:
			self.rect.x += vx
			self.rect.y += vy
			vy += gravity
			if self.rect.top >= self.ground:
				self.rect.top = self.ground
				vy = 0
				self.jumping = False
		self.velocity = (vx,vy)
	
	def jump(self):
		if not self.jumping:
			(vx,vy) = self.velocity
			vy -= self.jump_velocity
			self.velocity = (vx,vy)
			self.jumping = True
				

def main():
	pygame.init()
	screen = pygame.display.set_mode(screen_size)
	clock = pygame.time.Clock()

	rgroup = pygame.sprite.Group()
	runner = Runner('adventurer.png',starting_position)
	rgroup.add(runner)

	while True:
		clock.tick(FPS)
		screen.fill(black)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit(0)

		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP]:
			runner.jump()

		rgroup.update()
		rgroup.draw(screen)
		pygame.display.flip()

if __name__ == '__main__':
	main()