import random

import pygame
import pygbase


class LevelSelector(pygbase.GameState, name="level_selector"):
	def __init__(self):
		super().__init__()

		self.background_colour = pygbase.Common.get_value("background_colour")
		self.screen_size = pygame.Vector2(pygbase.Common.get_value("screen_width"), pygbase.Common.get_value("screen_height"))

		self.lighting_manager = pygbase.LightingManager(0.4)
		self.particle_manager = pygbase.ParticleManager(chunk_size=50, show_debug=False)
		self.ui_manager = pygbase.UIManager()

		self.camera = pygbase.Camera()

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
			self.screen_size / 2, 2, 100, 1100, True, "micro", self.particle_manager
		))

		self.ui = pygbase.UIManager()

		self.selector_frame = self.ui.add_frame(
			pygbase.Frame(
				(pygbase.UIValue(0.1, False), pygbase.UIValue(0.1, False)),
				(pygbase.UIValue(0.8, False), pygbase.UIValue(0.8, False)),
				self.ui.base_container,
				bg_colour=(0, 0, 0, 50)
			)
		)

		for level in range(pygbase.Common.get_value("num_levels")):
			self.selector_frame.add_element(
				pygbase.Button(
					(pygbase.UIValue(0.05, False), pygbase.UIValue(0.05, False)),
					(pygbase.UIValue(0.18, False), pygbase.UIValue(0)),
					"image", "button",
					self.selector_frame, self.switch_level, callback_args=(str(level + 1),),
					text=str(level + 1), text_colour=(240, 240, 240)
				), add_on_to_previous=(False, True)
			)

	def switch_level(self, level_name: str):
		from data.modules.game import Game

		self.set_next_state(pygbase.FadeTransition(self, Game(level_name), 4, (0, 0, 0)))

	def update(self, delta: float):
		self.ui.update(delta)
		self.lighting_manager.update(delta)
		self.particle_manager.update(delta)

	def draw(self, surface: pygame.Surface):
		surface.fill(self.background_colour)

		self.particle_manager.draw(surface, self.camera)
		self.lighting_manager.draw(surface, self.camera)

		self.ui.draw(surface)
