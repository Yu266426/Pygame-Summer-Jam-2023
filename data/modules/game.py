import random

import pygame
import pygbase

from data.modules.events import END_EVENT_TYPE
from data.modules.level import Level


class Game(pygbase.GameState, name="game"):
	def __init__(self, level_name: str):
		super().__init__()

		self.background_colour = pygbase.Common.get_value("background_colour")
		self.screen_size = pygame.Vector2(pygbase.Common.get_value("screen_width"), pygbase.Common.get_value("screen_height"))

		self.lighting_manager = pygbase.LightingManager(0.4)
		self.particle_manager = pygbase.ParticleManager(chunk_size=50, show_debug=False)
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

		self.level = Level(level_name, self.camera, self.particle_manager, self.lighting_manager, self.ui_manager)

		pygbase.EventManager.add_handler("game", END_EVENT_TYPE, self.end_event_handler)

		self.level_ended = False
		self.end_timer = pygbase.Timer(2, True, False)
		self.switching_states = False

	def end_event_handler(self, event: pygame.Event):
		self.level_ended = True
		self.end_timer.start()

	def update(self, delta: float):
		self.lighting_manager.update(delta)
		self.particle_manager.update(delta)
		self.ui_manager.update(delta)

		self.end_timer.tick(delta)

		self.level.update(delta)

		if self.level_ended and self.end_timer.done() and not self.switching_states:
			from data.modules.level_selector import LevelSelector
			self.set_next_state(pygbase.FadeTransition(self, LevelSelector(), 4, (0, 0, 0)))
			self.switching_states = True

		if pygbase.InputManager.get_key_just_pressed(pygame.K_ESCAPE):
			pygbase.EventManager.post_event(pygame.QUIT)

	def draw(self, surface: pygame.Surface):
		surface.fill(self.background_colour)
		self.particle_manager.draw(surface, self.camera)

		self.level.draw(surface)

		self.lighting_manager.draw(surface, self.camera)

		self.ui_manager.draw(surface)
