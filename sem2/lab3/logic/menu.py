import pygame as pg
import config.config as cfg


class Menu:

    def __init__(self):

        self.options = [
            "Start game",
            "Records",
            "Help",
            "Exit"
        ]

        self.selected = 0

        self.font = pg.font.SysFont("Arial", 40)

    def draw(self, screen):

        screen.fill(cfg.BLACK)

        title_font = pg.font.SysFont("Arial", 60)

        title = title_font.render(
            "PACMAN",
            True,
            cfg.YELLOW if hasattr(cfg, "YELLOW") else cfg.WHITE
        )

        screen.blit(
            title,
            (
                cfg.WIDTH // 2 - title.get_width() // 2,
                100
            )
        )

        for i, option in enumerate(self.options):

            color = cfg.RED if i == self.selected else cfg.WHITE

            text = self.font.render(
                option,
                True,
                color
            )

            screen.blit(
                text,
                (
                    cfg.WIDTH // 2 - text.get_width() // 2,
                    250 + i * 70
                )
            )

    def handle_input(self, event):

        if event.type == pg.KEYDOWN:

            if event.key == pg.K_UP:
                self.selected -= 1

            elif event.key == pg.K_DOWN:
                self.selected += 1

            elif event.key == pg.K_RETURN:
                return self.options[self.selected]

        self.selected %= len(self.options)

        return None
    
    def draw_game_over(self, screen):

        screen.fill(cfg.BLACK)

        title_font = pg.font.SysFont("Arial", 70)
        text_font = pg.font.SysFont("Arial", 40)

        title = title_font.render(
            "GAME OVER",
            True,
            cfg.RED
        )

        restart = text_font.render(
            "Press ENTER to restart",
            True,
            cfg.WHITE
        )

        exit_text = text_font.render(
            "Press ESC to exit",
            True,
            cfg.WHITE
        )

        screen.blit(
            title,
            (
                cfg.WIDTH // 2 - title.get_width() // 2,
                180
            )
        )

        screen.blit(
            restart,
            (
                cfg.WIDTH // 2 - restart.get_width() // 2,
                320
            )
        )

        screen.blit(
            exit_text,
            (
                cfg.WIDTH // 2 - exit_text.get_width() // 2,
                390
            )
        )

    def draw_win(self, screen):

        screen.fill(cfg.BLACK)

        title_font = pg.font.SysFont("Arial", 70)
        text_font = pg.font.SysFont("Arial", 40)

        title = title_font.render(
            "YOU WIN!",
            True,
            cfg.GREEN
        )

        restart = text_font.render(
            "Press ENTER to restart",
            True,
            cfg.WHITE
        )

        screen.blit(
            title,
            (
                cfg.WIDTH // 2 - title.get_width() // 2,
                180
            )
        )

        screen.blit(
            restart,
            (
                cfg.WIDTH // 2 - restart.get_width() // 2,
                320
            )
        )