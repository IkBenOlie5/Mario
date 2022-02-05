import pygame as pg
import pytmx

from game.resources import load_tile_map


class TiledMap:
    def __init__(self, filename: str) -> None:
        self.tm = load_tile_map(filename)
        self.width = self.tm.width * self.tm.tilewidth
        self.height = self.tm.height * self.tm.tileheight

    def draw(self, surface: pg.Surface) -> None:
        for layer in self.tm.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tm.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self.tm.tilewidth, y * self.tm.tileheight))
