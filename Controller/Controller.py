from random import randrange, choice
from Player import Player
from Util import Box, Obstacle, Coin
import sys
sys.path.append('./')
from Network import MyServer, Protocol
import Platform
from math import log

_Protocol = Protocol.TCP

class Controller(MyServer.MyServer(_Protocol)):


    def __init__(self, team, addr, port, width=800, height=600):
        #self.obstacles = [Obstacle(0, randrange(30,120), choice(Obstacle.Sprites))]
        super(Controller, self).__init__(1337 + team, -1)
        self.width = width
        self.height = height
        self.team = team
        self.addr = addr
        self.port = port

        self.ls_action['JUMP'] = self._jump
        self.ls_action['LEFT'] = self._left
        self.ls_action['RIGHT'] = self._right
        self.ls_action['BONUS'] = self._bonus
        self.ls_action['PLATFORM'] = self._platform
        self.platforms = []
        self.obstacles = []
        self.coins = []
        self.window = GameWindow(width, height)
        self.player = Player(200, 0, team, self.window)
        self.running = True

        self.always_alive = []
        self.disconnect(self.listener)
        self.inputs = []

        self.GameOver = False

        #self.start()

        #s = _Protocol.Socket()
        #s.connect(self.addr, self.port)
        #self.add_message(s, 'CONNECT ' + str(self.team) + ' ' + str(1337 + team))

        for i in range(14):
           self.GenerateObstacle()

        for i in range(6):
           self.GenerateCoin()

    def GenerateObstacle(self):
        delta_x = log(self.window.dx*20) * 40
        if len(self.obstacles) > 0:
            lastObst = self.obstacles[-1]
            x, y = lastObst.GetBox().x + lastObst.GetBox().width + randrange(int(delta_x*1), int(delta_x*1.2)),  self.height + randrange(0,100) - 150
        else:
            x, y = 200, 300
        obstacle = Obstacle(x, y-50, choice(Obstacle.Sprites))
        self.obstacles.append(obstacle)

    def GenerateCoin(self):
        delta_x = log(self.window.dx*10) * 40
        if len(self.coins) > 0:
            lastObst = self.coins[-1]
            x, y = lastObst.GetBox().x + lastObst.GetBox().width + randrange(int(delta_x*1), int(delta_x*1.2)),  self.height + randrange(0,100) - 150
        else:
            x, y = 200, 300
        coin = Coin(x, y - 200, 2)
        self.coins.append(coin)

    def Update(self):
        self.window.Update()
        self.player.Update(self.obstacles + self.platforms, self.coins)

        # If the player gets out of the window : GAME OVER
        self.GameOver = self.player.x <= self.window.x or self.player.y >= self.window.y + self.window.height
        if self.GameOver:
            self.stop()

        # Testing collisions
        if len(self.obstacles) > 0:
            if not self.window.GetBox().collides(self.obstacles[0].GetBox()):
                self.obstacles.pop(0)
                self.GenerateObstacle()

        if len(self.coins) > 0:
            if not self.window.GetBox().collides(self.coins[0].GetBox()):
                self.coins.pop(0)
                self.GenerateCoin()

        if len(self.platforms) > 0:
            if not self.window.GetBox().collides(self.platforms[0].GetBox()):
                self.platforms.pop(0)

    def _jump(self, sock = None):
        print "Jump"
        self.player.Jump()

    def _left(self, sock = None):
        print 'Left'
        self.player.Left()

    def _right(self, sock = None):
        print 'Right'
        self.player.Right()

    def _bonus(self, sock, num, x, y):
        print 'Bonus'

    def _platform(self, sock, x1, y1, x2, y2):
        dx, dy = self.window.x, self.window.y
        # print "window offset: ", dx, dy
        # print "haut gauche: ", x1, y1
        # print "bas droite: ", x2, y2
        self.platforms.append(Platform.Platform(int(x1 + dx), int(y1 + dy), int(x2 + dx), int(y2 + dy)))

class GameWindow(object):
    default_position = 0., 0.
    default_speed = 3., 0.
    default_acceleration = 0.01, 0.

    def __init__(self, width, height, position = default_position, speed = default_speed, acceleration = default_acceleration):
        self.x, self.y = position
        self.dx, self.dy = speed[0], speed[1]
        self.accX, self.accY = acceleration[0], acceleration[1]
        self.width, self.height = width, height

    def Update(self):
        self.dx += self.accX
        self.dy += self.accY
        self.x += self.dx
        self.y -= self.dy

    def GetBox(self):
        return Box(self.x, self.y, self.width, self.height)

    def SetAcceleration(self, acceleration):
        self.acceleration = acceleration

    def AddAcceleration(self, dAccel):
        self.acceleration += dAccel

