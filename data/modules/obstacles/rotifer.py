import math
import random
from typing import TYPE_CHECKING

import pygame
import pygbase

from data.modules.cilium import Cilium

if TYPE_CHECKING:
	from data.modules.player import Player


class Rotifer:
	def __init__(self, pos: tuple, angle: float, particle_manager: pygbase.ParticleManager):
		self.starting_pos = pos
		self.starting_angle = angle

		self.pos = pygame.Vector2(pos)
		self.angle = angle

		self.wave_offset = random.uniform(-10, 10)
		self.wave_amount = random.uniform(4, 6)
		self.wave_speed = random.uniform(800, 1200)

		self.animation = pygbase.Animation("sprite_sheet", "rotifer", 0, 7)
		self.animation.frame = random.randrange(0, 7)

		self.cilia = [
			Cilium(self, (-5, 120)),
			Cilium(self, (-13, 128)),
			Cilium(self, (-20, 140)),
			Cilium(self, (-30, 140)),
			Cilium(self, (-36, 140)),
			Cilium(self, (5, 120)),
			Cilium(self, (13, 128)),
			Cilium(self, (20, 140)),
			Cilium(self, (30, 140)),
			Cilium(self, (36, 140))
		]

		self.attract_point_offset_1 = pygame.Vector2(-20, 140)
		self.attract_point_offset_2 = pygame.Vector2(20, 140)
		self.affector_point_offset = pygame.Vector2(0, 140)

		self.attract_point_1 = self.pos - self.attract_point_offset_1.rotate(-self.angle)
		self.attract_point_2 = self.pos - self.attract_point_offset_2.rotate(-self.angle)

		self.affector_point = self.pos - self.affector_point_offset.rotate(-self.angle)
		self.affector = particle_manager.add_affector(
			pygbase.AffectorTypes.ATTRACTOR,
			pygbase.ParticleAttractor(self.attract_point_1, 210, 4000).link_pos(self.attract_point_1)
		)

		self.entity_attractor_scaling = 4000
		self.affect_entity_distance = 200

	def update(self, delta: float, attracted_entities: list["Player"]):
		self.animation.change_frame(random.uniform(1, 3) * delta)

		for cilium in self.cilia:
			cilium.update(delta)

		for attracted_entity in attracted_entities:
			self.attract_point_1.update(self.pos - self.attract_point_offset_1.rotate(-self.angle))
			to_player_vector_1 = self.attract_point_1 - attracted_entity.pos
			to_player_distance_1 = to_player_vector_1.length()
			to_player_vector_1.normalize_ip()

			self.attract_point_2.update(self.pos - self.attract_point_offset_2.rotate(-self.angle))
			to_player_vector_2 = self.attract_point_2 - attracted_entity.pos
			to_player_distance_2 = to_player_vector_2.length()
			to_player_vector_2.normalize_ip()

			self.affector_point.update(self.pos - self.affector_point_offset.rotate(-self.angle))

			if to_player_distance_1 < self.affect_entity_distance and to_player_distance_1 != 0:
				attracted_entity.velocity += to_player_vector_1 * (self.entity_attractor_scaling / to_player_distance_1) * delta
			if to_player_distance_2 < self.affect_entity_distance and to_player_distance_2 != 0:
				attracted_entity.velocity += to_player_vector_2 * (self.entity_attractor_scaling / to_player_distance_2) * delta

		self.angle = self.starting_angle + math.sin(pygame.time.get_ticks() / self.wave_speed + self.wave_offset) * self.wave_offset

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera, is_editor: bool = False):
		if not is_editor:
			self.animation.draw_at_pos(surface, self.pos - pygame.Vector2(0, -12), camera, angle=self.angle, pivot_point=(0, 76), draw_pos="midbottom")

			for cilium in self.cilia:
				cilium.draw(surface, camera)

		else:
			self.animation.draw_at_pos(surface, self.pos - pygame.Vector2(0, -12), camera, angle=self.angle, pivot_point=(0, 76), draw_pos="midbottom", flags=pygame.BLEND_ADD)

# pygame.draw.circle(surface, "red", camera.world_to_screen(self.attract_point_1), 5)
# pygame.draw.circle(surface, "red", camera.world_to_screen(self.attract_point_2), 5)
# pygame.draw.circle(surface, "orange", camera.world_to_screen(self.affector_point), 5)
