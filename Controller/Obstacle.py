from Util import Box

class Obstacle(object):
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.box = Box(x, y, *sprite.GetSize())

    def GetBox(self):
        return self.box

    def GetSprite(self):
        return self.sprite

class Coin(Obstacle):
    IMG = sf.Image()
    IMG.LoadFromFile('./Graphics/Items/Image1.png')

    def __init__(self, x, y, value):
        s = sf.Sprite(Coin.IMG)
        super(Coin, self).__init__(x, y, s)

        self.value = value

    def destroy(self):
        self.x = -100
        self.y = -100

