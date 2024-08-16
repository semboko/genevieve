from gui.elements import GUIelement, ErrorMessage
from typing import List, Optional, Callable
from pygame import Surface, Rect
from pygame.event import Event


class Screen:
    def __init__(self) -> None:
        self.elements: List[GUIelement] = []
        self.el_idx: Optional[int] = None
        self.on_render: List[Callable] = []

    def add_on_render(self, callback: Callable) -> None:
        self.on_render.append(callback)

    def add_element(self, el: GUIelement) -> None:
        self.elements.append(el)

    def post_setup(self):
        self.elements.append(ErrorMessage())

    def handle_mouseclick(self, event: Event) -> None:
        for el_idx, el in enumerate(self.elements):
            el_rect = el.get_rect()
            if el_rect.collidepoint(event.pos):
                el.handle_mouseclick(event)
                self.el_idx = el_idx
                print(f"Element {el_idx} chosen as a new active element")

    def handle_keypress(self, event: Event) -> None:
        if self.el_idx is None:
            return
        active_element = self.elements[self.el_idx]
        active_element.handle_keypress(event)

    def draw(self, screen: Surface) -> None:
        for el in self.elements:
            el.draw(screen)
