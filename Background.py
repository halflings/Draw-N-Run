from PySFML import sf

class Background:
    def __init__(self, img, speed):
        self.img = img
        self.speed = speed
        self.sprite1 = sf.Sprite(self.img)
        self.sprite2 = sf.Sprite(self.img)

    def Draw(self, window, posX, posY):
        self.sprite1.SetX(int(posX * self.speed) % self.img.GetWidth())
        self.sprite2.SetX(int(posX * self.speed) % self.img.GetWidth() - self.img.GetWidth())
        self.sprite1.SetY(posY)
        self.sprite2.SetY(posY)

        window.Draw(self.sprite1)
        window.Draw(self.sprite2)

