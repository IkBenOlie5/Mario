from __future__ import annotations

import pygame as pg

from game import constants as c
from game.tile_map import TiledMap

import typing

if typing.TYPE_CHECKING:
    from game import Game


def collide_hit_rect(sprite1: pg.sprite.Sprite, sprite2: pg.sprite.Sprite) -> bool:
    return sprite1.hit_rect.colliderect(sprite2.rect)  # type: ignore


def collide_with_group(sprite: pg.sprite.Sprite, group: pg.sprite.Group, dir_: str) -> bool | None:
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:

        if dir_ == "x":
            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            elif sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0

            sprite.hit_rect.centerx = sprite.pos.x
        elif dir_ == "y":
            touching = False
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
                touching = True
            elif sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y
            return touching


class Map(pg.sprite.Sprite):
    def __init__(self, game: Game, filename: str) -> None:
        self.groups = ()
        super().__init__(*self.groups)
        self.game = game
        self.tiled_map = TiledMap(filename)
        self.image = pg.Surface((self.tiled_map.width, self.tiled_map.height), pg.SRCALPHA)
        self.tiled_map.draw(self.image)
        self.rect = self.image.get_rect()


class AnimatedTile(pg.sprite.Sprite):
    def __init__(self, game: Game, x: int, y: int, animation: typing.Generator[pg.Surface, None, None]) -> None:
        self.groups = (game.all_sprites,)
        super().__init__(*self.groups)
        self.game = game
        self.animation = animation
        self.image = next(animation)
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.timer = 0

    def update(self) -> None:
        self.timer += self.game.dt
        if self.timer > c.MAX_TILE_ANIMATION_TIMER:
            self.image = next(self.animation)
            self.timer = 0


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game: Game, x: int, y: int, w: int, h: int) -> None:
        self.groups = (game.obstacles,)
        super().__init__(*self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)


class Background(pg.sprite.Sprite):
    def __init__(self, game: Game) -> None:
        self.groups = ()
        super().__init__(*self.groups)
        self.game = game
        self.image = game.sky_image.copy()
        self.image.blit(game.clouds_image, (0, 0))
        self.rect = self.image.get_rect()
        self.clouds_x = 0

    def update(self) -> None:
        self.image.blit(self.game.sky_image, (0, 0))
        self.image.blit(self.game.clouds_image, (self.clouds_x, 0))
        self.image.blit(self.game.clouds_image, (self.clouds_x - c.WIDTH, 0))
        self.clouds_x += c.CLOUDS_SPEED * self.game.dt
        self.clouds_x %= c.WIDTH


class Player(pg.sprite.Sprite):
    def __init__(self, game: Game, x: int, y: int) -> None:
        self.groups = (game.all_sprites,)
        super().__init__(*self.groups)
        self.game = game
        self.image = next(game.idle_animation)
        self.rect = self.image.get_rect()
        self.hit_rect = pg.Rect(0, 0, c.TILE_SIZE, c.TILE_SIZE)
        self.vel = pg.math.Vector2(0, 0)
        self.pos = pg.math.Vector2(x, y)
        self.can_jump = False
        self.timer = 0
        self.direction = "right"

    def get_keys(self) -> None:
        keys = pg.key.get_pressed()
        self.vel.x = 0
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -c.WALK_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = c.WALK_SPEED
        if (keys[pg.K_UP] or keys[pg.K_w] or keys[pg.K_SPACE]) and self.can_jump:
            self.vel.y = -c.JUMP_SPEED

        if self.vel.y < c.FALL_MAX:
            self.vel.y += c.FALL_ACCEL

    def update(self) -> None:
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_group(self, self.game.obstacles, "x")
        self.hit_rect.centery = self.pos.y
        self.can_jump = collide_with_group(self, self.game.obstacles, "y")
        self.rect.center = self.hit_rect.center

        self.timer += self.game.dt
        if self.timer > c.MAX_PLAYER_ANIMATION_TIMER:
            if self.vel.x > 0:
                self.image = next(self.game.walk_animation)
                self.direction = "right"
            elif self.vel.x < 0:
                self.image = pg.transform.flip(next(self.game.walk_animation), True, False)
                self.direction = "left"
            else:
                if self.direction == "right":
                    self.image = next(self.game.idle_animation)
                else:
                    self.image = pg.transform.flip(next(self.game.idle_animation), True, False)
            self.timer = 0
