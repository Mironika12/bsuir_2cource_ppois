import pygame as pg
import config.config as cfg

class Bullet(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: pg.Vector2):
        super().__init__()

        self.image = pg.Surface((8, 8))
        self.image.fill(cfg.RED)

        self.rect = self.image.get_rect(center=(x, y))

        self.direction = direction.normalize() if direction.length_squared() != 0 else pg.Vector2(0, 0)
        self.speed = 5

    def update(self, walls=None):
        dx = int(self.direction.x * self.speed)
        dy = int(self.direction.y * self.speed)

        self.rect.x += dx
        self.rect.y += dy

        if walls is not None and pg.sprite.spritecollide(self, walls, False):
            self.kill()