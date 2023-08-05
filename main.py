import cProfile

import pygbase

from data.modules.editor import Editor
from data.modules.files import SPRITE_SHEET_DIR, IMAGE_DIR
from data.modules.game import Game
from data.modules.level_selector import LevelSelector

if __name__ == '__main__':
	pygbase.init((800, 800), max_light_radius=798, light_radius_interval=2)

	# Resources
	pygbase.add_sprite_sheet_resource("sprite_sheet", 0, SPRITE_SHEET_DIR)
	pygbase.add_image_resource("image", 1, IMAGE_DIR)

	# Settings
	pygbase.Common.set_value("background_colour", (232, 232, 232))
	pygbase.Common.set_value("available_levels", 1)
	pygbase.Common.set_value("num_levels", 3)

	pygbase.Common.add_particle_setting(
		"micro", [(195, 202, 151), (196, 159, 120)],
		(9.0, 6.0), (0.13, 0.19), (1.0, 3.0),
		(0.0, 0.0),
		True
	)

	# App
	profiler = cProfile.Profile()
	# profiler.enable()

	app = pygbase.App(LevelSelector)
	app.run()

	# profiler.disable()

	pygbase.quit()

	profiler.dump_stats("stats.prof")
