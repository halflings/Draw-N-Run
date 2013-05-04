from PySFML import sf

import Input
import Network

import time

from Background import Background
from Bonus import Bonus
from ProgressBar import ProgressBar
from Controller import Controller

class App(object):
    minecrafter = sf.Font()
    minecrafter.LoadFromFile('minecrafter.ttf')

    music= sf.Music()
    music.OpenFromFile('omfgdogs.ogg')
    music.Initialize(4, 22000)
    music.SetVolume(60)


    gameover_sound = sf.Music()
    gameover_sound.OpenFromFile('Game_over.ogg')
    gameover_sound.Initialize(4, 22000)

    def __init__(self, addr, port, width = 800, height = 600, players = 2):
        App.music.Play()
        self.addr = addr
        self.port = port
        self.renderWindow = sf.RenderWindow(sf.VideoMode(width, height, 32), "Cartoon Runner")
        self.renderWindow.SetFramerateLimit(60)
        self.renderWindow.ShowMouseCursor(False)

        self.height = height
        self.width = width

        self.players = players

        self.score = 0

        #Input
        # self.input = Input.InputServer(Network.Protocol.TCP)(0, '127.0.0.1', 8080, -1)
        # self.input.start()

        #Other backgrounds
        imgBackground = sf.Image()
        imgBackground.LoadFromFile("./Graphics/Background/World1_background.png")
        imgClouds = sf.Image()
        imgClouds.LoadFromFile('./Graphics/Background/World1_clourds.png')
        imgPlatforms = sf.Image()
        imgPlatforms.LoadFromFile('./Graphics/Background/World1_platforms.png')
        self.lsBackground = []
        self.lsBackground.append(Background(imgBackground, 0))
        self.lsBackground.append(Background(imgClouds, -0.2))
        self.lsBackground.append(Background(imgPlatforms, -0.4))

        self.cursorImg = sf.Image()
        self.cursorImg.LoadFromFile('./Graphics/Cursors/Pencil.png')
        self.cursor = sf.Sprite(self.cursorImg)

        #Bonuses
        self.lsBonus = [Bonus(id) for id in xrange(3)]
        self.lsBonus[0].type = 0
        self.lsBonus[2].type = 0

        self.dead = 0

        #PosX ?
        self.posX = 0

        self.progressBar = ProgressBar(350, 250, 42)

        self.lsController = []

        for i in range(players):
            self.lsController.append( Controller.Controller(i, self.addr, self.port, width/players, height/players) )

        self.running = False

        self.winner = 0
        self.click = None

        self.rectView = self.renderWindow.GetView().GetRect()


    def Update(self):
        # Updating the model

        for c in self.lsController:
            c.Update()

        if self.lsController[0].GameOver and not self.lsController[1].GameOver:
            self.winner = 1
        elif self.lsController[1].GameOver and not self.lsController[0].GameOver:
            self.winner = 0

        if self.lsController[0].GameOver and self.lsController[1].GameOver:
            self.GameOver(self.winner)

        # Clearing the window
        self.renderWindow.Clear()

        view = sf.View(self.rectView)
        self.renderWindow.SetView(view)

        sizeY = self.renderWindow.GetHeight() * 1.0 / len(self.lsController)
        view = sf.View(sf.FloatRect(0, 0, self.renderWindow.GetWidth() , len(self.lsController) * self.renderWindow.GetHeight()))
        self.renderWindow.SetView(view)

        self.renderWindow.SetView(sf.View(self.rectView))

        sizeY = self.renderWindow.GetHeight() * 1.0 / len(self.lsController)

        for i, c in enumerate(self.lsController):
            y = i * sizeY
            for background in self.lsBackground:
                background.Draw(self.renderWindow,   self.posX, y)

            win = c.window.GetBox()
            # Displaying obstacles
            for obs in c.obstacles:
                sprite = obs.GetSprite()
                sprite.SetPosition(int(obs.x - win.x), int(obs.y - win.y + i*sizeY))
                self.renderWindow.Draw(sprite)

            for obs in c.coins:
                sprite = obs.GetSprite()
                sprite.SetPosition(int(obs.x - win.x), int(obs.y - win.y + i*sizeY))
                self.renderWindow.Draw(sprite)


            # Displaying the player
            player = c.player
            sprite = player.GetSprite()
            sprite.SetPosition(int(player.x - win.x), int(player.y - win.y + i*sizeY))
            self.renderWindow.Draw(sprite)

            self.ShowScore(c.player.point, y)

            #Displaying platforms
            for plat in c.platforms:
                sprite = plat.GetSprite()
                # box = plat.GetBox()
                # bX = box.x - win.x
                # bY = box.y - win.y
                # sprite.SetPosition(int(bX), int(bY))
                #self.renderWindow.Draw(sprite)


        #Displaying the bonuses
        self.posX += 3
        view = sf.View(self.rectView)
        view.Move(-10, -10)
        self.renderWindow.SetView(view)
        # self.progressBar.Draw(self.renderWindow)

        view.Move(10 - self.renderWindow.GetWidth() + 10 + 3 * (Bonus.Background.GetWidth() + 5), 0)
        self.renderWindow.SetView(view)
        for bonus in self.lsBonus:
            pass#bonus.Draw(self.renderWindow)

        #Displaying the cursor and score
        self.renderWindow.SetView(sf.View(self.rectView))

        input_ = self.renderWindow.GetInput()
        c, d = input_.GetMouseX(), input_.GetMouseY()
        size = self.cursor.GetSize()
        self.cursor.SetPosition(c - size[0] / 2., d - size[1] / 2.)
        self.renderWindow.Draw(self.cursor)

        self.renderWindow.Display()

    def EventListening(self):
        ##############
        ##  EVENTS  ##
        ##############
        c = self.lsController[0]
        c2 = self.lsController[-1]
        event = sf.Event()
        while self.renderWindow.GetEvent(event):
            if event.Type == sf.Event.Closed:
                App.music.Stop()
                self.Stop()

            if event.Type == sf.Event.KeyPressed:
                if event.Key.Code == sf.Key.Escape:
                    self.Stop()

                #if event.Key.Code in [sf.Key.Up, sf.Key.Space]:
                    #self.input.jump()

                #if event.Key.Code == sf.Key.Left:
                    #self.input.left()

                #if event.Key.Code == sf.Key.Right:
                    #self.input.right()

                if event.Key.Code in [sf.Key.Up, sf.Key.Space]:
                    c._jump(None)

                if event.Key.Code == sf.Key.Left:
                    c._left(None)

                if event.Key.Code == sf.Key.Right:
                    c._right(None)


                if event.Key.Code in [sf.Key.Z, sf.Key.W]:
                    c2._jump(None)

                if event.Key.Code in [sf.Key.A, sf.Key.Q]:
                    c2._left(None)

                if event.Key.Code == sf.Key.D:
                    c2._right(None)

            if event.Type == sf.Event.MouseButtonPressed:
                x, y = event.MouseButton.X, event.MouseButton.Y

                if y <= self.renderWindow.GetHeight() / 2.0:
                    self.click = x, y
                    # cursor = x, y
                else:
                    self.click = None

                    #if event.MouseButton.Button == sf.Mouse.Left:
                        #self.input.bonus(0, (x, y - self.renderWindow.GetHeight()))
                    #if event.MouseButton.Button == sf.Mouse.Middle:
                        #self.input.bonus(1, (x, y - self.renderWindow.GetHeight()))
                    #if event.MouseButton.Button == sf.Mouse.Right:
                       #self.input.bonus(2, (x, y - self.renderWindow.GetHeight()))

                    if event.MouseButton.Button == sf.Mouse.Left:
                        c._bonus(None, 0, x, y - self.renderWindow.GetHeight())
                    if event.MouseButton.Button == sf.Mouse.Middle:
                        c._bonus(None, 1, x, y - self.renderWindow.GetHeight())
                    if event.MouseButton.Button == sf.Mouse.Right:
                        c._bonus(None, 2, x, y - self.renderWindow.GetHeight())


            if event.Type == sf.Event.MouseButtonReleased:
                x, y = event.MouseButton.X, event.MouseButton.Y

                if y <= self.renderWindow.GetHeight() / 2.0 and self.click:
                    #self.input.platform(self.click, (x, y))
                    #input_ = self.renderWindow.GetInput()
                    #a, b = self.click
                    #c, d = input_.GetMouseX(), input_.GetMouseY()
                    #platform = Platform.Platform(a, b, c, d)
                    #self.renderWindow.Draw(platform.GetSprite())

                    c._platform(None, self.click[0], self.click[1], x, y)
                    #input_ = self.renderWindow.GetInput()
                    #a, b = self.click
                    #c, d = input_.GetMouseX(), input_.GetMouseY()
                    #platform = Platform.Platform(a, b, c, d)
                    #self.renderWindow.Draw(platform.GetSprite())

                self.click = None

    def GameOver(self, i):
        App.music.Stop()

        txt = sf.String( "GAME OVER ! Player {} wins".format(i+1), App.minecrafter, 40 )
        x, y = self.renderWindow.GetWidth() / 2 - 400,  self.renderWindow.GetHeight()/2 - 80
        score = sf.String( "with {} points".format(self.lsController[i].player.point), App.minecrafter, 35 )
        press_enter = sf.String( "Press ENTER to restart.", App.minecrafter, 35 )
        txt.SetPosition(int(x), int(y))
        score.SetPosition(int(x), int(y+90))
        press_enter.SetPosition(int(x), int(y+140))

        self.renderWindow.Draw(sf.Shape.Rectangle(0, 0, self.renderWindow.GetWidth(), self.renderWindow.GetHeight(),
        sf.Color(42, 42, 42)))
        self.renderWindow.Draw(txt)
        self.renderWindow.Draw(score)
        # self.renderWindow.Draw(press_enter)

        App.gameover_sound.Play()
        # self.renderWindow.Clear()

        self.renderWindow.Display()


        sf.Sleep(5.5)
        App.gameover_sound.Stop()
        self.Stop()

    def ShowScore(self, score, offset):
        scoreTxt = sf.String( "Score : {}".format(str(score).zfill(8)), App.minecrafter, 14 )
        x, y = self.renderWindow.GetWidth() / 2 - 350,  20 + offset
        scoreTxt.SetPosition(int(x), int(y))
        self.renderWindow.Draw(scoreTxt)


    def Run(self):
        self.running = True

        while self.running:
            self.EventListening()
            self.Update()

    def Stop(self):
        self.renderWindow.Close()
        self.running = False
        # self.input.end()
        # self.input.stop()
        # self.input.join()


if __name__ == '__main__':
    IPTURPIF = '134.214.199.157'
    app = App('127.0.0.1', 8080, 1400, 800)
    app.Run()
