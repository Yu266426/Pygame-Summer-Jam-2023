import random
from typing import Optional

import pygame
import pygbase


class Cilium:
	def __init__(self, parent, offset: tuple, angle_offset: float = 0):
		self.parent = parent
		self.offset = pygame.Vector2(offset)

		self.pivot_point = pygame.Vector2(0, 15)

		self.pos = self.parent.pos - self.offset

		self.image: pygbase.Image = pygbase.ResourceManager.get_resource("image", "cilium")

		self._angle = random.uniform(-50, 50)
		if abs(self._angle) < 10:
			self._angle *= 5

		self.angle_offset = angle_offset

		self.switch_timer = pygbase.Timer(random.uniform(0.03, 0.05), False, True)

	@property
	def angle(self):
		return self._angle + self.parent.angle + self.angle_offset

	def update(self, delta: float):
		self.switch_timer.tick(delta)

		if self.switch_timer.done():
			self._angle *= -1

		self.pos = self.parent.pos - self.offset.rotate(-self.parent.angle)

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		# pos = self.parent.pos - self.offset.rotate(-self.parent.angle)
		image = self.image.get_image(self.angle)
		# pos = self.parent.pos

		# Local offset
		rect = image.get_rect(center=self.pos)
		offset = (-self.pivot_point).rotate(-self.angle)
		rect = rect.move(offset)

		surface.blit(image, camera.world_to_screen(rect.topleft))
