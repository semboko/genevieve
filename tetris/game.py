from random import choice, randint
from shapes import all_shapes
from pickle import dumps, loads
from datetime import datetime, timezone
from music import explosion
import os


class Game:
    def __init__(self) -> None:
        self.grid = [[0 for _ in range(10)] for _ in range(20)]
        self.next_shape = self.spawn_shape()
        self.current_shape = self.spawn_shape()
        self.current_shape_pos = (0, 0)
        self.frame_counter = 0
        self.score = 0
        self.level = 0
        self.lines = 0
        self.game_over = False
        self.best_scores = []
        self.load_best_scores()

    def is_valid_position(self, pos, matrix=None):
        if matrix is None:
            matrix = self.current_shape
        if pos[0] < 0 or pos[0] + len(matrix[0]) - 1 > 9:
            return False
        if pos[1] + len(matrix) > 20:
            return False
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                value = matrix[row][col]
                if value == 0:
                    continue
                grid_row = row + pos[1]
                grid_col = col + pos[0]
                if self.grid[grid_row][grid_col] != 0:
                    return False
        return True

    def rotate_matrix(self, matrix, check_pos: bool = True):
        new_matrix = tuple(zip(*matrix[::-1]))
        if check_pos and not self.is_valid_position(self.current_shape_pos, new_matrix):
            return matrix
        return new_matrix

    def spawn_shape(self):
        shape = choice(all_shapes)
        for _ in range(randint(0, 3)):
            shape = self.rotate_matrix(shape, check_pos=False)
        return shape

    def load(self, filename: str):
        with open("./saved_games.bin", "rb") as file:
            (
                self.grid,
                self.next_shape,
                self.current_shape,
                self.frame_counter,
                self.score,
                self.level,
                self.lines,
                self.game_over,
            ) = loads(file.read())

    def save(self):
        dt = datetime.now(tz=timezone.utc).isoformat()
        with open(f"./saved_games/{dt}.bin", "wb") as file:
            file.write(
                dumps(
                    (
                        self.grid,
                        self.next_shape,
                        self.current_shape,
                        self.frame_counter,
                        self.score,
                        self.level,
                        self.lines,
                        self.game_over,
                    )
                )
            )

    def predict_position(self):
        x, y = self.current_shape_pos
        while y < 20 - len(self.current_shape):
            next_y = y + 1
            if not self.is_valid_position((x, next_y)):
                break
            y = next_y
        return x, y

    def step(self):
        speed = (20 - self.level) if self.level < 10 else 10
        if (self.frame_counter == speed):
            next_pos = (self.current_shape_pos[0], self.current_shape_pos[1] + 1)
            if not self.is_valid_position(next_pos):
                self.add_to_grid(self.current_shape_pos)
                self.current_shape = self.next_shape
                self.next_shape = self.spawn_shape()
                self.current_shape_pos = (0, 0)
                self.check_is_over()
            else:
                self.current_shape_pos = next_pos

            self.grid = self.remove_lines(self.grid)
            self.frame_counter = 0
        self.frame_counter += 1

    def check_is_over(self):
        if not self.is_valid_position(self.current_shape_pos):
            self.game_over = True
            self.best_scores.append(self.score)
            self.best_scores.sort(reverse=True)
            self.best_scores = self.best_scores[0:5]
            with open("./best.bin", "wb") as file:
                file.write(dumps(self.best_scores))

    def remove_lines(self, matrix: list[list[int]]):
        lines_to_remove = []
        for i, line in enumerate(matrix):
            if 0 not in line:
                lines_to_remove.append(i)

        if len(lines_to_remove) > 0:
            explosion.play()
            points = (40, 100, 300, 1200)[len(lines_to_remove) - 1]
            self.score += points * (self.level + 1)
            if (self.lines % 10) == 0:
                self.level += 1

        for line_idx in lines_to_remove:
            self.lines += 1
            matrix.remove(matrix[line_idx])
            matrix = [[0, ] * 10] + matrix

        return matrix

    def add_to_grid(self, pos):
        for row in range(len(self.current_shape)):
            for col in range(len(self.current_shape[row])):
                value = self.current_shape[row][col]
                if value == 0:
                    continue
                grid_row = row + pos[1]
                grid_col = col + pos[0]
                self.grid[grid_row][grid_col] = value

    def load_best_scores(self):
        if "best.bin" in os.listdir("."):
            with open("./best.bin", "rb") as file:
                self.best_scores = loads(file.read())
