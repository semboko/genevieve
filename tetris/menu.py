import pygame
from music import casual_music, explosion
from colors import game_palette


class Slider:
    def __init__(self, pos: tuple[int, int], size: tuple[int, int]) -> None:
        self.pos = pos
        self.size = size
        self.level = 0
        self.rect = pygame.Rect((0, 0), (0, 0))
        self.sounds: list[pygame.mixer.Sound] = []

    def change_level(self, mouse_pos: pygame.Vector2):
        if mouse_pos.x < self.pos[0]:
            self.level = 0
            return
        if mouse_pos.x > self.pos[0] + self.size[0]:
            self.level = 100
            return
        self.level = (mouse_pos.x - self.pos[0]) * 100 / self.size[0]

    def draw(self, surface: pygame.Surface, color: tuple[int]):
        bg = pygame.Surface(self.size)
        w = self.size[1]
        rect_x = self.level * (self.size[0] - w) / 100
        moving_rect = pygame.Rect(
            (rect_x + 5, 5), (w - 10, self.size[1] - 10)
        )
        pygame.draw.rect(bg, color, ((0, 0), self.size), 1)
        pygame.draw.rect(bg, color, moving_rect)
        self.rect = surface.blit(bg, self.pos)


class VolumeSlider(Slider):
    sounds: list[pygame.mixer.Sound]

    def bind_to(self, sounds: list[pygame.mixer.Sound]):
        self.sounds = sounds

    def change_level(self, mouse_pos: pygame.Vector2):
        super().change_level(mouse_pos)
        for sound in self.sounds:
            sound.set_volume(self.level / 100)


class ColorSelect:
    def __init__(self) -> None:
        self.pos = (340, 150)
        self.size = (200, 100)
        colors = game_palette.current_palette
        self.label_img = pygame.font.SysFont("Arial", 18).render("Current Palette", True, colors[4])
        self.rect = pygame.Rect((self.pos[0] + 50, self.pos[1] + 50), self.size)
        self.options = [pygame.Rect(0, 0, 0, 0) for _ in game_palette.paletts]

    def draw_palette(self, pos, palette, surface):
        x = self.pos[0] + pos[0]
        y = self.pos[1] + pos[1]
        for color in palette:
            pygame.draw.rect(surface, palette[color], (x, y, 15, 15))
            x += 17

    def handle_click(self, event: pygame.event.Event):
        for i, opt_rect in enumerate(self.options):
            if opt_rect.collidepoint((event.pos[0] - 50, event.pos[1] - 50)):
                game_palette.current_palette = game_palette.paletts[i]

    def draw(self, surface: pygame.Surface) -> None:
        label_x = self.pos[0]
        label_y = self.pos[1] - self.label_img.get_height() - 5
        surface.blit(self.label_img, (label_x, label_y))
        colors = game_palette.current_palette
        pygame.draw.rect(surface, colors[4], (self.pos, self.size), 1)

        y = 16
        for i, palette in enumerate(game_palette.paletts):
            pos_x = self.pos[0] + 16
            pos_y = self.pos[1] + y + 7
            self.options[i] = pygame.draw.circle(surface, (255, 255, 255), (pos_x, pos_y), 6, 1)
            if palette == game_palette.current_palette:
                pygame.draw.circle(surface, (255, 255, 255), (pos_x, pos_y), 3)
            self.draw_palette((30, y), palette, surface)
            y += 25


class Controller:
    def __init__(
        self,
        pos: tuple[int],
        size: tuple[int],
        label: str,
        color: tuple[int],
        ControllerType: type[Slider],
        **extra_params
    ):
        self.pos = pos
        self.size = size
        self.label_img = pygame.font.SysFont("Arial", 18).render(label, True, color)
        self.color = color
        self.controller = ControllerType(self.pos, self.size)
        if isinstance(self.controller, VolumeSlider):
            self.controller.bind_to(extra_params["sounds"])

    def draw(self, surface: pygame.Surface):
        label_x = self.pos[0]
        label_y = self.pos[1] - 5 - self.label_img.get_height()
        surface.blit(self.label_img, (label_x, label_y))
        self.controller.draw(surface, self.color)


class Menu:
    def __init__(self) -> None:
        self.shown = True

        self.menu_surface = pygame.Surface((600, 700))
        self.title = pygame.font.SysFont("Arial", 35).render("Menu", True, (255, 255, 255))
        self.title_dest = self.title.get_rect(center=(300, 100))

        self.controllers = [
            Controller((50, 150), (200, 30), "Volume", (217, 87, 143), VolumeSlider, sounds=[casual_music]),
            Controller((50, 220), (200, 30), "Sound Effects", (154, 191, 17), VolumeSlider, sounds=[explosion]),
        ]
        self.active_element = None

        self.color_select = ColorSelect()

        self.close_img = pygame.font.SysFont("Arial", 30).render("EXIT", True, (255, 255, 255))
        self.close_surface = pygame.Surface((self.close_img.get_width() + 50, self.close_img.get_height() + 20))
        self.close_surface.blit(self.close_img, (25, 10))
        colors = game_palette.current_palette
        pygame.draw.rect(self.close_surface, colors[6], ((0, 0), self.close_surface.get_size()), 1)
        self.close_dest = self.close_surface.get_rect(center=(300, 450))
        self.close_dest.bottom = 680

    def handle_event(self, event: pygame.event.Event) -> None:
        if not hasattr(event, "pos"):
            return
        mouse_pos = pygame.Vector2(event.pos) - pygame.Vector2((50, 50))
        if event.type == pygame.MOUSEBUTTONDOWN:
            for controller in self.controllers:
                if controller.controller.rect.collidepoint(mouse_pos):
                    self.active_element = controller.controller
            if self.close_dest.collidepoint(mouse_pos):
                self.shown = False
            if self.color_select.rect.collidepoint(event.pos):
                self.color_select.handle_click(event)

        if event.type == pygame.MOUSEBUTTONUP:
            self.active_element = None

        if event.type == pygame.MOUSEMOTION and self.active_element is not None:
            self.active_element.change_level(mouse_pos)

    def get_button(self):
        button_surface = pygame.Surface((250, 50))
        button_surface.fill((0, 0, 0))
        font = pygame.font.SysFont("Arial", 25)
        txt = font.render("Menu", True, (255, 255, 255))
        txt_dest = txt.get_rect(center=(125, 25))
        button_surface.blit(txt, txt_dest)
        return button_surface

    def draw_frame(self, window: pygame.Surface) -> None:
        if not self.shown:
            return

        self.menu_surface.fill((0, 0, 0))
        colors = game_palette.current_palette
        pygame.draw.rect(self.menu_surface, colors[6], (10, 10, 580, 680), 1)
        self.menu_surface.blit(self.title, self.title_dest)
        self.menu_surface.blit(self.close_surface, self.close_dest)

        for c in self.controllers:
            c.draw(self.menu_surface)
        self.color_select.draw(self.menu_surface)
        window.blit(self.menu_surface, (50, 50))
