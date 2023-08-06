import cProfile
import json

import pygbase

from data.modules.editor import Editor
from data.modules.files import SPRITE_SHEET_DIR, IMAGE_DIR, DATA_DIR, SOUND_DIR
from data.modules.main_menu import MainMenu

if __name__ == '__main__':
	pygbase.init((800, 800), max_light_radius=798, light_radius_interval=2)

	# Resources
	pygbase.add_sprite_sheet_resource("sprite_sheet", 0, SPRITE_SHEET_DIR)
	pygbase.add_image_resource("image", 1, IMAGE_DIR)
	pygbase.add_sound_resource("sound", 2, SOUND_DIR, sound_ending=".wav")

	# Save data
	save_path = DATA_DIR / "save.json"
	available_levels = 1
	if not save_path.is_file():
		with open(save_path, "x") as save_file:
			data = {
				"available_levels": 1,
				"completed": False
			}

			save_file.write(json.dumps(data))
	else:
		with open(save_path) as save_file:
			data = json.load(save_file)

			# Clamp between 1 and 6
			available_levels = min(max(data["available_levels"], 1), 6)

	# Settings
	pygbase.Common.set_value("background_colour", (232, 232, 232))
	pygbase.Common.set_value("trans_time", 0.5)
	pygbase.Common.set_value("available_levels", available_levels)
	pygbase.Common.set_value("num_levels", 6)
	pygbase.Common.set_value("water_sounds", (
		"water_1", "water_2", "water_3", "water_4", "water_5", "water_6", "water_7"
	))

	pygbase.Common.add_particle_setting(
		"micro", [(195, 202, 151), (196, 159, 120)],
		(9.0, 6.0), (0.13, 0.19), (1.0, 3.0),
		(0.0, 0.0),
		True
	)

	# App
	profiler = cProfile.Profile()
	# profiler.enable()

	app = pygbase.App(MainMenu)
	app.run()

	# profiler.disable()

	pygbase.quit()

	profiler.dump_stats("stats.prof")
