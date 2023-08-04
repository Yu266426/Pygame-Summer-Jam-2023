import random

import pygame
import pygbase

from data.modules.colliders.circle_collider import CircleCollider


class Axopod:
	def __init__(self, parent: "Heliozoon", offset: tuple | pygame.Vector2, angle: float):
		self.parent = parent
		self.offset = pygame.Vector2(offset)

		self.pivot_point = pygame.Vector2(0, 15)

		self.pos = self.parent.pos - self.offset

		self.image: pygbase.Image = pygbase.ResourceManager.get_resource("image", "axopod")

		self._angle = -angle + 90 + random.uniform(-10, 10)

	@property
	def angle(self):
		return self._angle + self.parent.angle

	def update(self, delta: float):
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


class Heliozoon:
	def __init__(self, pos: tuple, angle: float):
		self.starting_pos = pos
		self.starting_angle = angle

		self.pos = pygame.Vector2(pos)
		self.angle = angle

		self.animation = pygbase.Animation("sprite_sheet", "heliozoon", 0, 4)

		self.axopodia: list[Axopod] = []
		for _ in range(random.randint(9, 16)):
			axopod_angle = random.uniform(0, 360)
			self.axopodia.append(
				Axopod(self, pygame.Vector2(43, 0).rotate(axopod_angle), axopod_angle)
			)

		self.angular_velocity = random.uniform(-1, 1)

		self.collider = CircleCollider(self.pos, 70)

	def update(self, delta: float):
		self.animation.change_frame(2 * delta)

		self.angular_velocity += random.uniform(-20, 20) * delta
		if abs(self.angular_velocity) > 5:
			self.angular_velocity -= self.angular_velocity * 5 * delta

		self.angle += self.angular_velocity

		for axopod in self.axopodia:
			axopod.update(delta)

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera, is_editor: bool = False):
		if not is_editor:
			self.animation.draw_at_pos(surface, self.pos, camera, angle=self.angle, draw_pos="center")

			for axopod in self.axopodia:
				axopod.draw(surface, camera)

		# pygame.draw.circle(surface, "red", camera.world_to_screen(self.pos), 70)
		else:
			self.animation.draw_at_pos(surface, self.pos, camera, angle=self.angle, draw_pos="center", flags=pygame.BLEND_ADD)
