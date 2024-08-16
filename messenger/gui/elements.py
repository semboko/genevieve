from pygame import Vector2, Surface, font, draw, Rect
from pygame.event import Event
from typing import Callable, List, Tuple
from storage import storage
from string import printable
from datetime import datetime
from utils import cut_string, break_string_into_lines
import pygame


class GUIelement:
    def __init__(self, pos: Vector2, size: Vector2) -> None:
        self.pos = pos
        self.size = size

    def handle_mouseclick(self, event: Event) -> None:
        print("Mouse was clicked")

    def handle_keypress(self, event: Event) -> None:
        print("Key was pressed")

    def get_rect(self):
        return pygame.Rect(self.pos, self.size)

    def draw(self, screen: Surface) -> None:
        raise NotImplementedError("Draw must be implemented for every child of GUIelement")


class ScreenTitle(GUIelement):
    def __init__(self, pos: Vector2, txt: str) -> None:
        self.txt = txt
        f = font.SysFont("Arial", 26)
        self.txt_surface = f.render(txt, True, (0, 0, 0))
        super().__init__(pos, Vector2(self.txt_surface.get_size()))

    def draw(self, screen: Surface) -> None:
        screen_width = screen.get_width()
        txt_width = self.txt_surface.get_width()

        x_pos = (screen_width - txt_width) / 2
        y_pos = self.pos.y

        screen.blit(self.txt_surface, (x_pos, y_pos))


class DynamicText(GUIelement):
    def __init__(
        self,
        pos: Vector2,
        size: Vector2,
        storage_key: str,
        default_value: str,
        font_size: int = 18
    ) -> None:
        super().__init__(pos, size)
        self.storage_key = storage_key
        self.default_value = default_value
        self.font = pygame.font.SysFont("Arial", font_size)

    def draw(self, screen: Surface) -> None:
        text = storage.get(self.storage_key) or self.default_value
        text_img = self.font.render(text, True, (0, 0, 0))
        screen.blit(text_img, self.pos)


class Message(GUIelement):

    author_font = font.SysFont("Arial", 18)
    msg_font = font.SysFont("Arial", 16)
    dt_font = font.SysFont("Arial", 12)

    def __init__(self, width: int, author: str, msg: str, date: str) -> None:
        self.author = author
        self.msg = msg
        self.date = date
        self.width = width
        self.msg_img = self.build_layout()

    def prepare_msg(self, bg_color: Tuple[int, int, int]) -> Surface:
        msg_imgs = []
        start = 0
        length = 45

        while start < len(self.msg):
            end = start + length
            line = self.msg[start:end]
            line_img = self.msg_font.render(line, True, (0, 0, 0))
            msg_imgs.append(line_img)
            start = end

        msg_img_width = max(msg_imgs, key=lambda i: i.get_width()).get_width()
        msg_img_height = len(msg_imgs) * msg_imgs[0].get_height()

        msg_img = Surface(Vector2(msg_img_width, msg_img_height))
        msg_img.fill(bg_color)
        y = 0
        for i in msg_imgs:
            msg_img.blit(i, (0, y))
            y += i.get_height()

        return msg_img

    def build_layout(self) -> Surface:

        bg_color = (240, 222, 255) if self.author == storage["username"] else (230, 230, 230)

        author_img = self.author_font.render(self.author, True, (0, 0, 0))
        msg_img = self.prepare_msg(bg_color)

        dt = datetime.fromtimestamp(float(self.date))
        time_to_show = dt.strftime("%m/%d/%y %H:%M:%S")

        dt_img = self.dt_font.render(time_to_show, True, (150, 150, 150))

        margin = 5
        total_height = author_img.get_height() + msg_img.get_height() + 3 * margin
        total_width = self.width

        surface = Surface((total_width, total_height))
        surface.fill((255, 255, 255))
        draw.rect(
            surface,
            bg_color,
            pygame.Rect((0, 0), (surface.get_size())),
            0,
            10,
        )
        surface.blit(author_img, (margin, margin))
        surface.blit(msg_img, (margin, 2 * margin + author_img.get_height()))
        surface.blit(dt_img, (total_width - dt_img.get_width() - margin, margin))

        return surface

    def draw(self, screen: Surface) -> None:
        screen.blit(self.msg_img, self.pos)


class MessagesList(GUIelement):
    def __init__(self, pos: Vector2, size: Vector2) -> None:
        super().__init__(pos, size)
        self.offset_y = 0
        self.surface_height = 0
        self.messages_height = 0

    def handle_mouseclick(self, event: Event) -> None:
        if event.button == pygame.BUTTON_WHEELUP:
            print("wheel up")
            self.offset_y += 5
            if (self.messages_height - self.surface_height) < self.offset_y:
                self.offset_y = self.messages_height - self.surface_height
                storage["msg_end"] += 10

        if event.button == pygame.BUTTON_WHEELDOWN:
            print("wheel down")
            if self.offset_y <= 0:
                self.offset_y = 0
                return
            self.offset_y -= 5

    def draw(self, screen: Surface) -> None:
        bottom_y = storage["message_input_top"] - 5
        top_y = 110
        self.surface_height = bottom_y - top_y
        surface = pygame.Surface((self.size.x, self.surface_height))
        surface.fill((255, 255, 255))

        local_y = surface.get_height() + self.offset_y
        self.messages_height = 0
        for author, msg, dt in reversed(storage["messages"]):
            msg = Message(self.size.x, author, msg, dt)
            height = msg.msg_img.get_height()
            self.messages_height += height + 5
            local_y -= height + 5
            surface.blit(msg.msg_img, (0, local_y))

        screen.blit(surface, (self.pos.x, top_y))


class TextInput(GUIelement):
    def __init__(self, pos: Vector2, size: Vector2, key: str, name: str = "") -> None:
        super().__init__(pos, size)
        storage[key] = ""
        self.key = key
        self.font = font.SysFont("Arial", 18)
        self.rect = Rect(pos, size)
        self.name = name
        name_font = font.SysFont("Arial", 12)
        self.name_img = name_font.render(name, True, (0, 0, 0), (255, 255, 255))

    def handle_keypress(self, event: Event) -> None:
        if event.key == pygame.K_BACKSPACE:
            storage[self.key] = storage[self.key][0:-1]
            return
        if event.key == pygame.K_RETURN:
            print("return was pressed")
            return
        if event.unicode == "|":
            return
        if event.unicode in printable:
            storage[self.key] += event.unicode

    def draw(self, screen: Surface) -> None:
        draw.rect(screen, (0, 0, 0), self.rect, 1, 10)
        txt_surface = self.font.render(storage[self.key], True, (0, 0, 0))
        txt_size = txt_surface.get_size()
        txt_height = txt_size[1]
        screen.blit(txt_surface, self.pos + Vector2(5, self.size.y / 2 - txt_height / 2))
        screen.blit(self.name_img, self.pos + Vector2(20, -6))


class ResizableTextInput(TextInput):
    def draw(self, screen: Surface) -> None:
        text_lines = break_string_into_lines(storage[self.key], length=30)
        text_imgs = []
        total_text_height = 11
        for line in text_lines:
            txt_img = self.font.render(line, True, (0, 0, 0))
            total_text_height += txt_img.get_height()
            text_imgs.append(txt_img)
        bottom_line = self.pos.y + self.size.y  # 580
        bottom_line -= 11  # Because of the bottom margin
        for txt_img in reversed(text_imgs):
            img_height = txt_img.get_height()
            img_y = bottom_line - img_height
            img_x = self.pos.x + 5
            screen.blit(txt_img, (img_x, img_y))
            bottom_line -= img_height

        if total_text_height == 11:
            total_text_height += 16
            bottom_line -= 16
            # bottom_line = self.pos.y

        total_text_height += 11  # Because of the top margin
        bottom_line -= 11  # Because of the top margin

        storage["message_input_top"] = bottom_line

        # From now the bottom_line variable actually holds the y position of the top

        outline = pygame.Rect(
            (self.pos.x, bottom_line),
            (self.size.x, total_text_height),
        )
        pygame.draw.rect(screen, (0, 0, 0), outline, 1, 10)


class Button(GUIelement):
    def __init__(self, pos: Vector2, size: Vector2, txt: str, onclick: Callable) -> None:
        super().__init__(pos, size)
        self.font = font.SysFont("Arial", 16)
        self.txt_image = self.font.render(txt, True, (0, 0, 0))
        self.onclick = onclick

    def handle_mouseclick(self, event: Event) -> None:
        self.onclick(event)

    def draw(self, screen: Surface) -> None:
        r = Rect(self.pos, self.size)
        draw.rect(screen, (200, 200, 200), r, border_radius=10)
        draw.rect(screen, (0, 0, 0), r, 1, 10)
        screen.blit(self.txt_image, self.pos + self.size / 2 - Vector2(self.txt_image.get_size()) / 2)


class TextInputWHints(TextInput):

    def __init__(self, pos: Vector2, size: Vector2, key: str, name: str = "") -> None:
        super().__init__(pos, size, key, name)
        self.hints_font = pygame.font.SysFont("Arial", 18)
        self.hints_surface = pygame.Surface((0, 0))
        self.hints_rect = pygame.Rect(
            (self.pos + pygame.Vector2(0, size.y + 10)),
            self.hints_surface.get_size(),
        )

    def get_rect(self):
        total_height = self.size.y + self.hints_rect.height
        return pygame.Rect(self.pos, (self.size.x, total_height))

    def handle_keypress(self, event: Event) -> None:
        super().handle_keypress(event)
        storage.get_contact_hints()
        if len(storage[self.key]) < 2:
            storage["contact_hints"] = []

    def handle_mouseclick(self, event: Event) -> None:
        if self.hints_rect.collidepoint(event.pos):
            rel_y = event.pos[1] - self.hints_rect.top
            idx = int(rel_y/21)
            storage.add_friend(storage["contact_hints"][idx])
            storage[self.key] = ""
            storage["contact_hints"] = []
            storage.load_contacts()

    def draw(self, screen: Surface) -> None:
        super().draw(screen)
        imgs = []
        hints_height = 0
        for contact in storage["contact_hints"]:
            contact_img = self.hints_font.render(contact, True, (0, 0, 0))
            hints_height += contact_img.get_height()
            imgs.append(contact_img)

        self.hints_surface = pygame.Surface((self.size.x, hints_height))
        self.hints_surface.fill((255, 255, 255))

        y = 0
        for img in imgs:
            self.hints_surface.blit(img, (0, y))
            y = y + img.get_height()

        self.hints_rect = screen.blit(self.hints_surface, self.hints_rect)


class ElementList(GUIelement):
    def __init__(self, pos: Vector2, size: Vector2, storage_key: str, loader_callback: Callable, click_callback: Callable) -> None:
        self.storage_key = storage_key
        self.on_render = loader_callback
        self.on_click = click_callback
        self.font = pygame.font.SysFont("Arial", 18)
        self.x_img = self.font.render("X", True, (0, 0, 0))
        self.item_rect: List[pygame.Rect] = []
        self.x_rect: List[pygame.Rect] = []
        super().__init__(pos, size)

    def handle_mouseclick(self, event: Event) -> None:
        for i in range(len(self.item_rect)):
            if self.item_rect[i].collidepoint(event.pos):
                self.on_click(storage["contacts"][i])

        for i in range(len(self.x_rect)):
            if self.x_rect[i].collidepoint(event.pos):
                contact_id = storage["contacts"][i]
                storage.delete_contact(contact_id)

    def draw(self, screen: Surface) -> None:
        self.item_rect = []
        self.x_rect = []
        y = self.pos.y
        for contact in storage["contacts"]:
            contact_img = self.font.render(cut_string(contact, letters=25), True, (0, 0, 0))
            rect = screen.blit(contact_img, (self.pos.x, y))
            self.item_rect.append(rect)

            x_pos = (self.pos.x + self.size.x - self.x_img.get_width(), y)
            x_rect = screen.blit(self.x_img, x_pos)
            self.x_rect.append(x_rect)

            y += contact_img.get_height() + 5


class ErrorMessage(GUIelement):
    def __init__(self) -> None:
        super().__init__(Vector2(10, 10), Vector2(380, 20))
        self.font = pygame.font.SysFont("Arial", 18)

    def handle_mouseclick(self, event: Event) -> None:
        storage["error_msg"] = ""

    def draw(self, screen: Surface) -> None:
        if storage["error_msg"] == "":
            return

        lines = break_string_into_lines(storage["error_msg"], 30)

        surface_height = 0
        line_imgs = []
        for line in lines:
            line_img = self.font.render(line, True, (255, 255, 255))
            surface_height += line_img.get_height()
            line_imgs.append(line_img)

        surface = Surface((self.size.x, surface_height + 20))
        surface.fill((219, 77, 101))
        y = 10
        for img in line_imgs:
            surface.blit(img, (10, y))
            y += img.get_height() + 5

        screen.blit(surface, self.pos)
