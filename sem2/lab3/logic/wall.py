import pygame as pg
import config.config as cfg

class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.image = pg.Surface((size, size))
        self.image.fill(cfg.BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))