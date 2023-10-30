class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class StrokeCoord:
    def __init__(self, x, y, t):
        self.x=x
        self.y=y
        self.t=t

    def __init__(self, p, t):
        self.x=p.x
        self.y=p.y
        self.t=t