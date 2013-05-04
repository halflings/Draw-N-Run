from PySFML import sf
from Client import App

class Menu:
    def __init__(self, width = 1400, height = 700, window = None):
        self.width, self.height = width, height
        if not window:
            self.window = sf.RenderWindow(sf.VideoMode(width, height, 32), "Cartoon Runner")
            self.window.SetFramerateLimit(24)
        else:
            self.window = window

        self.running = False
        self.cursor = 0
        self.sprCursor = []

        img = sf.Image()
        img.LoadFromFile("Graphics/Menu/bg.png")
        self.sprBackground = sf.Sprite(img)

        x = -(self.window.GetWidth() - self.sprBackground.GetSize()[0]) / 2.0
        y = 0
        self.sprBackground.SetCenter(x, y)

        img = sf.Image()
        img.LoadFromFile("Graphics/Menu/logo.png")
        self.sprLogo = sf.Sprite(img)
        x = -(self.window.GetWidth() - self.sprLogo.GetSize()[0]) / 2.0
        y = -30
        self.sprLogo.SetCenter(x, y)

        img1, img2 = sf.Image(), sf.Image()
        img1.LoadFromFile("Graphics/Menu/start.png")
        img2.LoadFromFile("Graphics/Menu/start_on.png")
        self.sprCursor += [(sf.Sprite(img1), sf.Sprite(img2))]

        x = -(self.window.GetWidth() - self.sprCursor[-1][0].GetSize()[0]) / 2.0
        self.sprCursor[-1][0].SetCenter(x, 0)
        self.sprCursor[-1][0].SetY(600)
        self.sprCursor[-1][1].SetCenter(x, -600)

        # img1, img2 = sf.Image(), sf.Image()
        # img1.LoadFromFile("./img/selection_niveau.png")
        # img2.LoadFromFile("./img/selection_niveau_on.png")
        # self.sprCursor += [(sf.Sprite(img1), sf.Sprite(img2))]

        # x = -(self.window.GetWidth() - self.sprCursor[-1][0].GetSize()[0]) / 2.0
        # self.sprCursor[-1][0].SetCenter(x, 0)
        # self.sprCursor[-1][0].SetY(self.sprCursor[-2][0].GetPosition()[1] + self.sprCursor[-2][0].GetSubRect().Bottom + 30)
        # self.sprCursor[-1][1].SetCenter(x, -self.sprCursor[-1][0].GetPosition()[1])

        self.music = sf.Music()
        self.music.OpenFromFile('omfgdogs.ogg')
        self.music.Initialize(4, 16000)
        self.music.Play()
        self.musicPlayed = True

    def run(self):
        self.running = True
        while self.running:
            self.event()
            self.draw()

    def event(self):
        event = sf.Event()
        while self.window.GetEvent(event):
            if event.Type == sf.Event.Closed:
                self.running = False

            if event.Type == sf.Event.KeyPressed:
                if event.Key.Code == sf.Key.Up:
                    self.goUp()
                if event.Key.Code == sf.Key.Down:
                    self.goDown()
                if event.Key.Code == sf.Key.Return:
                    self.goIn()
                if event.Key.Code == sf.Key.M:
                    if self.musicPlayed:
                        self.music.Pause()
                        self.musicPlayed = False
                    else:
                        self.music.Play()
                        self.musicPlayed = True

    def draw(self):
        self.window.Clear()
        self.window.Draw(self.sprBackground)
        self.window.Draw(self.sprLogo)

        for i, p in enumerate(self.sprCursor):
            self.window.Draw(p[0])
            if i == self.cursor:
                self.window.Draw(p[1])

        self.window.Display()

    def goUp(self):
        self.cursor -= 1
        if self.cursor < 0:
            self.cursor = len(self.sprCursor) - 1

    def goDown(self):
        self.cursor += 1
        if self.cursor >= len(self.sprCursor):
            self.cursor = 0

    def goIn(self):
        self.music.Stop()
        self.app = App('127.0.0.1', 8080, self.width, self.height)
        self.app.Run()

if __name__ == "__main__":
    menu = Menu()
    menu.run()
