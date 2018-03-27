#!/usr/bin/env python
'''

For every line in the collide method (lines 58-91), please add a comment describing what it does. 

Try to describe each line within the context of the program as a whole, rather than just mechanically

Feel free to alter the parameters to see how things change. That can be a great way to be able to intuit what is supposed to be happening

I will do a few lines for you as an example


'''
import sys, logging, math, pygame, random as r
assert sys.version_info >= (3,4), 'This script requires at least Python 3.4'

logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

screen_size = (WIDTH,HEIGHT) = (600,600)
FPS = 60
black = (0,0,0)

class Ball(pygame.sprite.Sprite):
	def __init__(self, label, size, mass, color, position, direction):
		pygame.sprite.Sprite.__init__(self)
		self.label = label
		self.size = size
		self.image = pygame.Surface(size)
		self.rect = self.image.get_rect()
		pygame.draw.ellipse(self.image, color, self.rect)
		self.image.set_colorkey((0,0,0))
		(self.rect.x,self.rect.y) = position
		self.direction = direction
		self.mass = mass
		self.collided = False

	def update(self):
		(dx,dy) = self.direction
		self.rect.x += dx
		self.rect.y += dy
		
		(WIDTH,HEIGHT) = screen_size
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
			dx *= -1
		if self.rect.left < 0:
			self.rect.left = 0
			dx *= -1
		if self.rect.top < 0:
			self.rect.top = 0
			dy *= -1
		if self.rect.bottom > HEIGHT:
			self.rect.bottom = HEIGHT
			dy *= -1
		self.direction = (dx,dy)
	
	def collide(self, other_object):	
		'''
		
		Checks to see if the object has collided with another object. Assumes that each collision will be calculated pairwise.
		If there has been a collision, and the objects are still moving toward each other, the direction attribute of both objects is updated
		
		
		'''
		(dx,dy) = self.direction				# the x and y components of the direction
		(odx,ody) = other_object.direction		# the x and y components of the other object's direction
		(cx,cy) = self.rect.center
		(ocx,ocy) = other_object.rect.center
		radius = self.rect.width/2
		oradius = other_object.rect.width/2
		#find the hypotenuse
		distance = math.sqrt(abs(cx-ocx)**2 + abs(cy-ocy)**2)
		if distance <= 0:
			distance = 0.1
		combined_distance = (radius+oradius)
		if distance <= combined_distance:	#collision
			normal = ((cx-ocx)/distance,(cy-ocy)/distance)	# a vector tangent to the plane of collision
			velocity_delta = ((odx-dx),(ody-dy))	#the relative difference between the speed of the two objects
			(nx,ny) = normal
			(vdx,vdy) = velocity_delta
			dot_product = nx*vdx + ny*vdy
			if dot_product >= 0:	#check if the objects are moving toward each other
				impulse_strength = dot_product * (self.mass / other_object.mass)
				impulse = (ix,iy) = (impulse_strength * nx, impulse_strength * ny)
				dx += ix * (other_object.mass/self.mass)
				dy += iy * (other_object.mass/self.mass)
				self.direction = (dx,dy)
				odx -= ix * (self.mass/other_object.mass)
				ody -= iy * (self.mass/other_object.mass)
				other_object.direction = (odx,ody)

	def draw(self,screen):
		self.image.blit(screen,(0,0),self.rect)

	def get_energy(self):
		(dx,dy) = self.direction
		return math.sqrt(abs(dx)**2 + abs(dy)**2)/self.mass

def main():
	pygame.init()
	screen = pygame.display.set_mode(screen_size)
	clock = pygame.time.Clock()

	balls = []
	colors = [(255,212,59),(34,139,230),(240,62,62),(174,62,201),(253,126,20),(64,192,87),(194,37,92),(73,80,87)]
	positions = [(260,180),(180,100),(260,100),(340,100),(220,60),(220,140),(300,140),(300,60)]
	size = (50,50)
	mass = 30
	initial_velocity = (0,0)
	for c in range(len(colors)):
		initial_position = positions[c]
		ball = Ball('{0}'.format(c+1),size,mass,colors[c],initial_position,initial_velocity)
		balls.append(ball)
	ball = Ball('Cue',size,mass,(255,255,255),(260,500),(0,-20))
	balls.append(ball)

	ball_group = pygame.sprite.Group()
	for b in balls:
		ball_group.add(b)

	
	while True:
		clock.tick(FPS)
		screen.fill(black)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit(0)

		for b in balls:
			for c in balls:
				if b.label != c.label:
					b.collide(c)
		ball_group.update()
		ball_group.draw(screen)
		pygame.display.flip()

if __name__ == '__main__':
	main()