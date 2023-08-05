import pygame
import pygbase

from data.modules.colliders.circle_collider import CircleCollider


class EndPoint:
	def __init__(self, pos: tuple | pygame.Vector2, particle_manager: pygbase.ParticleManager, lighting_manager: pygbase.LightingManager):
		self.pos = pygame.Vector2(pos)

		self.radius = 50

		self.collider = CircleCollider(self.pos, self.radius).link_pos(self.pos)

		self.particle_spawner = particle_manager.add_spawner(
			pygbase.CircleSpawner(
				self.pos,
				0.6, 1, self.radius,
				True,
				"micro",
				particle_manager
			).link_pos(self.pos)
		)

		self.light = lighting_manager.add_light(
			pygbase.Light(
				self.pos,
				0.4, self.radius * 1.4, self.radius * 0.2, 2
			)
		)

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera, is_editor: bool = False):
		if is_editor:
			pygame.draw.circle(surface, "blue", camera.world_to_screen(self.pos), 50, width=3)
