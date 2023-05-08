import turtle

turtle.width(10)
turtle.speed(0)

UNIT = 150

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

def click_handler(x, y):
    print(x, y)

turtle.onscreenclick(click_handler)
turtle.mainloop()