''' coordinates for handwriting-data
* Contains classes that provide structure for
  coordinate values gathered from drawing
'''

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

    def tuplize(self):
        return (self.x, self.y)

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

    def tuplize(self):
        return (self.x, self.y)
    
    def deformat(self):
        new_format={}
        new_format["x"]=self.x
        new_format["y"]=self.y
        new_format["t"]=self.t
        return new_format