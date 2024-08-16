import os
import pygame
from shapes import all_shapes
from random import choice, randint
from menu import Menu
from music import explosion
from colors import game_palette
from pickle import dumps, loads
from datetime import datetime, timezone
from game_over_screen import game_over_surface
from game import Game


pygame.init()
main_surface = pygame.display.set_mode((710, 800))
clock = pygame.time.Clock()

game_surface = pygame.Surface((370, 740))
next_shape_surface = pygame.Surface((250, 200))
info_surface = pygame.Surface((250, 200))
best_score_surface = pygame.Surface((250, 220))

info_font = pygame.font.SysFont("Arial", 37)


menu = Menu()

menu_button = menu.get_button()
menu_button_rect = menu_button.get_rect(left=430, top=480)

cw = 37


cg = Game()


def draw_matrix(matrix, pos=(0, 0), surface=game_surface, outline: int = 0):
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            value = matrix[row][col]
            if value == 0:
                continue
            rect_x = (pos[0] + col) * cw + 3
            rect_y = (pos[1] + row) * cw + 3
            rect = pygame.Rect((rect_x, rect_y), (cw - 6, cw - 6))
            colors = game_palette.current_palette
            pygame.draw.rect(surface, colors[value], rect, outline)


def get_center(surface: pygame.Surface, shape: tuple[tuple[int]]):
    surface_width, surface_height = surface.get_size()
    shape_height = len(shape)
    shape_width = len(shape[0])
    x = (surface_width / cw) / 2 - shape_width / 2
    y = (surface_height / cw) / 2 - shape_height / 2
    return x, y


def draw_best_score():
    best_score_surface.fill((0, 0, 0))
    y = 5
    for i, score in enumerate(cg.best_scores):
        score_img = pygame.font.SysFont("Arial", 30).render(
            f"#{i+1}: {score}", True, (255, 255, 255)
        )
        best_score_surface.blit(score_img, (10, y))
        y += 44


if "saved_games" not in os.listdir("."):
    os.mkdir("saved_games")


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            menu.shown = not menu.shown
        if menu.shown:
            menu.handle_event(event)
            continue
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_UP):
                cg.current_shape = cg.rotate_matrix(cg.current_shape)

            if event.key == pygame.K_SPACE:
                y_before = cg.current_shape_pos[1]
                cg.current_shape_pos = cg.predict_position()
                cg.score += (cg.current_shape_pos[1] - y_before) * 2

            if event.key == pygame.K_r and cg.game_over:
                cg = Game()

            if event.key == pygame.K_p:
                cg.save()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT and menu_button_rect.collidepoint(
                event.pos
            ):
                menu.shown = True
                break
            if event.button == pygame.BUTTON_LEFT:
                cg.current_shape = cg.rotate_matrix(cg.current_shape)
            if event.button == pygame.BUTTON_WHEELDOWN:
                new_pos = (cg.current_shape_pos[0], cg.current_shape_pos[1] + 1)
                if cg.is_valid_position(new_pos):
                    current_shape_pos = new_pos
                    cg.score += 1

        if event.type == pygame.MOUSEMOTION:
            if game_surface.get_rect(left=30, top=30).collidepoint(event.pos):
                game_pos = event.pos[0] - 30, event.pos[1] - 30
                x = game_pos[0] // 37
                next_pos = x, cg.current_shape_pos[1]
                if cg.is_valid_position(next_pos):
                    cg.current_shape_pos = next_pos

    pressed = pygame.key.get_pressed()

    if any((pressed[pygame.K_a], pressed[pygame.K_LEFT])) and cg.frame_counter % 5 == 0:
        new_pos = (cg.current_shape_pos[0] - 1, cg.current_shape_pos[1])
        if cg.is_valid_position(new_pos):
            cg.current_shape_pos = new_pos

    if (
        any((pressed[pygame.K_d], pressed[pygame.K_RIGHT]))
        and cg.frame_counter % 5 == 0
    ):
        new_pos = (cg.current_shape_pos[0] + 1, cg.current_shape_pos[1])
        if cg.is_valid_position(new_pos):
            cg.current_shape_pos = new_pos

    if any((pressed[pygame.K_s], pressed[pygame.K_DOWN])) and cg.frame_counter % 5 == 0:
        new_pos = (cg.current_shape_pos[0], cg.current_shape_pos[1] + 1)
        if cg.is_valid_position(new_pos):
            cg.current_shape_pos = new_pos
            cg.score += 1

    main_surface.fill((255, 255, 255))

    game_surface.fill((0, 0, 0))
    next_shape_surface.fill((0, 0, 0))
    info_surface.fill((0, 0, 0))
    draw_matrix(cg.grid)
    draw_matrix(cg.current_shape, cg.current_shape_pos)
    next_shape_pos = get_center(next_shape_surface, cg.next_shape)
    draw_matrix(cg.next_shape, pos=next_shape_pos, surface=next_shape_surface)

    score_img = info_font.render(f"Score: {cg.score}", True, (255, 255, 255))
    info_surface.blit(score_img, (10, 10))

    level_img = info_font.render(f"Level: {cg.level}", True, (255, 255, 255))
    info_surface.blit(level_img, (10, 57))

    lines_img = info_font.render(f"Lines: {cg.lines}", True, (255, 255, 255))
    info_surface.blit(lines_img, (10, 104))

    drop_pos = cg.predict_position()
    draw_matrix(cg.current_shape, drop_pos, game_surface, 1)

    if cg.game_over:
        game_surface.blit(game_over_surface, (20, 270))

    draw_best_score()

    main_surface.blit(game_surface, (30, 30))
    main_surface.blit(next_shape_surface, (430, 30))
    main_surface.blit(info_surface, (430, 260))
    main_surface.blit(menu_button, menu_button_rect)
    main_surface.blit(best_score_surface, (430, 550))

    if not menu.shown and not cg.game_over:
        cg.step()

    menu.draw_frame(main_surface)

    pygame.display.update()
    clock.tick(60)
