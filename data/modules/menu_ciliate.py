import random

import pygame
import pygbase

from data.modules.cilium import Cilium
from data.modules.colliders.circle_collider import CircleCollider
from data.modules.obstacles.cyanobacterium import Cyanobacterium


class MenuCiliate:
	def __init__(self, pos: tuple):
		self.pos = pygame.Vector2(pos)
		self.angle = random.uniform(0, 360)
		self.angular_velocity = 0

		self.animation = pygbase.Animation("sprite_sheet", "ciliate", 0, 5)

		self.drag = 0
		self.speed = random.randint(100, 140)

		self.velocity = pygame.Vector2(0, -self.speed).rotate(-self.angle)
		self.bounce = 1

		self.collider_pos_1 = self.pos + pygame.Vector2(0, 40)
		self.collider_pos_2 = self.pos + pygame.Vector2(0, -40)
		self.colliders = [
			CircleCollider(self.pos, 30).link_pos(self.pos),
			CircleCollider(self.pos, 30).link_pos(self.collider_pos_1),
			CircleCollider(self.pos, 30).link_pos(self.collider_pos_2)
		]

		self.cilia = [
			Cilium(self, (0, -73), angle_offset=180),
			Cilium(self, (0, -72), angle_offset=175),
			Cilium(self, (0, -72), angle_offset=185)
		]

	def update_position(self, delta: float, obstacles: list):
		# X movement
		x_movement = self.velocity.x * delta
		self.pos.x += x_movement

		for obstacle in obstacles:
			if isinstance(obstacle, Cyanobacterium):
				if obstacle.line1.collides_with(self.colliders[0]) or obstacle.line2.collides_with(self.colliders[0]):
					self.pos.x -= x_movement
					self.velocity.x *= -self.bounce

		# Y movement
		y_movement = self.velocity.y * delta
		self.pos.y += y_movement

		for obstacle in obstacles:
			if isinstance(obstacle, Cyanobacterium):
				if obstacle.line1.collides_with(self.colliders[0]) or obstacle.line2.collides_with(self.colliders[0]):
					self.pos.y -= y_movement
					self.velocity.y *= -self.bounce

	def update_angle(self, delta: float):
		velocity_angle = self.velocity.angle_to((0, -1)) % 360
		angle_diff_1 = velocity_angle - self.angle
		angle_diff_2 = velocity_angle + 360 - self.angle
		angle_diff_3 = velocity_angle - 360 - self.angle

		min_diff = min(abs(angle_diff_1), abs(angle_diff_2), abs(angle_diff_3))

		if min_diff == abs(angle_diff_1):
			self.angular_velocity += angle_diff_1 * 5 * delta
		elif min_diff == abs(angle_diff_2):
			self.angular_velocity += angle_diff_2 * 5 * delta
		elif min_diff == abs(angle_diff_3):
			self.angular_velocity += angle_diff_3 * 5 * delta

		self.angular_velocity -= self.angular_velocity * 0.9 * delta
		self.angle += self.angular_velocity * delta
		self.angle %= 360

	def update(self, delta: float, obstacles: list):
		self.animation.change_frame(2 * delta)
		self.collider_pos_1.update(self.pos + pygame.Vector2(0, 40).rotate(-self.angle))
		self.collider_pos_2.update(self.pos + pygame.Vector2(0, -40).rotate(-self.angle))

		self.update_position(delta, obstacles)
		self.update_angle(delta)

		for cilium in self.cilia:
			cilium.update(delta)

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		self.animation.draw_at_pos(surface, self.pos, camera, angle=self.angle, draw_pos="center")

		for cilium in self.cilia:
			cilium.draw(surface, camera)
