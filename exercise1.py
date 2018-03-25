#!/usr/bin/env python
'''

Choose values for gravity, friction, and air_resistance (lines 25–27). Try to find a combination that seems realistic

For every line in the update method (lines 41-66), please add a comment describing what it does. 

Try to describe each line within the context of the program as a whole, rather than just mechanically

Feel free to alter the parameters to see how things change. That can be a great way to be able to intuit what is supposed to be happening

I will do a few lines for you as an example


'''
import sys, logging, random, pygame
assert sys.version_info >= (3,4), 'This script requires at least Python 3.4'

logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

screen_size = (600,600)
FPS = 60
black = (0,0,0)
gravity = 0
friction = 0
air_resistance = 0

class Ball(pygame.sprite.Sprite):
	def __init__(self, i, size, color, position, direction):
		pygame.sprite.Sprite.__init__(self)
		self.size = size
		self.image = pygame.Surface(size)
		self.rect = self.image.get_rect()
		pygame.draw.ellipse(self.image, color, self.rect)
		self.image.set_colorkey((0,0,0))
		(self.rect.x,self.rect.y) = position
		self.direction = direction
		self.id = i

	def update(self):
		(dx,dy) = self.direction	# get the current velocity
		self.rect.x += dx		# move the sprite
		self.rect.y += dy

		dy = dy + gravity
		dx *= (1.0-air_resistance)
		dy *= (1.0-air_resistance)
		
		(WIDTH,HEIGHT) = screen_size
		if self.rect.right >= WIDTH:
			self.rect.right = WIDTH
			dx = dx * -1 * (1.0-friction)
		if self.rect.left <= 0:
			self.rect.left = 0
			dx = dx * -1 * (1.0-friction)
		if self.rect.top <= 0:
			self.rect.top = 0
			dy = dy * -1 * (1.0-friction)
		if self.rect.bottom >= HEIGHT:
			self.rect.bottom = HEIGHT
			dx = dx * -1 * (1.0-friction)
			dy = dy * -1 * (1.0-friction)
			if abs(dy) < 1:			# keep it from bouncing forever
				dy = 0
		self.direction = (dx,dy)


def main():
	pygame.init()
	screen = pygame.display.set_mode(screen_size)
	clock = pygame.time.Clock()

	balls = pygame.sprite.Group()
	for i in range(random.randrange(10,50)):
		size = random.randrange(10,50)
		color = (random.randrange(255),random.randrange(255),random.randrange(255))
		initial_position = (random.randrange(25,screen_size[0]-25),random.randrange(25,screen_size[1]-25))
		initial_velocity = (random.randrange(-10,10),0)
		ball = Ball(i,(size,size),color,initial_position,initial_velocity)
		balls.add(ball)

	while True:
		clock.tick(FPS)
		screen.fill(black)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit(0)

		balls.update()
		balls.draw(screen)
		pygame.display.flip()

if __name__ == '__main__':
	main()