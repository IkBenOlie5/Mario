import os
import typing
from pathlib import Path

import pygame as pg
import pytmx

game_directory = Path(os.path.dirname(__file__)).parent
assets_directory = os.path.join(game_directory, "assets")
image_directory = os.path.join(assets_directory, "images")
sound_directory = os.path.join(assets_directory, "sounds")


def load_tile_map(filename: str) -> pytmx.TiledMap:
    tm = pytmx.load_pygame(os.path.join(assets_directory, filename), pixelalpha=True)
    return tm


def load_png(filename: str) -> pg.surface.Surface:
    image = pg.image.load(os.path.join(image_directory, filename))

    if image.get_alpha() is None:
        image = image.convert()
        return image
    image = image.convert_alpha()
    return image


def load_animation(directory_name: str) -> typing.Generator[pg.surface.Surface, None, None]:
    images = [
        load_png(os.path.join(image_directory, directory_name, filename))
        for filename in sorted(os.listdir(os.path.join(image_directory, directory_name)))
    ]

    while True:
        yield from iter(images)


def load_sound(filename: str) -> pg.mixer.Sound:
    return pg.mixer.Sound(os.path.join(sound_directory, filename))
