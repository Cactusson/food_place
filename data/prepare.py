import os
import sys
import pygame as pg

from . import tools


SCREEN_SIZE = (1000, 650)
ORIGINAL_CAPTION = 'Food Place'

# pg.mixer.pre_init(44100, -16, 1, 512)
pg.init()
os.environ['SDL_VIDEO_CENTERED'] = 'TRUE'
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()

BACKGROUND_COLOR = pg.Color('#FCB241')
FILL_COLOR = pg.Color('#F7D098')
FRAME_COLOR = pg.Color('#911F27')
BUTTON_COLOR = pg.Color('#FCF0C8')


def graphics_from_directories(directories):
    """
    Calls the tools.load_all_graphics() function for all directories passed.
    """
    base_path = os.path.join("resources", "graphics")
    GFX = {}
    for directory in directories:
        if getattr(sys, 'frozen', False):
            path = os.path.join(os.path.dirname(sys.executable), 'graphics',
                                directory)
        else:
            path = os.path.join(base_path, directory)
        GFX[directory] = tools.load_all_gfx(path)
    return GFX

_SUB_DIRECTORIES = [
    'customers', 'customers_new', 'customers_simple', 'gui', 'numbers',
    'other', 'rifle', 'table', 'table_simple', 'waiter', 'waiter_new',
    'ufo']
GFX = graphics_from_directories(_SUB_DIRECTORIES)

fonts_path = os.path.join('resources', 'fonts')
FONTS = tools.load_all_fonts(fonts_path)

# sfx_path = os.path.join('resources', 'sounds')
# SFX = tools.load_all_sfx(sfx_path)

# music_path = os.path.join('resources', 'music')
# MUSIC = tools.load_all_music(music_path)
