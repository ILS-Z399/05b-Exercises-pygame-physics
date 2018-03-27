#!/usr/bin/env python
'''

In this exercise, you have a chance to play with music and sound effects.
Find some (appropriately licensed) background music online (I recommend http://freemusicarchive.org) and set it as the soundtrack for this exercise. You should have at least three pieces of music that play alternate randomly.
Then find some sound samples and make them play when keys are pressed. Describe the keys that play sound in your README.md.
There are many sources of Creative Commons licensed sound effects, but most of them require registering with the site.
If you want to add some graphics that are tied to either the music or the sound effects (or both), I will give you extra credit.

The music files that accompany this exercise are:
	http://freemusicarchive.org/music/Lobo_Loco/Long__Relaxed/Chief_Inspector_Baldwin_ID_873
	http://freemusicarchive.org/music/Lobo_Loco/Long__Relaxed/Ambient_Blues_Joe_ID_773
	Both composed and performed by Lobo Loco and distributed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License
Sound effects obtained from:
	https://freesound.org/people/Hanbaal/sounds/178668/ (by Hanbaal)
	https://freesound.org/people/Theriavirra/sounds/270090/ (by Theriavirra)
	And are distributed under a Creative Commons Attribution 3.0 Unported License

'''
import sys, logging, pygame, random, os
assert sys.version_info >= (3,4), 'This script requires at least Python 3.4' 

logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

screen_size = (800,600)
FPS = 60
black = (0,0,0)


def main():
	pygame.init()
	screen = pygame.display.set_mode(screen_size)
	clock = pygame.time.Clock()


	SONG_END = pygame.USEREVENT + 1
	pygame.mixer.music.set_endevent(SONG_END)

	soundtrack = ['Ambient_Blues_Joe_ID_773.mp3','Chief_Inspector_Baldwin_ID_873.mp3']
	current_track = random.choice(soundtrack)
	pygame.mixer.music.load(os.path.join('mp3', current_track))
	pygame.mixer.music.play()
	
	sound_files = ['snare.wav','drumsticks.wav']
	sound_library = []
	for s in sound_files:
		sound_library.append(pygame.mixer.Sound(os.path.join('mp3', s)))

	screen.fill(black)
	while True:
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit(0)
			if event.type == pygame.KEYDOWN:
				keys = pygame.key.get_pressed()
				if keys[pygame.K_UP]:
					logging.info('Pressed up')
					sound_library[0].play()
				if keys[pygame.K_DOWN]:
					logging.info('Pressed down')
					sound_library[1].play()
				if keys[pygame.K_LEFT]:
					logging.info('Pressed left')
				if keys[pygame.K_RIGHT]:
					logging.info('Pressed right')

			if event.type == SONG_END:		# we created a new event type that fires when the song is over
				logging.info('Song ended')
				new_track = random.choice(soundtrack)
				while new_track == current_track:
					new_track = random.choice(soundtrack)
				current_track = new_track
				pygame.mixer.music.load(os.path.join('mp3', current_track))
				pygame.mixer.music.play()

		pygame.display.flip()


if __name__ == '__main__':
	main()