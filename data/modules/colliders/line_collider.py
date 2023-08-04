import math

import pygame
import pygbase


class LineCollider:
	def __init__(self, start_pos: pygame.Vector2 | tuple[float, float], angle: float, length: float, start_offset: float = 0):
		self.start_pos: pygame.Vector2 = pygame.Vector2(start_pos)
		self.angle: float = angle
		self.length: float = length
		self.offset = start_offset

		self.line = pygame.Vector2(0, -self.length).rotate(-self.angle)

	def link_pos(self, pos: pygame.Vector2) -> "LineCollider":
		self.start_pos = pos
		return self

	def set_angle(self, new_angle: float):
		self.angle = new_angle
		self.line = pygame.Vector2(0, -self.length).rotate(-self.angle)

	def change_angle(self, amount: float):
		self.angle -= amount
		self.line = pygame.Vector2(0, -self.length).rotate(-self.angle)

	@property
	def end_pos(self):
		return self.start_pos + self.line

	def get_range(self) -> tuple[tuple[float, float], tuple[float, float]]:
		quadrant = math.floor((self.angle % 360) / 90) + 1

		end_pos = self.end_pos

		if quadrant == 1:
			x_range = self.start_pos.x, end_pos.x
			y_range = self.start_pos.y, end_pos.y
		elif quadrant == 2:
			x_range = end_pos.x, self.start_pos.x
			y_range = self.start_pos.y, end_pos.y
		elif quadrant == 3:
			x_range = end_pos.x, self.start_pos.x
			y_range = end_pos.y, self.start_pos.y
		else:  # Quadrant 4
			x_range = self.start_pos.x, end_pos.x
			y_range = end_pos.y, self.start_pos.y

		return x_range, y_range

	def point_within_line_segment(self, point: pygame.Vector2) -> bool:
		"""
		Detects if a point **already on** the line is within the line segment
		"""

		dist_1 = self.start_pos.distance_to(point)
		dist_2 = self.end_pos.distance_to(point)

		return self.length - 0.05 < dist_1 + dist_2 < self.length + 0.05

	def line_collide(self, line) -> bool:
		my_start = self.start_pos + self.line.normalize() * self.offset
		my_end = self.end_pos

		other_start = line.start_pos
		other_end = line.end_pos

		# Cross Product Method (ChatGPT, make more clear in future)
		dir_1 = (other_end.x - other_start.x) * (my_start.y - other_start.y) - (other_end.y - other_start.y) * (my_start.x - other_start.x)
		dir_2 = (other_end.x - other_start.x) * (my_end.y - other_start.y) - (other_end.y - other_start.y) * (my_end.x - other_start.x)
		dir_3 = (my_end.x - my_start.x) * (other_start.y - my_start.y) - (my_end.y - my_start.y) * (other_start.x - my_start.x)
		dir_4 = (my_end.x - my_start.x) * (other_end.y - my_start.y) - (my_end.y - my_start.y) * (other_end.x - my_start.x)

		return (dir_1 > 0 > dir_2 or dir_1 < 0 < dir_2) and (dir_3 > 0 > dir_4 or dir_3 < 0 < dir_4)

	def collides_with(self, collider) -> bool:
		from data.modules.colliders.circle_collider import CircleCollider

		if isinstance(collider, LineCollider):
			return self.line_collide(collider)

		elif isinstance(collider, CircleCollider):
			if self.start_pos.distance_to(collider.pos) < collider.radius:
				return True
			if self.end_pos.distance_to(collider.pos) < collider.radius:
				return True

			dot = ((collider.pos.x - self.start_pos.x) * (self.end_pos.x - self.start_pos.x) + (collider.pos.y - self.start_pos.y) * (self.end_pos.y - self.start_pos.y)) / self.length ** 2

			closest_point = pygame.Vector2(
				self.start_pos.x + dot * (self.end_pos.x - self.start_pos.x),
				self.start_pos.y + dot * (self.end_pos.y - self.start_pos.y)
			)

			if not self.point_within_line_segment(closest_point):
				return False

			return closest_point.distance_to(collider.pos) < collider.radius

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera):
		pygame.draw.line(screen, "yellow", camera.world_to_screen(self.start_pos + self.line.normalize() * self.offset), camera.world_to_screen(self.start_pos + self.line), width=4)
