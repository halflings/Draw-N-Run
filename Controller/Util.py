import glob
from PySFML import *

class Box(object):
    def __init__(self, x, y, witdh, height):
        self.x = x
        self.y = y
        self.width = witdh
        self.height = height

    def contains(self, point):
        x, y = point[0], point[1]
        onX = x >= self.x and x <= (self.x + self.width)
        onY = y >= self.y and y <= (self.y + self.height)
        return onX and onY

    def collides(self, box):
        return not( box.x > (self.x + self.width) \
                or (box.x + box.width) < self.x \
                or (box.y + box.height) < self.y \
                or box.y > (self.y + self.height) )

class Animation(object):
    def __init__(self, path, frameDiv = 8):
        paths = glob.glob("{}/*".format(path))
        paths.sort()

        self.sprites = []
        for path in paths:
            image = sf.Image()
            image.LoadFromFile(path)
            sprite = sf.Sprite(image)
            sprite.SetScale(0.5, 0.5)
            self.sprites.append(sprite)
        self.tick = 0

        self.curSprite = self.sprites[0]

        # The sprite changes each [frameDiv] frames
        self.frameDiv = frameDiv

    def GetSprite(self):
        self.curSprite = self.sprites[int(self.tick/self.frameDiv)]
        self.tick = (self.tick + 1) % (int(self.frameDiv*len(self.sprites)))

        return self.curSprite

    def Reset(self):
        self.tick = 0

    def GetSize(self):
        size = self.curSprite.GetSize()
        return size.x, size.y

def _initObstacles(path = "./Graphics/Platforms"):
    paths = glob.glob(path + "/*")
    sprites = []
    for path in paths:
        image = sf.Image()
        image.LoadFromFile(path)
        sprite = sf.Sprite(image)
        sprites.append(sprite)
    return sprites

class Obstacle(object):
    Sprites = _initObstacles()

    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.box = Box(x, y, sprite.GetSize()[0], sprite.GetSize()[1])

    def GetBox(self):
        return self.box

    def GetSprite(self):
        return self.sprite

class Coin(Obstacle):
    IMG = sf.Image()
    IMG.LoadFromFile('./Graphics/Items/Image1.png')
    gameover_sound = sf.Music()
    gameover_sound.OpenFromFile('Coin.ogg')
    gameover_sound.Initialize(4, 22000)

    def __init__(self, x, y, value):
        s = sf.Sprite(Coin.IMG)
        super(Coin, self).__init__(x, y, s)

        self.value = value

    def destroy(self):
        Coin.gameover_sound.Play()
        self.x = -100
        self.y = -100

