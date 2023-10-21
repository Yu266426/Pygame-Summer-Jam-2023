import json
import random

import pygame
import pygbase

from data.modules.events import END_EVENT_TYPE, WIN_EVENT_TYPE
from data.modules.files import DATA_DIR
from data.modules.level import Level
from data.modules.sound import SoundHandler


class Game(pygbase.GameState, name="game"):
	def __init__(self, level_name: str):
		super().__init__()

		self.background_colour = pygbase.Common.get_value("background_colour")
		self.screen_size = pygame.Vector2(pygbase.Common.get_value("screen_width"), pygbase.Common.get_value("screen_height"))

		self.lighting_manager = pygbase.LightingManager(0.4)
		self.particle_manager = pygbase.ParticleManager(chunk_size=50)
		self.ui_manager = pygbase.UIManager()

		self.camera = pygbase.Camera(-self.screen_size / 2)

		self.lighting_manager.add_light(pygbase.Light(
			self.screen_size / 2,
			0.2,
			self.screen_size.x * 1,
			0, 0,
			camera_affected=False
		))
		self.lighting_manager.add_light(pygbase.Light(
			self.screen_size / 2,
			0.35,
			self.screen_size.x * 0.6,
			0, 0,
			camera_affected=False
		))

		micro_particle_settings = pygbase.Common.get_particle_setting("micro")

		for _ in range(random.randint(100, 200)):
			self.particle_manager.add_particle(
				pygame.Vector2(random.uniform(-600, 600), random.uniform(-600, 600)),
				micro_particle_settings
			)

		self.particle_manager.add_spawner(pygbase.CircleSpawner(
			self.camera.pos, 2, 100, 1100, True, "micro", self.particle_manager
		).link_pos(self.camera.pos))

		self.level_name = level_name
		self.level = Level(level_name, self.camera, self.particle_manager, self.lighting_manager, self.ui_manager)

		pygbase.EventManager.add_handler("game", END_EVENT_TYPE, self.end_event_handler)
		pygbase.EventManager.add_handler("game", WIN_EVENT_TYPE, self.win_event_handler)

		self.level_ended = False
		self.level_won = False
		self.end_timer = pygbase.Timer(2, True, False)
		self.switching_states = False

		SoundHandler.play_music("main")

	def end_event_handler(self, event: pygame.Event):
		self.level_ended = True
		self.end_timer.start()

	def win_event_handler(self, event: pygame.Event):
		self.level_won = True

	def update(self, delta: float):
		self.lighting_manager.update(delta)
		self.particle_manager.update(delta)
		self.ui_manager.update(delta)
		SoundHandler.update(delta)

		self.end_timer.tick(delta)

		self.level.update(delta)

		if self.level_ended and self.end_timer.done() and not self.switching_states:
			to_win_screen = False

			if self.level_won:
				with open(DATA_DIR / "save.json", "r") as save_file:
					data = json.load(save_file)

				# Final level
				if not data["completed"] and pygbase.Common.get_value("num_levels") == int(self.level_name):
					data["completed"] = True

					with open(DATA_DIR / "save.json", "w") as save_file:
						save_file.write(json.dumps(data))

					to_win_screen = True

				# Unlock next level
				elif pygbase.Common.get_value("available_levels") == int(self.level_name):
					pygbase.Common.set_value("available_levels", int(self.level_name) + 1)
					data["available_levels"] = int(self.level_name) + 1

					with open(DATA_DIR / "save.json", "w") as save_file:
						save_file.write(json.dumps(data))

			if not to_win_screen:
				from data.modules.level_selector import LevelSelector
				self.set_next_state(pygbase.FadeTransition(self, LevelSelector(), 4, (0, 0, 0)))
				self.switching_states = True
			else:
				from data.modules.win import Win
				self.set_next_state(pygbase.FadeTransition(self, Win(), 4, (0, 0, 0)))
				self.switching_states = True

		if pygbase.InputManager.get_key_just_pressed(pygame.K_ESCAPE):
			self.level_ended = True
			self.level.ended = True
			self.level.player.ended = True

			from data.modules.level_selector import LevelSelector
			self.set_next_state(pygbase.FadeTransition(self, LevelSelector(), pygbase.Common.get_value("trans_time"), (0, 0, 0)))
			self.switching_states = True

			SoundHandler.play_sound(random.choice(pygbase.Common.get_value("water_sounds")))

	def draw(self, surface: pygame.Surface):
		surface.fill(self.background_colour)
		self.particle_manager.draw(surface, self.camera)

		self.level.draw(surface)

		self.lighting_manager.draw(surface, self.camera)

		self.ui_manager.draw(surface)
