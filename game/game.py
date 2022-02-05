import sys

import pygame as pg

from game import constants as c
from game.camera import Camera
from game.resources import load_animation, load_png, load_sound
from game.sprites import AnimatedTile, Background, Map, Obstacle, Player


class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 2, 512)
        pg.init()
        self.screen = pg.display.set_mode(c.SIZE, pg.DOUBLEBUF)
        pg.display.set_caption(c.TITLE)
        pg.event.set_allowed([pg.QUIT, pg.KEYDOWN])
        self.clock = pg.time.Clock()

        self.sky_image = pg.transform.scale(load_png(c.SKY_FILE), (c.WIDTH, c.HEIGHT))
        self.clouds_image = pg.transform.scale(load_png(c.CLOUDS_FILE), (c.WIDTH, c.HEIGHT))
        self.idle_animation = load_animation(c.IDLE_DIR)
        self.walk_animation = load_animation(c.WALK_DIR)

        self.jump_sound = load_sound(c.JUMP_FILE)

        self.dt = 0
        self.playing = False
        self.debug = False

    def new(self):
        self.all_sprites = pg.sprite.Group()

        self.background = Background(self)
        self.map = Map(self, c.MAP_FILE)

        self.obstacles = pg.sprite.Group()
        for object_ in self.map.tiled_map.tm.objects:
            if object_.name == "player":
                self.player = Player(self, object_.x, object_.y)
            elif object_.name == "obstacle":
                Obstacle(self, object_.x, object_.y, object_.width, object_.height)
            elif object_.name == "spike":
                AnimatedTile(self, object_.x, object_.y, load_animation(c.SPIKE_DIR))
            elif object_.name == "water":
                AnimatedTile(self, object_.x, object_.y, load_animation(c.WATER_DIR))

        self.camera = Camera(self.map.tiled_map.width, self.map.tiled_map.height)

    @staticmethod
    def quit():
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.background.update()
        self.camera.update(self.player)

    def draw(self):
        self.screen.blit(self.background.image, self.background.rect)
        self.screen.blit(self.map.image, self.camera.apply(self.map.rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))
        pg.display.update()

    def run(self):
        while True:
            self.events()
            self.update()
            self.draw()
            self.dt = self.clock.tick(c.FPS) / 1000
            pg.display.set_caption(f"{c.TITLE} - FPS: {self.clock.get_fps():.2f}")

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
