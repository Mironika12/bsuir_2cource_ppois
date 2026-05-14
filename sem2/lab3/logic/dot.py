import pygame as pg
import config.config as cfg


class Dot(pg.sprite.Sprite):

    def __init__(self, x: int, y: int):
        super().__init__()

        self.image = pg.Surface((6, 6), pg.SRCALPHA)

        pg.draw.circle(
            self.image,
            cfg.WHITE,
            (3, 3),
            3
        )

        self.rect = self.image.get_rect()

        self.rect.center = (
            x + cfg.TILE_SIZE // 2,
            y + cfg.TILE_SIZE // 2
        )