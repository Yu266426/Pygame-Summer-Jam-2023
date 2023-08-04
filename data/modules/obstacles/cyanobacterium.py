import pygame
import pygbase

from data.modules.colliders.line_collider import LineCollider


class Cyanobacterium:
	def __init__(self, pos: tuple, angle: float):
		self.starting_pos = pos
		self.starting_angle = angle

		self.pos = pygame.Vector2(pos)
		self.angle = angle

		self.image: pygbase.Image = pygbase.ResourceManager.get_resource("image", "cyanobacterium")

		self.line1 = LineCollider(self.pos + pygame.Vector2(10, 145).rotate(-self.angle), self.angle, 290)
		self.line2 = LineCollider(self.pos + pygame.Vector2(-10, 145).rotate(-self.angle), self.angle, 290)

	def update(self, delta: float):
		pass

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera, is_editor: bool = False):
		image = self.image.get_image(self.angle)

		# Local offset
		rect = image.get_rect(center=self.pos)

		surface.blit(image, camera.world_to_screen(rect.topleft))
