import pygame
from typing import Tuple, Optional, Type


def convert(pos: Tuple[float, float], h: int) -> Tuple[int, int]:
    x, y = pos
    return round(x), round(h - y)


class AbsctractScene:
    def __init__(self) -> None:
        pass
    
    def handle_event(self, event: pygame.event.Event) -> None:
        pass
    
    def update(self) -> None:
        pass
    
    def render(self, display: pygame.Surface) -> None:
        pass


class Game:
    def __init__(
        self,
        window_size: Tuple[int, int], 
        background_color: Tuple[int, int, int], 
        fps: int,
    ):
        pygame.init()
        self.bgc = background_color
        self.fps = fps
        self.display = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        self.scene: Optional[AbsctractScene] = None
    
    def load_scene(self, Scene: Type[AbsctractScene]):
        self.scene = Scene()
    
    def run(self):
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    return

                self.scene.handle_event(e)

            self.scene.update()
            
            self.display.fill(self.bgc)
            
            self.scene.render(self.display)
            
            pygame.display.update()
            self.clock.tick(self.fps)
            