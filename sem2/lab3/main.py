import pygame as pg
import config.config as cfg
from logic.player import Player
from logic.map_manager import MapManager
from logic.enemy import Enemy
from logic.menu import Menu
from logic.record_manager import RecordManager

def play_music(path, loop=-1, volume=0.5):
    """Запуск музыки"""
    pg.mixer.music.stop()
    pg.mixer.music.load(path)
    pg.mixer.music.set_volume(volume)
    pg.mixer.music.play(loop)
    

def start_new_game():
    """Создаёт нового игрока, врагов и группы спрайтов"""
    player = Player("Shunkevich")
    basic_sprites = pg.sprite.Group(player)

    enemy1 = Enemy("Enemy1", r"./assets/images/zhuk.png", 30, 30, behavior="random_shooter")
    enemy2 = Enemy("Enemy2", r"./assets/images/zhuk.png", 150, 150, behavior="chaser")
    enemy_sprites = pg.sprite.Group(enemy1, enemy2)

    bullet_sprites = pg.sprite.Group()
    return player, basic_sprites, enemy_sprites, bullet_sprites

def handle_menu_events(event, menu):
    """Обработка событий в меню"""
    if event.type != pg.KEYDOWN:
        return None, None
    action = menu.handle_input(event)
    if action == "Start game":
        return start_new_game(), "game"
    elif action == "Exit":
        return None, "quit"
    elif action == "Records":
        return None, "records"
    elif action == "Help":
        return None, "help"
    return None, None

def handle_game_over_events(event):
    """Обработка событий после смерти или победы"""
    if event.type != pg.KEYDOWN:
        return None, None
    if event.key == pg.K_RETURN:
        return start_new_game(), "game"
    elif event.key == pg.K_ESCAPE:
        return None, "quit"
    return None, None

def main():
    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
    pg.display.set_caption("Pacman")
    clock = pg.time.Clock()
    menu = Menu()
    record_manager = RecordManager()

    # музыка меню
    play_music(cfg.MENU_MUSIC_PATH)

    collision_sound = pg.mixer.Sound(cfg.COLLISION_SOUND_PATH)
    bonus_sound = pg.mixer.Sound(cfg.BONUS_SOUND_PATH)

    player, basic_sprites, enemy_sprites, bullet_sprites = start_new_game()
    level1_map = MapManager()
    level1_map.load_map(cfg.LEVEL1_MAP_PATH)

    game_state = "menu"
    record_name = ""
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            # --- MENU ---
            if game_state == "menu":
                res, state = handle_menu_events(event, menu)

                if state == "quit":
                    running = False
                elif state == "records":
                    game_state = "records"
                elif state == "help":
                    game_state = "help"
                elif res:
                    player, basic_sprites, enemy_sprites, bullet_sprites = res
                    game_state = state
                    if game_state == "game":
                        play_music(cfg.GAME_MUSIC_PATH)

            # --- GAME ---
            elif game_state == "game":
                # Обработка restart / exit из клавиатуры
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        game_state = "menu"

            # --- GAME OVER / WIN ---
            elif game_state in ("game_over", "win"):
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        player, basic_sprites, enemy_sprites, bullet_sprites = start_new_game()
                        game_state = "game"
                        play_music(cfg.GAME_MUSIC_PATH)
                    elif event.key == pg.K_ESCAPE:
                        running = False

            # --- NEW RECORD ---
            elif game_state == "new_record":
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        if record_name.strip():
                            record_manager.add_record(record_name, player.score)
                            record_name = ""
                            game_state = "game_over"
                    elif event.key == pg.K_BACKSPACE:
                        record_name = record_name[:-1]
                    else:
                        if len(record_name) < 15:
                            record_name += event.unicode

            # --- RECORDS SCREEN ---
            elif game_state == "records":
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        game_state = "menu"

            elif game_state == "help":
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        game_state = "menu"

        # Обновление игры
        if game_state == "game":
            basic_sprites.update(level1_map.wall_group)
            enemy_sprites.update(level1_map.wall_group, player, bullet_sprites, level1_map.map_data)
            bullet_sprites.update(level1_map.wall_group)

            # сбор точек и бонусов
            dots = pg.sprite.spritecollide(player, level1_map.dot_group, True)
            player.score += len(dots) * 10

            bonuses = pg.sprite.spritecollide(player, level1_map.bonus_group, True)
            player.score += len(bonuses) * 20
            if bonuses:
                player.apply_bonus(level1_map.wall_group)
                bonus_sound.play()

            # Проверка проигрыша
            if pg.sprite.spritecollide(player, bullet_sprites, True) or pg.sprite.spritecollide(player, enemy_sprites, False):
                collision_sound.play()
                if record_manager.is_new_record(player.score):
                    game_state = "new_record"
                else:
                    game_state = "game_over"
                play_music(cfg.MENU_MUSIC_PATH)

            # Проверка победы
            if len(level1_map.dot_group) == 0:
                game_state = "win"
                play_music(cfg.MENU_MUSIC_PATH)

        # Отрисовка
        screen.fill(cfg.BLACK)
        if game_state == "menu":
            menu.draw(screen)
        elif game_state == "game":
            level1_map.draw(screen)
            menu.draw_score(screen, player.score)
            for sprite in basic_sprites:
                if hasattr(sprite, "draw"):
                    sprite.draw(screen)
                else:
                    screen.blit(sprite.image, sprite.rect)
            enemy_sprites.draw(screen)
            bullet_sprites.draw(screen)
        elif game_state == "game_over":
            menu.draw_game_over(screen)
        elif game_state == "win":
            menu.draw_win(screen)
        elif game_state == "new_record":
            menu.draw_new_record(
                screen,
                player.score,
                record_name
            )
        elif game_state == "records":
            menu.draw_records(
                screen,
                record_manager.records
            )
        elif game_state == "help":
            menu.draw_help(screen)

        pg.display.flip()
        clock.tick(cfg.FPS)

    pg.quit()

if __name__ == "__main__":
    main()