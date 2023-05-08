import turtle

turtle.width(10)
turtle.speed(0)

UNIT = 150
TURN = True
OCCUPIED_CELLS = dict()
WINNER = None

def draw_line(init_x, init_y, lenght):
    turtle.penup()
    turtle.goto(init_x, init_y)
    turtle.pendown()
    turtle.forward(lenght)

draw_line(-1.5 * UNIT, 0.5 * UNIT, 3 * UNIT)
draw_line(-1.5 * UNIT, -0.5 * UNIT, 3 * UNIT)
turtle.right(90)
draw_line(-0.5 * UNIT, 1.5 * UNIT, 3 * UNIT)
draw_line(0.5 * UNIT, 1.5 * UNIT, 3 * UNIT)
turtle.left(90)

def draw_x(x, y):
    turtle.color("red")
    size = 0.8 * UNIT
    diag = 1.41 * size
    turtle.right(45)
    draw_line(x - size/2, y + size/2, diag)
    turtle.right(90)
    draw_line(x + size/2, y + size/2, diag)
    turtle.left(135)

def draw_o(x, y):
    turtle.color("green")
    size = 0.8 * UNIT
    turtle.penup()
    turtle.setpos(x, y - size/2)
    turtle.pendown()
    turtle.circle(size/2)


def is_outside(x, y):
    conditions = (
        x > 1.5 * UNIT,
        x < -1.5 * UNIT,
        y > 1.5 * UNIT,
        y < -1.5 * UNIT,
    )
    
    return any(conditions)

def detect_line(coord):
    if coord > 0.5 * UNIT:
        return 1
    if coord < -0.5 * UNIT:
        return -1
    return 0


def detect_winner():
    if len(OCCUPIED_CELLS) < 5:
        return
    
    # Check each column
    for col in (-1, 0, 1):
        shapes = []
        for coord, shape in OCCUPIED_CELLS.items():
            if coord[0] == col:
                shapes.append(shape)
        if len(shapes) == 3 and shapes[0] == shapes[1] == shapes[2]:
            turtle.right(90)
            draw_line(UNIT * col, 1.5 * UNIT, 3 * UNIT)
            return shapes[0]
        
    
    for row in (-1, 0, 1):
        shapes = []
        for coord, shape in OCCUPIED_CELLS.items():
            if coord[1] == row:
                shapes.append(shape)
        if len(shapes) == 3 and shapes[0] == shapes[1] == shapes[2]:
            draw_line(-1.5 * UNIT, row * UNIT, 3 * UNIT)
            return shapes[0]

    left_diag = ((-1, 1), (0, 0), (1, -1))
    right_diag = ((-1, -1), (0, 0), (1, 1))
    
    left_cells = []
    right_cells = []
    
    for coord, shape in OCCUPIED_CELLS.items():
        if coord in left_diag:
            left_cells.append(shape)
        if coord in right_diag:
            right_cells.append(shape)
    
    if len(left_cells) == 3 and left_cells[0] == left_cells[1] == left_cells[2]:
        turtle.right(45)
        draw_line(-1.5 * UNIT, 1.5 * UNIT, 4.24 * UNIT)
        return left_cells[0]
    
    if len(right_cells) == 3 and right_cells[0] == right_cells[1] == right_cells[2]:
        # Draw the diag line
        return right_cells[0]
    


def click_handler(x, y):
    global WINNER
    global TURN
    if WINNER is not None:
        return
    
    if is_outside(x, y):
        return
    
    col = detect_line(x)
    row = detect_line(y)
    
    if (col, row) in OCCUPIED_CELLS:
        return
    OCCUPIED_CELLS[(col, row)] = TURN
    
    x = col * UNIT
    y = row * UNIT
    
    if TURN:
        draw_x(x, y)
    else:
        draw_o(x, y)
    TURN = not TURN
    
    WINNER = detect_winner()


turtle.onscreenclick(click_handler)
turtle.mainloop()