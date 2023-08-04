import os.path
import pathlib
import sys

CURRENT_DIR = pathlib.Path(os.path.dirname(os.path.realpath(sys.argv[0])))
DATA_DIR = CURRENT_DIR / "data"

ASSET_DIR = DATA_DIR / "assets"
IMAGE_DIR = ASSET_DIR / "images"
SPRITE_SHEET_DIR = ASSET_DIR / "sprite_sheets"

LEVEL_DIR = ASSET_DIR / "levels"
