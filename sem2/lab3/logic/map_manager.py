import pygame as pg
import json
import config.config as cfg
from logic.wall import Wall
from logic.dot import Dot
from logic.bonus import Bonus

class MapManager:
    def __init__(self, tile_size: int = cfg.TILE_SIZE):
        self.tile_size = tile_size
        self.map_data: list[list[int]] = []
        self.wall_group = pg.sprite.Group()
        self.dot_group = pg.sprite.Group()
        self.bonus_group = pg.sprite.Group()

    def load_map(self, path: str):
        with open(path, "r") as file:
            self.map_data = json.load(file)
        
        self.wall_group.empty()
        self.dot_group.empty()
        self.bonus_group.empty()
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile == 1:
                    wall = Wall(x * self.tile_size, y * self.tile_size, self.tile_size)
                    self.wall_group.add(wall)
                elif tile == 0:
                    dot = Dot(
                        x * self.tile_size,
                        y * self.tile_size
                    )

                    self.dot_group.add(dot)
                elif tile == 2:
                    bonus = Bonus(
                        x * self.tile_size,
                        y * self.tile_size
                    )

                    self.bonus_group.add(bonus)


    def draw(self, surface: pg.Surface):
        self.wall_group.draw(surface)
        self.dot_group.draw(surface)
        self.bonus_group.draw(surface)