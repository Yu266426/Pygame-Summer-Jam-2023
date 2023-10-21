import json
import random

import pygame
import pygbase

from data.modules.files import LEVEL_DIR, ASSET_DIR
from data.modules.menu_ciliate import MenuCiliate
from data.modules.obstacles.cyanobacterium import Cyanobacterium
from data.modules.obstacles.heliozoon import Heliozoon
from data.modules.obstacles.rotifer import Rotifer
from data.modules.sound import SoundHandler


class MainMenu(pygbase.GameState, name="main_menu"):
	def __init__(self):
		super().__init__()

		self.background_colour = pygbase.Common.get_value("background_colour")
		self.screen_size = pygame.Vector2(pygbase.Common.get_value("screen_width"), pygbase.Common.get_value("screen_height"))

		self.lighting_manager = pygbase.LightingManager(0.4)
		self.particle_manager = pygbase.ParticleManager(chunk_size=50)
		self.ui_manager = pygbase.UIManager()

		self.camera = pygbase.Camera(-self.screen_size / 2)

		self.start_levels = ["start_1.json", "start_2.json", "start_3.json", "start_4.json"]
		self.start_level = random.choice(self.start_levels)

		self.obstacles = []
		self.ciliates = []

		self.setup()

		self.ui_manager.add_element(
			pygbase.Button(
				(pygbase.UIValue(0.1, False), pygbase.UIValue(0.6, False)),
				(pygbase.UIValue(0.8, False), pygbase.UIValue(0)),
				"image", "large_button",
				self.ui_manager.base_container,
				self.to_level_selector,
				text="Play",
				text_colour=(240, 240, 240),
				font=ASSET_DIR / "fira_sans.ttf",
				use_sys=False
			)
		)

		self.ui_manager.add_element(
			pygbase.Button(
				(pygbase.UIValue(0), pygbase.UIValue(0.03, False)),
				(pygbase.UIValue(0.8, False), pygbase.UIValue(0)),
				"image", "large_button",
				self.ui_manager.base_container,
				pygbase.EventManager.post_event,
				callback_args=(pygame.QUIT,),
				text="Quit",
				text_colour=(240, 240, 240),
				font=ASSET_DIR / "fira_sans.ttf",
				use_sys=False
			),
			add_on_to_previous=(False, True),
			align_with_previous=(True, False)
		)

		SoundHandler.play_music("intro")

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

		for _ in range(random.randint(2, 6)):
			self.ciliates.append(MenuCiliate((
				random.randint(-40, 40),
				random.randint(-40, 40)
			)))

		with open(LEVEL_DIR / self.start_level) as level_file:
			data = json.load(level_file)

		for rotifer in data["obstacles"]["rotifers"]:
			self.obstacles.append(Rotifer(rotifer[0], rotifer[1], self.particle_manager))

		for heliozoon in data["obstacles"]["heliozoa"]:
			self.obstacles.append(Heliozoon(heliozoon[0], heliozoon[1]))

		for heliozoon in data["obstacles"]["cyanobacteria"]:
			self.obstacles.append(Cyanobacterium(heliozoon[0], heliozoon[1]))

	def to_level_selector(self):
		from data.modules.level_selector import LevelSelector
		self.set_next_state(pygbase.FadeTransition(self, LevelSelector(), pygbase.Common.get_value("trans_time"), (0, 0, 0)))
		SoundHandler.play_sound(random.choice(pygbase.Common.get_value("water_sounds")))

	def update(self, delta: float):
		self.ui_manager.update(delta)
		self.lighting_manager.update(delta)
		self.particle_manager.update(delta)
		SoundHandler.update(delta)

		for ciliate in self.ciliates:
			ciliate.update(delta, self.obstacles)

		for obstacle in self.obstacles:
			if isinstance(obstacle, Rotifer):
				obstacle.update(delta, [])
			else:
				obstacle.update(delta)

		if pygbase.InputManager.get_key_just_pressed(pygame.K_ESCAPE):
			pygbase.EventManager.post_event(pygame.QUIT)

	def draw(self, surface: pygame.Surface):
		surface.fill(self.background_colour)

		self.particle_manager.draw(surface, self.camera)

		for ciliate in self.ciliates:
			ciliate.draw(surface, self.camera)

		for obstacle in self.obstacles:
			obstacle.draw(surface, self.camera)

		self.lighting_manager.draw(surface, self.camera)

		self.ui_manager.draw(surface)
