import json
import logging
from typing import Callable, Any

import pygame
import pygbase

from data.modules.files import LEVEL_DIR
from data.modules.obstacles.cyanobacterium import Cyanobacterium
from data.modules.obstacles.heliozoon import Heliozoon
from data.modules.obstacles.rotifer import Rotifer
from data.modules.player import Player


class Editor(pygbase.GameState, name="editor"):
	def __init__(self):
		super().__init__()

		self.level_name = "test"

		self.background_colour = pygbase.Common.get_value("background_colour")
		self.screen_size = pygame.Vector2(pygbase.Common.get_value("screen_width"), pygbase.Common.get_value("screen_height"))

		self.particle_manager = pygbase.ParticleManager()

		self.camera_controller = pygbase.CameraController(pos=-self.screen_size / 2)

		self.obstacles = []

		if (LEVEL_DIR / f"{self.level_name}.json").is_file():
			with open(self.file_path) as level_file:
				data = json.load(level_file)

			for rotifer in data["obstacles"]["rotifers"]:
				self.obstacles.append(Rotifer(rotifer[0], rotifer[1], self.particle_manager))

			for heliozoon in data["obstacles"]["heliozoa"]:
				self.obstacles.append(Heliozoon(heliozoon[0], heliozoon[1]))

			for heliozoon in data["obstacles"]["cyanobacteria"]:
				self.obstacles.append(Cyanobacterium(heliozoon[0], heliozoon[1]))

		self.selected_object = 0
		self.selection_results: list[Callable[..., Any]] = [
			Rotifer,
			Heliozoon,
			Cyanobacterium
		]

		self.place_angle = 0

		self.ui = pygbase.UIManager()
		self.selection_text = self.ui.add_element(
			pygbase.TextElement(
				(pygbase.UIValue(0.99, False), pygbase.UIValue(0.01, False)),
				"arial", pygbase.UIValue(0.06, False), "black", str(self.selected_object),
				self.ui.base_container,
				anchor=pygbase.UIAnchors.TOP_RIGHT
			)
		)

		self.angle_text = self.ui.add_element(
			pygbase.TextElement(
				(pygbase.UIValue(0.01, False), pygbase.UIValue(0.01, False)),
				"arial", pygbase.UIValue(0.06, False), "black", str(self.place_angle),
				self.ui.base_container,
				anchor=pygbase.UIAnchors.TOP_LEFT
			)
		)

	@property
	def file_path(self):
		return LEVEL_DIR / f"{self.level_name}.json"

	def update_selected_object(self):
		if pygbase.InputManager.get_key_just_pressed(pygame.K_1):
			self.selected_object = 0
		if pygbase.InputManager.get_key_just_pressed(pygame.K_2):
			self.selected_object = 1
		if pygbase.InputManager.get_key_just_pressed(pygame.K_3):
			self.selected_object = 2

		self.selection_text.set_text(str(self.selected_object + 1))

	def update_angle(self):
		self.place_angle += pygbase.InputManager.get_scroll_y()
		self.place_angle %= 360

		self.angle_text.set_text(str(self.place_angle))

	def save(self):
		data = {
			"obstacles": {
				"rotifers": [],
				"heliozoa": [],
				"cyanobacteria": []
			},
			"player": [0, 0]
		}

		for obstacle in self.obstacles:
			if isinstance(obstacle, Rotifer):
				data["obstacles"]["rotifers"].append((obstacle.starting_pos, obstacle.starting_angle))
			if isinstance(obstacle, Heliozoon):
				data["obstacles"]["heliozoa"].append((obstacle.starting_pos, obstacle.starting_angle))
			if isinstance(obstacle, Cyanobacterium):
				data["obstacles"]["cyanobacteria"].append((obstacle.starting_pos, obstacle.starting_angle))

		with open(self.file_path, "w") as level_file:
			level_file.write(json.dumps(data))

		logging.info("Saving Level")

	def update(self, delta: float):
		self.ui.update(delta)

		self.camera_controller.update(delta)

		self.update_selected_object()
		self.update_angle()

		for obstacle in self.obstacles:
			if isinstance(obstacle, Rotifer):
				obstacle.update(delta, Player((0, 0)))
			else:
				obstacle.update(delta)

		if pygbase.InputManager.get_mouse_just_pressed(0):
			spawn_pos = self.camera_controller.camera.screen_to_world(pygame.mouse.get_pos())
			if self.selection_results[self.selected_object] == Rotifer:
				self.obstacles.append(
					self.selection_results[self.selected_object](
						(spawn_pos.x, spawn_pos.y),
						self.place_angle,
						self.particle_manager
					)
				)
			else:
				self.obstacles.append(
					self.selection_results[self.selected_object](
						(spawn_pos.x, spawn_pos.y),
						self.place_angle
					)
				)

		if pygbase.InputManager.check_modifiers(pygame.KMOD_CTRL) and pygbase.InputManager.get_key_just_pressed(pygame.K_s):
			self.save()

		# Quit
		if pygbase.InputManager.get_key_just_pressed(pygame.K_ESCAPE):
			pygbase.EventManager.post_event(pygame.QUIT)

	def draw(self, surface: pygame.Surface):
		surface.fill(self.background_colour)

		pygame.draw.circle(surface, "blue", self.camera_controller.camera.world_to_screen((0, 0)), 5)

		for obstacle in self.obstacles:
			obstacle.draw(surface, self.camera_controller.camera)

		self.selection_results[self.selected_object](
			self.camera_controller.camera.screen_to_world(pygame.mouse.get_pos()),
			self.place_angle
		).draw(surface, self.camera_controller.camera, is_editor=True)

		self.ui.draw(surface)
