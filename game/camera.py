import pygame as pg

from game import constants as c


class Camera:
    def __init__(self, width: int, height: int) -> None:
        self.camera = pg.Rect((0, 0), (width, height))
        self.width = width
        self.height = height

    def apply(self, rect: pg.Rect) -> pg.rect.Rect:
        return rect.move(self.camera.topleft)

    def update(self, target: pg.sprite.Sprite) -> None:
        self.camera.x = max(-self.width + c.WIDTH, min(0, -target.rect.centerx + int(c.WIDTH / 2)))
        self.camera.y = max(-self.height + c.HEIGHT, min(0, -target.rect.centery + int(c.HEIGHT / 2)))
