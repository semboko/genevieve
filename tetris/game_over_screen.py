from pygame import Surface
from pygame.font import SysFont
from pygame.draw import rect
from colors import game_palette


game_over_surface = Surface((330, 250))

game_over_surface.fill((0, 0, 0))
colors = game_palette.current_palette
rect(game_over_surface, colors[4], (10, 10, 310, 230), 1)

large_font = SysFont("Arial", 40)

go_image = large_font.render("Game Over", True, (255, 255, 255))
go_dest = go_image.get_rect(center=(330/2, 250/2))
go_dest.top -= 20
game_over_surface.blit(go_image, go_dest)

medium_font = SysFont("Arial", 20)

press_img = medium_font.render("Press <R> to restart", True, (255, 255, 255))
press_dest = (go_dest.left, go_dest.bottom + 10)
game_over_surface.blit(press_img, press_dest)
