import json

import pygame
import pygbase

from data.modules.end_point import EndPoint
from data.modules.events import END_EVENT_TYPE, WIN_EVENT_TYPE
from data.modules.files import LEVEL_DIR
from data.modules.obstacles.cyanobacterium import Cyanobacterium
from data.modules.obstacles.heliozoon import Heliozoon
from data.modules.obstacles.rotifer import Rotifer
from data.modules.player import Player


class Level:
	def __init__(self, name: str, camera: pygbase.Camera, particle_manager: pygbase.ParticleManager, lighting_manager: pygbase.LightingManager, ui_manager: pygbase.UIManager):
		self.screen_size = pygame.Vector2(pygbase.Common.get_value("screen_width"), pygbase.Common.get_value("screen_height"))

		self.camera = camera
		self.camera_following = False

		self.particle_manager = particle_manager

		self.micro_particle_settings = pygbase.Common.get_particle_setting("micro")

		self.player = Player((0, 0))

		self.obstacles = []

		self.player_health_bar = ui_manager.add_element(
			pygbase.ProgressBar(
				(pygbase.UIValue(0.01, False), pygbase.UIValue(0.01, False)),
				(pygbase.UIValue(0.35, False), pygbase.UIValue(0.07, False)),
				1, pygbase.UIValue(5),
				(0, 255, 75, 100),
				(0, 0, 0, 40),
				ui_manager.base_container
			)
		)

		# Load level
		with open(LEVEL_DIR / f"{name}.json") as level_file:
			data = json.load(level_file)

		for rotifer in data["obstacles"]["rotifers"]:
			self.obstacles.append(Rotifer(rotifer[0], rotifer[1], self.particle_manager))

		for heliozoon in data["obstacles"]["heliozoa"]:
			self.obstacles.append(Heliozoon(heliozoon[0], heliozoon[1]))

		for heliozoon in data["obstacles"]["cyanobacteria"]:
			self.obstacles.append(Cyanobacterium(heliozoon[0], heliozoon[1]))

		self.end_point = EndPoint(data["end_pos"], particle_manager, lighting_manager)

		self.ended = False

	def end(self):
		pygbase.EventManager.post_event(END_EVENT_TYPE)
		self.ended = True
		self.player.ended = True

	@staticmethod
	def win():
		pygbase.EventManager.post_event(WIN_EVENT_TYPE)

	def update(self, delta: float):
		self.player.update(delta, self.obstacles)
		self.player_health_bar.set_fill_percent(self.player.health / self.player.max_health)

		if not self.ended and self.player.health <= 0:
			self.end()

		if self.camera_following:
			self.camera.lerp_to_target(self.player.pos - self.screen_size / 2, 2 * delta)

		if (self.player.pos - self.screen_size / 2).distance_to(self.camera.pos) < 80:
			self.camera_following = False
		elif (self.player.pos - self.screen_size / 2).distance_to(self.camera.pos) > 240:
			self.camera_following = True

		for obstacle in self.obstacles:
			if isinstance(obstacle, Rotifer):
				obstacle.update(delta, [self.player])
			else:
				obstacle.update(delta)

		if not self.ended:
			for player_collider in self.player.colliders:
				if player_collider.collides_with(self.end_point.collider):
					self.end()
					self.win()

	def draw(self, surface: pygame.Surface):
		self.player.draw(surface, self.camera)

		for obstacle in self.obstacles:
			obstacle.draw(surface, self.camera)
