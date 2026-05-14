import pygame as pg
import config.config as cfg
import random

class Player(pg.sprite.Sprite):
    def __init__(self, name: str, *groups):
        super().__init__(*groups)

        self.name = name

        self.image = pg.image.load(cfg.PLAYER_PICTURE_PATH)
        self.image = pg.transform.scale(self.image, cfg.ENTITY_SIZE)
        self.rect = self.image.get_rect()

        self.rect.x = cfg.WIDTH // 2
        self.rect.y = cfg.HEIGHT // 2

        self.rect.centerx = (
            (cfg.WIDTH // 2 // cfg.TILE_SIZE)
            * cfg.TILE_SIZE
            + cfg.TILE_SIZE // 2
        )

        self.rect.centery = (
            (cfg.HEIGHT // 2 // cfg.TILE_SIZE)
            * cfg.TILE_SIZE
            + cfg.TILE_SIZE // 2
        )

        self.current_dir = pg.Vector2(0, 0)
        self.next_dir = pg.Vector2(0, 0)

        self.speed = 2
        self.turn_tolerance = 4

        self.base_speed = 2
        self.speed = self.base_speed

        self.has_shield = False

        self.speed_effect_end = 0
        self.shield_effect_end = 0

    def update(self, walls):
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.next_dir = pg.Vector2(-1, 0)
        elif keys[pg.K_RIGHT]:
            self.next_dir = pg.Vector2(1, 0)
        elif keys[pg.K_UP]:
            self.next_dir = pg.Vector2(0, -1)
        elif keys[pg.K_DOWN]:
            self.next_dir = pg.Vector2(0, 1)

        if self.can_turn(walls):
            self.current_dir = self.next_dir

        current_time = pg.time.get_ticks()

        # конец ускорения
        if (
            self.speed != self.base_speed
            and current_time > self.speed_effect_end
        ):
            self.speed = self.base_speed

        # конец щита
        if (
            self.has_shield
            and current_time > self.shield_effect_end
        ):
            self.has_shield = False

        self.move(self.current_dir.x * self.speed, self.current_dir.y * self.speed, walls)
        self.center_in_tunnel()

    def move(self, dx, dy, walls):
        dx = int(dx)
        dy = int(dy)

        test_rect = self.rect.copy()
        test_rect.x += dx
        test_rect.y += dy

        for wall in walls:
            if test_rect.colliderect(wall.rect):
                return

        self.rect = test_rect

    def can_turn(self, walls):
        test_rect = self.rect.copy()
        test_rect.x += int(self.next_dir.x * self.speed)
        test_rect.y += int(self.next_dir.y * self.speed)

        for wall in walls:
            if test_rect.colliderect(wall.rect):
                return False

        if self.next_dir.x != 0:
            center_y = (
                (self.rect.centery // cfg.TILE_SIZE) * cfg.TILE_SIZE
                + cfg.TILE_SIZE // 2
            )
            if abs(self.rect.centery - center_y) > self.turn_tolerance:
                return False

        elif self.next_dir.y != 0:
            center_x = (
                (self.rect.centerx // cfg.TILE_SIZE) * cfg.TILE_SIZE
                + cfg.TILE_SIZE // 2
            )
            if abs(self.rect.centerx - center_x) > self.turn_tolerance:
                return False

        return True

    def center_in_tunnel(self):
        if self.current_dir.x != 0:
            center_y = (
                (self.rect.centery // cfg.TILE_SIZE) * cfg.TILE_SIZE
                + cfg.TILE_SIZE // 2
            )
            self.rect.centery = center_y

        elif self.current_dir.y != 0:
            center_x = (
                (self.rect.centerx // cfg.TILE_SIZE) * cfg.TILE_SIZE
                + cfg.TILE_SIZE // 2
            )
            self.rect.centerx = center_x

    def apply_bonus(self, walls):
        effect = random.choice([
            "speed",
            "teleport",
            "shield"
        ])

        current_time = pg.time.get_ticks()

        # ================= SPEED =================

        if effect == "speed":

            self.speed = 4
            self.speed_effect_end = current_time + 5000

            print("SPEED BOOST")

        # ================= TELEPORT =================

        elif effect == "teleport":

            free_positions = []

            for y in range(cfg.MAP_SIZE):

                for x in range(cfg.MAP_SIZE):

                    cell_rect = pg.Rect(
                        x * cfg.TILE_SIZE,
                        y * cfg.TILE_SIZE,
                        cfg.TILE_SIZE,
                        cfg.TILE_SIZE
                    )

                    collision = False

                    for wall in walls:

                        if cell_rect.colliderect(wall.rect):
                            collision = True
                            break

                    if not collision:
                        free_positions.append((x, y))

            if free_positions:

                x, y = random.choice(free_positions)

                self.rect.centerx = (
                    x * cfg.TILE_SIZE
                    + cfg.TILE_SIZE // 2
                )

                self.rect.centery = (
                    y * cfg.TILE_SIZE
                    + cfg.TILE_SIZE // 2
                )

            print("TELEPORT")

        # ================= SHIELD =================

        elif effect == "shield":

            self.has_shield = True
            self.shield_effect_end = current_time + 30000

            print("SHIELD")