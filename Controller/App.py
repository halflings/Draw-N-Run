from PySFML import sf
from View import *
import time

class App(object):

    def __init__(self, width = 800, height = 600):
        self.view = View("../test/bg.png", width, height)

    def Run(self):
        while self.view.renderWindow.IsOpened():
            event = sf.Event()
            while self.view.renderWindow.GetEvent(event):
                if event.Type == sf.Event.Closed:
                    self.view.renderWindow.Close()
            self.view.Update()
            time.sleep(0.08)

if __name__ == '__main__':
    app = App(800, 600)
    app.Run()
