from PySFML import sf

class ProgressBar:
    FrameL = sf.Image()
    FrameL.LoadFromFile('./Graphics/Jauges/Jauge_start.png')

    FrameR = sf.Image()
    FrameR.LoadFromFile('./Graphics/Jauges/Jauge_end.png')

    Empty = sf.Image()
    Empty.LoadFromFile('./Graphics/Jauges/Jauge_empty.png')

    Full = sf.Image()
    Full.LoadFromFile("./Graphics/Jauges/Jauge_full.png")

    def __init__(self, width, max, value = 0):
        self.width = width
        self.max = max
        self.value = max if value > max else value

        self.sprFrameL = sf.Sprite(ProgressBar.FrameL)
        self.sprFrameR = sf.Sprite(ProgressBar.FrameR)
        self.sprEmpty = sf.Sprite(ProgressBar.Empty)
        self.sprFull = sf.Sprite(ProgressBar.Full)

        self.sprFrameR.SetX(self.width + ProgressBar.FrameL.GetWidth())

    def Draw(self, window):
        self.value = self.value % self.max
        xLim = self.value * 1.0 / self.max * self.width / ProgressBar.Empty.GetWidth()

        window.Draw(self.sprFrameL)
        window.Draw(self.sprFrameR)
        for x in xrange(int(self.width * 1.0 / ProgressBar.Empty.GetWidth())):
            if x <= xLim:
                self.sprFull.SetX(x * ProgressBar.Full.GetWidth() + ProgressBar.FrameL.GetWidth())
                window.Draw(self.sprFull)
            else:
                self.sprEmpty.SetX(x * ProgressBar.Empty.GetWidth() + ProgressBar.FrameL.GetWidth())
                window.Draw(self.sprEmpty)

