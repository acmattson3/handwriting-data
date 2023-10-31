class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self, p):
        self.x=p.x
        self.y=p.y

    def zero(self):
        self.x=0
        self.y=0

class StrokeCoord:
    def __init__(self, x, y, t):
        self.x=x
        self.y=y
        self.t=t

    def __init__(self, p, t):
        self.x=p.x
        self.y=p.y
        self.t=t

    def copy(self, p):
        self.x=p.x
        self.y=p.y
        self.t=p.t

    def copy(self, p, t):
        self.x=p.x
        self.y=p.y
        self.t=t

    def copy(self, x, y, t):
        self.x=x
        self.y=y
        self.t=t