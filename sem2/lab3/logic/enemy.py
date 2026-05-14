import random
from collections import deque
import pygame as pg
import config.config as cfg
from logic.bullet import Bullet

class Enemy(pg.sprite.Sprite):
    def __init__(self, name: str, skin_path: str, x: int = 0, y: int = 0,
                 behavior: str = "random_shooter", shoot_cooldown: int = 1500):
        super().__init__()

        if not isinstance(name, str):
            raise TypeError("Имя не является строкой.")
        self.name = name

        if not isinstance(skin_path, str):
            raise TypeError("Переданный путь не является строкой.")

        self.image = pg.image.load(skin_path)
        self.image = pg.transform.scale(self.image, cfg.ENTITY_SIZE)
        self.rect = self.image.get_rect()

        self.rect.centerx = (
            (x // cfg.TILE_SIZE) * cfg.TILE_SIZE
            + cfg.TILE_SIZE // 2
        )

        self.rect.centery = (
            (y // cfg.TILE_SIZE) * cfg.TILE_SIZE
            + cfg.TILE_SIZE // 2
        )

        self.direction = pg.Vector2(1, 0)
        self.speed = 2

        self.behavior = behavior
        self.shoot_cooldown = shoot_cooldown
        self.last_shot_time = 0

    def update(
        self,
        walls=None,
        player=None,
        bullets=None,
        map_data=None
    ):
        if self.behavior == "chaser":
            self._chase_player(map_data, walls, player)
        else:
            self._random_move(walls)

        self._move(walls)

        if self.behavior == "random_shooter":
            self._shoot(player, bullets)

    def _move(self, walls):
        dx = int(self.direction.x * self.speed)
        dy = int(self.direction.y * self.speed)

        test_rect = self.rect.copy()
        test_rect.x += dx
        test_rect.y += dy

        if walls is not None:
            for wall in walls:
                if test_rect.colliderect(wall.rect):
                    return

        self.rect = test_rect
        self._center_in_tunnel()

    def _is_centered(self):
        center_x = (
            (self.rect.centerx // cfg.TILE_SIZE) * cfg.TILE_SIZE
            + cfg.TILE_SIZE // 2
        )
        center_y = (
            (self.rect.centery // cfg.TILE_SIZE) * cfg.TILE_SIZE
            + cfg.TILE_SIZE // 2
        )
        return (
            abs(self.rect.centerx - center_x) <= self.speed
            and abs(self.rect.centery - center_y) <= self.speed
        )

    def _get_possible_directions(self, walls):
        directions = [
            pg.Vector2(1, 0),
            pg.Vector2(-1, 0),
            pg.Vector2(0, 1),
            pg.Vector2(0, -1),
        ]

        possible = []

        for direction in directions:
            test_rect = self.rect.copy()
            test_rect.x += int(direction.x * self.speed)
            test_rect.y += int(direction.y * self.speed)

            blocked = False
            if walls is not None:
                for wall in walls:
                    if test_rect.colliderect(wall.rect):
                        blocked = True
                        break

            if not blocked:
                possible.append(direction)

        return possible

    def _random_move(self, walls):
        possible = self._get_possible_directions(walls)

        if not possible:
            return

        if self.direction in possible and random.randint(0, 20) != 0:
            return

        opposite = pg.Vector2(-self.direction.x, -self.direction.y)

        filtered = [d for d in possible if d != opposite]

        if filtered:
            self.direction = random.choice(filtered)
        else:
            self.direction = random.choice(possible)

    def _chase_player(self, map_data, walls, player):
        if player is None or map_data is None:
            return

        if not self._is_centered():
            return

        start = (self.rect.centerx // cfg.TILE_SIZE, self.rect.centery // cfg.TILE_SIZE)

        target = (player.rect.centerx // cfg.TILE_SIZE, player.rect.centery // cfg.TILE_SIZE)

        queue = deque([start])

        visited = {start: None}

        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]

        while queue:
            current = queue.popleft()

            if current == target:
                break

            for dx, dy in directions:
                nx = current[0] + dx
                ny = current[1] + dy

                if (
                    ny < 0
                    or ny >= len(map_data)
                    or nx < 0
                    or nx >= len(map_data[0])
                ):
                    continue

                if map_data[ny][nx] == 1:
                    continue

                neighbor = (nx, ny)

                if neighbor not in visited:

                    queue.append(neighbor)
                    visited[neighbor] = current

        if target not in visited:
            return

        path = []
        current = target

        while current is not None:
            path.append(current)
            current = visited[current]

        path.reverse()

        if len(path) < 2:
            possible = self._get_possible_directions(walls)

            if possible:
                opposite = pg.Vector2(
                    -self.direction.x,
                    -self.direction.y
                )

                filtered = [
                    d for d in possible
                    if d != opposite
                ]

                if filtered:
                    self.direction = random.choice(filtered)
                else:
                    self.direction = random.choice(possible)
            return

        next_cell = path[1]
        dx = next_cell[0] - start[0]
        dy = next_cell[1] - start[1]

        self.direction = pg.Vector2(dx, dy)

    def _shoot(self, player, bullets):
        if player is None or bullets is None:
            return

        current_time = pg.time.get_ticks()
        if current_time - self.last_shot_time < self.shoot_cooldown:
            return

        direction = pg.Vector2(
            player.rect.centerx - self.rect.centerx,
            player.rect.centery - self.rect.centery
        )

        if direction.length_squared() == 0:
            return

        bullet = Bullet(self.rect.centerx, self.rect.centery, direction)
        bullets.add(bullet)
        self.last_shot_time = current_time

    def _center_in_tunnel(self):
        if self.direction.x != 0:

            target_y = (
                (self.rect.centery // cfg.TILE_SIZE)
                * cfg.TILE_SIZE
                + cfg.TILE_SIZE // 2
            )

            diff = target_y - self.rect.centery

            if abs(diff) <= 1:
                self.rect.centery = target_y
            else:
                self.rect.y += 1 if diff > 0 else -1

        elif self.direction.y != 0:

            target_x = (
                (self.rect.centerx // cfg.TILE_SIZE)
                * cfg.TILE_SIZE
                + cfg.TILE_SIZE // 2
            )

            diff = target_x - self.rect.centerx

            if abs(diff) <= 1:
                self.rect.centerx = target_x
            else:
                self.rect.x += 1 if diff > 0 else -1