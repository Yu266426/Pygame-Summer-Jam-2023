import pygame
import pygbase

from data.modules.colliders.circle_collider import CircleCollider
from data.modules.obstacles.cyanobacterium import Cyanobacterium
from data.modules.obstacles.heliozoon import Heliozoon
from data.modules.obstacles.rotifer import Rotifer


class Player:
	def __init__(self, pos: tuple):
		self.pos = pygame.Vector2(pos)
		self.angle = 270
		self.angular_velocity = 0

		self.animation = pygbase.Animation("sprite_sheet", "ciliate", 0, 5)

		self.drag = 0.6
		self.speed = 200

		self.velocity = pygame.Vector2()

		self.input = pygame.Vector2()

		self.collider_pos_1 = self.pos + pygame.Vector2(0, 40)
		self.collider_pos_2 = self.pos + pygame.Vector2(0, -40)
		self.colliders = [
			CircleCollider(self.pos, 30).link_pos(self.pos),
			CircleCollider(self.pos, 30).link_pos(self.collider_pos_1),
			CircleCollider(self.pos, 30).link_pos(self.collider_pos_2)
		]

		self.max_health = 50
		self.health = 50
		self.heliozoa_hurt_timer = pygbase.Timer(1.5, True, False)
		self.rotifer_hurt_timer = pygbase.Timer(0.3, True, False)

		self.ended = False

	def get_inputs(self):
		self.input.x = pygbase.InputManager.get_key_pressed(pygame.K_d) - pygbase.InputManager.get_key_pressed(pygame.K_a)
		self.input.y = pygbase.InputManager.get_key_pressed(pygame.K_s) - pygbase.InputManager.get_key_pressed(pygame.K_w)

	def update_position(self, delta: float, obstacles: list):
		acceleration = self.input * self.speed
		acceleration -= self.velocity * self.drag

		self.velocity += acceleration * delta

		# X movement
		x_movement = self.velocity.x * delta + 0.5 * acceleration.x * (delta ** 2)
		self.pos.x += x_movement

		for obstacle in obstacles:
			if isinstance(obstacle, Cyanobacterium):
				if obstacle.line1.collides_with(self.colliders[0]) or obstacle.line2.collides_with(self.colliders[0]):
					self.pos.x -= x_movement
					self.velocity.x = 0

		# Y movement
		y_movement = self.velocity.y * delta + 0.5 * acceleration.y * (delta ** 2)
		self.pos.y += y_movement

		for obstacle in obstacles:
			if isinstance(obstacle, Cyanobacterium):
				if obstacle.line1.collides_with(self.colliders[0]) or obstacle.line2.collides_with(self.colliders[0]):
					self.pos.y -= y_movement
					self.velocity.y = 0

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

		self.heliozoa_hurt_timer.tick(delta)
		self.rotifer_hurt_timer.tick(delta)

		if not self.ended:
			self.get_inputs()
		else:
			self.input.update(0)

		self.update_position(delta, obstacles)
		self.update_angle(delta)

		# Damage
		if self.heliozoa_hurt_timer.done() and self.rotifer_hurt_timer.done():
			for obstacle in obstacles:
				if isinstance(obstacle, Heliozoon):
					for collider in self.colliders:
						if obstacle.collider.collides_with(collider):
							self.health -= 20
							self.heliozoa_hurt_timer.start()
							break
				if isinstance(obstacle, Rotifer):
					if self.pos.distance_to(obstacle.attract_point_1) < 40 or self.pos.distance_to(obstacle.attract_point_2) < 40:
						self.health -= 5
						self.rotifer_hurt_timer.start()
						break

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		self.animation.draw_at_pos(surface, self.pos, camera, angle=self.angle, draw_pos="center")

# for collider in self.colliders:
# 	pygame.draw.circle(surface, "red", camera.world_to_screen(collider.pos), 30)
