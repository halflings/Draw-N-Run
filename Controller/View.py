from PySFML import sf

from Controller import Controller

class View(object):

    def __init__(self, background_path, width = 800, height = 600):
        self.renderWindow = sf.RenderWindow(sf.VideoMode(800, 600), "Cartoon Runner")
        bgImg = sf.Image()
        bgImg.LoadFromFile(background_path)
        self.bg = sf.Sprite(bgImg)

        self.controller = Controller()

    def Update(self):
        self.controller.Update()

        self.renderWindow.Draw(self.bg)

        for obs in self.controller.obstacles:
            obs.GetSprite().SetPosition(obs.x, obs.y)
            self.renderWindow.Draw(obs.GetSprite())

        player = self.controller.player
        #print "Player ", player.x, player.y
        sprite = player.GetSprite()
        sprite.SetPosition(int(player.x), int(player.y))
        print player.x, player.y
        self.renderWindow.Draw(sprite)

        self.renderWindow.Display()

        self.renderWindow.Clear()


