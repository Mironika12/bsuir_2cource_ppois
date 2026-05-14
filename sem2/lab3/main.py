import pygame as pg
import config.config as cfg
from logic.player import Player
from logic.map_manager import MapManager
from logic.enemy import Enemy
from logic.menu import Menu

pg.init()
# pg.mixer.init()

screen = pg.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
pg.display.set_caption("Pacman")
clock = pg.time.Clock()

menu = Menu()

level1_map = MapManager()
level1_map.load_map(r"./config/level1.json")


def restart_game():
    player = Player("Shunkevich")

    basic_sprites = pg.sprite.Group()
    basic_sprites.add(player)

    enemy1 = Enemy(
        "Enemy1",
        r"./assets/images/zhuk.png",
        30,
        30,
        behavior="random_shooter"
    )

    enemy2 = Enemy(
        "Enemy2",
        r"./assets/images/zhuk.png",
        150,
        180,
        behavior="chaser"
    )

    enemy_sprites = pg.sprite.Group()
    enemy_sprites.add(enemy1)
    enemy_sprites.add(enemy2)

    bullet_sprites = pg.sprite.Group()

    return player, basic_sprites, enemy_sprites, bullet_sprites


player, basic_sprites, enemy_sprites, bullet_sprites = restart_game()

game_state = "menu"
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if game_state == "menu":
            action = menu.handle_input(event)

            if action == "Start game":
                player, basic_sprites, enemy_sprites, bullet_sprites = restart_game()
                game_state = "game"

            elif action == "Exit":
                running = False

        elif game_state == "game_over":
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    player, basic_sprites, enemy_sprites, bullet_sprites = restart_game()
                    game_state = "game"
                elif event.key == pg.K_ESCAPE:
                    running = False

        elif game_state == "win":
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    player, basic_sprites, enemy_sprites, bullet_sprites = restart_game()
                    level1_map.load_map(r"./config/level1.json")
                    game_state = "game"

    if game_state == "menu":
        menu.draw(screen)

    elif game_state == "game":
        basic_sprites.update(level1_map.wall_group)

        enemy_sprites.update(
            level1_map.wall_group,
            player,
            bullet_sprites,
            level1_map.map_data
        )

        bullet_sprites.update(level1_map.wall_group)

        # сбор точек
        pg.sprite.spritecollide(
            player,
            level1_map.dot_group,
            True
        )

        # сбор бонусов
        bonuses = pg.sprite.spritecollide(
            player,
            level1_map.bonus_group,
            True
        )

        if bonuses:
            player.apply_bonus(level1_map.wall_group)

        if (
            not player.has_shield
            and pg.sprite.spritecollide(player, enemy_sprites, False)
        ):
            game_state = "game_over"

        if (
            not player.has_shield
            and pg.sprite.spritecollide(player, bullet_sprites, True)
        ):
            game_state = "game_over"

        if len(level1_map.dot_group) == 0:
            game_state = "win"

        screen.fill(cfg.BLACK)
        level1_map.draw(screen)

        basic_sprites.draw(screen)
        enemy_sprites.draw(screen)
        bullet_sprites.draw(screen)

    elif game_state == "game_over":
        menu.draw_game_over(screen)

    elif game_state == "win":
        menu.draw_win(screen)

    

    pg.display.flip()
    clock.tick(cfg.FPS)

pg.quit()