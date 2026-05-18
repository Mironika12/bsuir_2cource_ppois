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

    def draw_score(self, screen, score: int):
        score_font = pg.font.SysFont("Arial", 30)

        score_text = score_font.render(
            f"Score: {score}",
            True,
            cfg.WHITE
        )

        screen.blit(
            score_text,
            (10, 10)
        )

    def draw_new_record(
        self,
        screen,
        score,
        name
    ):

        screen.fill(cfg.BLACK)

        title_font = pg.font.SysFont("Arial", 60)
        text_font = pg.font.SysFont("Arial", 40)

        title = title_font.render(
            "NEW RECORD!",
            True,
            cfg.YELLOW
        )

        score_text = text_font.render(
            f"Score: {score}",
            True,
            cfg.WHITE
        )

        name_text = text_font.render(
            f"Name: {name}",
            True,
            cfg.GREEN
        )

        enter_text = text_font.render(
            "Press ENTER to save",
            True,
            cfg.WHITE
        )

        screen.blit(
            title,
            (
                cfg.WIDTH // 2 - title.get_width() // 2,
                120
            )
        )

        screen.blit(
            score_text,
            (
                cfg.WIDTH // 2 - score_text.get_width() // 2,
                240
            )
        )

        screen.blit(
            name_text,
            (
                cfg.WIDTH // 2 - name_text.get_width() // 2,
                320
            )
        )

        screen.blit(
            enter_text,
            (
                cfg.WIDTH // 2 - enter_text.get_width() // 2,
                420
            )
        )

    def draw_records(self, screen, records):
        screen.fill(cfg.BLACK)

        title_font = pg.font.SysFont("Arial", 60)
        text_font = pg.font.SysFont("Arial", 40)

        title = title_font.render("BEST RECORDS", True, cfg.YELLOW)
        screen.blit(
            title,
            (cfg.WIDTH // 2 - title.get_width() // 2, 80)
        )

        for i, record in enumerate(records):
            name_text = text_font.render(
                f"{i + 1}. {record['name']}",
                True,
                cfg.WHITE
            )
            score_text = text_font.render(
                f"{record['score']}",
                True,
                cfg.WHITE
            )

            y = 180 + i * 50
            screen.blit(name_text, (120, y))
            screen.blit(score_text, (cfg.WIDTH - 180, y))

    def draw_help(self, screen):
        screen.fill(cfg.BLACK)

        title_font = pg.font.SysFont("Arial", 60)
        text_font = pg.font.SysFont("Arial", 32)

        # Заголовок
        title = title_font.render("HELP / RULES", True, cfg.YELLOW)
        screen.blit(title, (cfg.WIDTH // 2 - title.get_width() // 2, 50))

        # Список правил
        rules = [
            "Use arrow keys to move the player",
            "Collect all dots to win",
            "Avoid enemies and bullets",
            "Collect bonuses for special effects:",
            "  - Speed boost",
            "  - Random teleport",
            "  - Shield (if enabled)",
            "Press ESC to return to menu"
        ]

        y = 150
        for line in rules:
            text = text_font.render(line, True, cfg.WHITE)
            screen.blit(text, (50, y))
            y += 40