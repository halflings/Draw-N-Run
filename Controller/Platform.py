from PySFML import sf
from Util import Box

Limits = (200., 15.)

def _limit_size(size):
    a, b = size
    if a > 0:
        a = min(a, Limits[0])
    else:
        a = max(a, -Limits[0])
    if b > 0:
        b = min(b, Limits[1])
    else:
        b = max(b, -Limits[1])
    return a, b

class Platform(object):
    def __init__(self, x1, y1, x2, y2):
        self.x, self.y = min(x1, x2), min(y1, y2)
        x, y = self.x, self.y
        self.size = _limit_size((x2 - x1, y2 - y1))
        self.sprite = sf.Shape.Rectangle(x, y, x + self.size[0], y + self.size[1], sf.Color(42, 42, 42))
        #size = (abs(x2 - x1), abs(y2 - y1))
        #self.sprite = sf.Shape.Rectangle(x, y, x + size[0], y + size[1], sf.Color(42, 42, 42))

    def GetBox(self):
        return Box(self.x, self.y, self.size[0], self.size[1])

    def GetSprite(self):
        return self.sprite
