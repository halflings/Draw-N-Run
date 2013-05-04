from PySFML import sf

class Bonus:
    double_jump = 0

    Background = sf.Image()
    Background.LoadFromFile("./Graphics/Jauges/Frame.png")

    Bonus = []
    Bonus += [sf.Image()]
    Bonus[0].LoadFromFile('./Graphics/Items/Double_jump.png')

    def __init__(self, id, type = None):
        self.id = id
        self.type = type
        self.sprBackground = sf.Sprite(Bonus.Background)
        self.sprBonus = sf.Sprite(sf.Image())

        self.sprBonus.SetX((Bonus.Background.GetWidth() + 5) * self.id + 7)
        self.sprBonus.SetY(7);
        self.sprBackground.SetX((Bonus.Background.GetWidth() + 5) * self.id)

    def Draw(self, window):
        window.Draw(self.sprBackground)

        if self.type is not None:
            self.sprBonus.SetImage(Bonus.Bonus[self.type])
            window.Draw(self.sprBonus)

