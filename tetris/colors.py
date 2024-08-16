palette1 = {
    1: (252, 186, 3),
    2: (255, 0, 0),
    3: (3, 11, 252),
    4: (232, 12, 70),
    5: (46, 46, 219),
    6: (179, 36, 126),
    7: (154, 191, 17),
}

palette2 = {
    1: "#2713F2",
    2: "#B913F2",
    3: "#550FB8",
    4: "#1347F2",
    5: "#F213D5",
    6: "#9F64F2",
    7: "#D5AB33",
}

palette3 = {
    1: "#2713F3",
    2: "#B913F2",
    3: "#550FB5",
    4: (232, 12, 70),
    5: (46, 46, 219),
    6: "#9F64F1",
    7: "#D5AB32",
}


class GamePalette:
    def __init__(self) -> None:
        self.current_palette = palette1
        self.paletts = [palette1, palette2, palette3]


game_palette = GamePalette()
