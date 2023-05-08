import turtle
from itertools import pairwise
from geometry import intersect
from math import sqrt

turtle.tracer(5)

class Room:
    def __init__(self, coords):
        self.corners = coords
        self.t = turtle.Turtle()
        self.t.speed(0)
        self.t.hideturtle()
        self.t.width(1)
        self.t.color("black", "grey")
        
    def draw_walls(self):
        self.t.penup()
        self.t.setpos(self.corners[0])
        self.t.pendown()
        
        self.t.begin_fill()
        
        for corner in self.corners:
            self.t.setpos(corner)
        self.t.setpos(self.corners[0])
        
        self.t.end_fill()
    
    def is_outside(self, x, y):
        xs = [x for x, _ in self.corners]
        ys = [y for _, y in self.corners]
        conditions = frozenset((
            x > max(xs),
            x < min(xs),
            y > max(ys),
            y < min(ys),
        ))
        return any(conditions)
    
    def intersect_walls(self, p1, p2):
        for c1, c2 in pairwise(self.corners + (self.corners[0], )):
            if intersect(p1, p2, c1, c2):
                return True
        


class VacumRobot:
    def __init__(self):
        self.t = turtle.Turtle()
        # self.t.penup()
        self.t.speed(0)
        self.step_size = 10
        self.clean_spots = set()
        
    def clean_current_spot(self):
        x, y = self.get_my_position()
        self.t.dot(5, "blue")
        self.clean_spots.add((x, y))
        
    def is_current_spot_clean(self):
        x, y = self.get_my_position()
        return (x, y) in self.clean_spots
    
    def step_forward(self):
        self.t.forward(self.step_size)
    
    def get_my_position(self):
        x, y = self.t.pos()
        return round(x), round(y)
    
    def step_backward(self):
        self.t.backward(self.step_size)
        
    def forward_is_possible(self, room):
        self.step_forward()
        x, y = self.get_my_position()
        self.step_backward()
        return not room.is_outside(x, y)

    def rotate(self):
        self.t.right(90)
    
    def move_to(self, spot):
        self.t.goto(spot)
    
    def get_neighborhood(self, spot):
        x, y = spot
        return (
            (x + self.step_size, y),
            (x, y + self.step_size),
            (x - self.step_size, y),
            (x, y - self.step_size),
        )
        
    def astar_move_to(self, target, room: Room):
        start = self.get_my_position()
        open_set = set((start, ))
        closed_set = set()
        
        g_score, h_score, f_score = {}, {}, {}
        
        distance = lambda a, b: sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
        
        g_score[start] = 0
        h_score[start] = distance(start, target)
        f_score[start] = g_score[start] + h_score[start]
        
        came_from = {}
        
        while open_set:
            spot = min(open_set, key=lambda e: f_score[e])
            
            if spot == target:
                reverse_path = [target]
                while reverse_path[-1] != start:
                    prev_step = reverse_path[-1]
                    next_step = came_from[prev_step]
                    reverse_path.append(next_step)
                for spot in reversed(reverse_path):
                    self.move_to(spot)
            
            open_set.remove(spot)
            closed_set.add(spot)
            
            for n in self.get_neighborhood(spot):
                if n in closed_set:
                    continue
                
                if room.intersect_walls(spot, n):
                    continue
                
                open_set.add(n)
                
                g_score[n] = g_score[spot] + self.step_size
                h_score[n] = distance(n, target)
                f_score[n] = g_score[n] + h_score[n]
                
                came_from[n] = spot
                
    def clean(self, room):
        while True:
            if not self.forward_is_possible(room):
                self.step_backward()
                self.rotate()
            if not self.is_current_spot_clean():
                self.clean_current_spot()
            self.step_forward()
            
    def clean_recursively(self, room, depth=0):
        print(depth)
        if self.is_current_spot_clean():
            return
        self.clean_current_spot()
        
        for i in range(4):
            if self.forward_is_possible(room):
                self.step_forward()
                self.clean_recursively(room, depth + 1)
                self.step_backward()
            self.rotate()
            
    def clean_iteratively(self, room: Room):
        stack = [self.get_my_position()]
        
        while stack:
            spot = stack.pop()
            
            if not room.intersect_walls(self.get_my_position(), spot):
                self.move_to(spot)
            else:
                self.t.color("red")
                self.astar_move_to(spot, room)
                self.t.color("black")
            
            
            self.clean_current_spot()
            for neighbor in self.get_neighborhood(spot):
                if neighbor in self.clean_spots:
                    continue
                
                if neighbor in stack:
                    continue
                
                # if room.is_outside(*neighbor):
                #     continue
                
                if room.intersect_walls(spot, neighbor):
                    continue
                
                stack.append(neighbor)


room = Room((
    (-178, -108),
    (-200, -108),
    (-200, 149),
    (194, 149),
    (194, -159),
    (-72, -159),
    (-72, -108),
    (-85, -108),
    (-85, -99),
    (-72, -99),
    (-72, 0),
    (-7, 0),
    (-7, -5),
    (-63, -5),
    (-63, -150),
    (61, -150),
    (61, -82),
    (33, -82),
    (33, -5),
    (29, -5),
    (29, 0),
    (70, 0),
    (70, -5),
    (38, -5),
    (38, -77),
    (66, -77),
    (66, -150),
    (185, -150),
    (185, -5),
    (106, -5), 
    (106, 0),
    (185, 0),
    (185, 35),
    (182, 35),
    (182, 38),
    (185, 38),
    (185, 141),
    (66, 141),
    (66, 38),
    (152, 38),
    (152, 35),
    (-75, 35),
    (-75, 38),
    (61, 38),
    (61, 141),
    (-66, 141),
    (-66, 116),
    (-72, 116),
    (-72, 141),
    (-192, 141),
    (-192, -99),
    (-178, -99),
    (-178, -108),
    (-85, -108),
))
room.draw_walls()
robot = VacumRobot()
# robot.clean(room)
# robot.clean_recursively(room)
robot.clean_iteratively(room)

turtle.mainloop()