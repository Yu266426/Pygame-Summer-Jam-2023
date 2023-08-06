import random

import pygame
import pygbase

from data.modules.files import ASSET_DIR
from data.modules.sound import SoundHandler


class LevelSelector(pygbase.GameState, name="level_selector"):
	def __init__(self):
		super().__init__()

		self.background_colour = pygbase.Common.get_value("background_colour")
		self.screen_size = pygame.Vector2(pygbase.Common.get_value("screen_width"), pygbase.Common.get_value("screen_height"))

		self.lighting_manager = pygbase.LightingManager(0.4)
		self.particle_manager = pygbase.ParticleManager(chunk_size=50, show_debug=False)
		self.ui_manager = pygbase.UIManager()

		self.camera = pygbase.Camera(-self.screen_size / 2)

		self.mouse_world_pos = self.camera.screen_to_world(pygame.mouse.get_pos())

		self.setup()

		self.selector_frame = self.ui_manager.add_frame(
			pygbase.Frame(
				(pygbase.UIValue(0.1, False), pygbase.UIValue(0.1, False)),
				(pygbase.UIValue(0.8, False), pygbase.UIValue(0.6, False)),
				self.ui_manager.base_container,
				bg_colour=(0, 0, 0, 50)
			)
		)

		self.ui_manager.add_element(
			pygbase.Button(
				(pygbase.UIValue(0.1, False), pygbase.UIValue(0.75, False)),
				(pygbase.UIValue(0.8, False), pygbase.UIValue(0.15, False)),
				"image", "large_button",
				self.ui_manager.base_container,
				self.back_button_handler,
				text="Back To Menu",
				text_colour=(240, 240, 240),
				font=ASSET_DIR / "fira_sans.ttf",
				use_sys=False
			)
		)

		for level in range(min(pygbase.Common.get_value("available_levels"), pygbase.Common.get_value("num_levels"))):
			self.selector_frame.add_element(
				pygbase.Button(
					(pygbase.UIValue(0.05, False), pygbase.UIValue(0.05, False)),
					(pygbase.UIValue(0.9, False), pygbase.UIValue(0.108, False)),
					"image", "button",
					self.selector_frame, self.switch_level, callback_args=(str(level + 1),),
					text=str(level + 1), text_colour=(240, 240, 240),
					font=ASSET_DIR / "fira_sans.ttf",
					use_sys=False
				), add_on_to_previous=(False, True)
			)

	def setup(self):
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

		self.particle_manager.add_affector(
			pygbase.AffectorTypes.ATTRACTOR,
			pygbase.ParticleAttractor(self.mouse_world_pos, 400, 3000).link_pos(self.mouse_world_pos)
		)

		SoundHandler.play_music("intro")

	def switch_level(self, level_name: str):
		from data.modules.game import Game

		self.set_next_state(pygbase.FadeTransition(self, Game(level_name), pygbase.Common.get_value("trans_time"), (0, 0, 0)))

	def back_button_handler(self):
		from data.modules.main_menu import MainMenu

		self.set_next_state(pygbase.FadeTransition(self, MainMenu(), pygbase.Common.get_value("trans_time"), (0, 0, 0)))

	def update(self, delta: float):
		self.ui_manager.update(delta)
		self.lighting_manager.update(delta)
		self.particle_manager.update(delta)
		SoundHandler.update(delta)

		self.mouse_world_pos.update(self.camera.screen_to_world(pygame.mouse.get_pos()))

		if pygbase.InputManager.get_key_just_pressed(pygame.K_ESCAPE):
			self.back_button_handler()

	def draw(self, surface: pygame.Surface):
		surface.fill(self.background_colour)

		self.particle_manager.draw(surface, self.camera)
		self.lighting_manager.draw(surface, self.camera)

		self.ui_manager.draw(surface)
