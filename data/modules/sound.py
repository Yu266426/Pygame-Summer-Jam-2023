import random

import pygame
import pygbase

from data.modules.files import MUSIC_DIR


class SoundHandler:
	current_music: str = ""
	water_timer = pygbase.Timer(random.uniform(0.9, 3.0), False, False)

	@classmethod
	def update(cls, delta: float):
		cls.water_timer.tick(delta)
		if cls.water_timer.done():
			SoundHandler.play_sound(random.choice(pygbase.Common.get_value("water_sounds")))
			cls.water_timer.set_cooldown(random.uniform(5.0, 12.0))
			cls.water_timer.start()

	@classmethod
	def play_music(cls, name: str, volume: float = 1.0):
		if cls.current_music != name:
			if pygame.mixer.music.get_busy():
				pygame.mixer.music.fadeout(400)
				pygame.mixer.music.queue(MUSIC_DIR / f"{name}.wav", loops=-1)
			else:
				pygame.mixer.music.load(MUSIC_DIR / f"{name}.wav")
				pygame.mixer.music.set_volume(volume)
				pygame.mixer.music.play(-1)

			cls.current_music = name

	@classmethod
	def play_sound(cls, name: str):
		sound: pygame.mixer.Sound = pygbase.ResourceManager.get_resource("sound", name)
		sound.play()
