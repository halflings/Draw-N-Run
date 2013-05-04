from Util import Animation, Box
from PySFML import sf
class State(object):

    def __init__(self, name, animation_path):
        self.name = name
        self.animation = Animation(animation_path)

    def Reset(self):
        self.animation.Reset()

    def GetSprite(self):
        return self.animation.GetSprite()

class Player(object):

    GRAVITY = -.9
    DEFAULT_SPEED_X, DEFAULT_SPEED_Y = 3.0, 0
    DEFAULT_ACC = 0.01

    names = ['Drawer', 'Rival']
    states = ['Run', 'Jump_up', 'Hurt']

    jump_sound= sf.Music()
    jump_sound.OpenFromFile('Jump_start.ogg')
    jump_sound.Initialize(4, 22000)

    def __init__(self, x=10, y=400, id = 0, window = None, accX = DEFAULT_ACC):
        self.x, self.y = x, y
        self.dx, self.dy = Player.DEFAULT_SPEED_X, Player.DEFAULT_SPEED_Y
        self.dxBase = Player.DEFAULT_SPEED_X
        self.accX, self.accY = accX, Player.GRAVITY

        self.window = window

        self.name = Player.names[id % 2]

        self.states = dict()
        for state in Player.states:
            self.states[state] = State(state, './Graphics/Characters/{}/{}'.format(self.name, state) )
        self.state = self.states['Run']
        self.run = ''

        self.point = 0


    def GetSprite(self):
        return self.state.GetSprite()

    def GetBox(self):
        size = self.state.GetSprite().GetSize()
        return Box(self.x, self.y, *size)

    def Update(self, obstacles, coins):
        # print "At update", self.x, self.y
        # print "Speeds", self.dx, self.dy

        if self.run == 'L' or ('l' in self.run and self.state == self.states['Jump_up']):
            self.dx = self.dxBase - 4
        elif self.run == 'R' or ('r' in self.run and self.state == self.states['Jump_up']):
            self.dx = self.dxBase + 4
        else:
            self.dx = self.dxBase

        if self.state == self.states['Run']:
            if self.run == 'L':
                self.run = 'llllll'
            elif self.run == 'R':
                self.run = 'rrrrrrr'
            else:
                if self.run:
                    self.run = self.run[1:]

        #We update the player's position
        self.dxBase += self.accX
        self.dy += self.accY

        self.x += self.dx
        # if self.window:
        #     self.x = min(self.x, self.window.x + self.window.GetBox().width/2)
        self.y -= self.dy

        #We check if there was any collision
        box = self.GetBox()

        for obstacle in obstacles:
            obstBox = obstacle.GetBox()
            if box.collides(obstBox):
                dx = self.x + box.width - obstBox.x
                dy = self.y + box.height - obstBox.y
                if dx > 0 and dx < 5 and dy >  3:
                    self.x = obstBox.x - box.width

                if dy >= 0 and dx - box.width > 0 :
                    self.y = obstBox.y - box.height
                    self.dy = 0
                    if self.state != self.states['Run']:
                        self.ChangeState(self.states['Run'])
        for c in coins:
            obstBox = c.GetBox()
            if box.collides(obstBox):
                self.point += c.value
                c.destroy()

    def ChangeState(self, state):
        state.Reset()
        self.state = state

    def Jump(self, speed=(0, 15)):
        if self.state != self.states['Jump_up']:
            Player.jump_sound.Play()
            self.dxBase += speed[0]
            self.dy += speed[1]
            self.ChangeState(self.states['Jump_up'])

    def Left(self, dx = -2):
        self.run = 'L'

    def Right(self, dx = 2):
        self.run = 'R'

