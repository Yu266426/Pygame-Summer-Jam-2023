import random

import pygame
import pygbase

from data.modules.level import Level


class Game(pygbase.GameState, name="game"):
	def __init__(self):
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

		self.level = Level("test", self.camera, self.particle_manager, self.ui_manager)

	def update(self, delta: float):
		self.lighting_manager.update(delta)
		self.particle_manager.update(delta)
		self.ui_manager.update(delta)

		self.level.update(delta)

		if pygbase.InputManager.get_key_just_pressed(pygame.K_ESCAPE):
			pygbase.EventManager.post_event(pygame.QUIT)

	def draw(self, surface: pygame.Surface):
		surface.fill(self.background_colour)
		self.particle_manager.draw(surface, self.camera)

		self.level.draw(surface)

		self.lighting_manager.draw(surface, self.camera)

		self.ui_manager.draw(surface)
