import os
import typing
from pathlib import Path

import pygame as pg
import pytmx

game_folder = Path(os.path.dirname(__file__)).parent
assets_folder = os.path.join(game_folder, "assets")
image_folder = os.path.join(assets_folder, "images")


def load_tile_map(filename: str) -> pytmx.TiledMap:
    tm = pytmx.load_pygame(os.path.join(assets_folder, filename), pixelalpha=True)
    return tm


def load_png(filename: str) -> pg.surface.Surface:
    image = pg.image.load(os.path.join(image_folder, filename))
    


    if image.get_alpha() is None:
        image = image.convert()
        return image
    image = image.convert_alpha()
    return image


def load_animation(directory_name: str) -> typing.Generator[pg.surface.Surface, None, None]:
    images = [
        load_png(os.path.join(image_folder, directory_name, filename))
        for filename in sorted(os.listdir(os.path.join(image_folder, directory_name)))
    ]

    while True:
        yield from iter(images)
