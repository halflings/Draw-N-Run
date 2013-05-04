# Include the PySFML extension
from PySFML import sf


# Create a graphical string to display
text = sf.String("Hello SFML")
image = sf.Image()

if(not(image.LoadFromFile("perso.png"))):
    window.Draw(sf.String("Image not found"))

sprite = sf.Sprite(image);
sprite.SetPosition(200.0, 100.0)
sprite.Rotate(60)

bgImg = sf.Image()
bgImg.LoadFromFile("bg.png")
bg = sf.Sprite(bgImg)
bg.SetPosition(0, 0)

# Create the main window
window = sf.RenderWindow(sf.VideoMode(int(bg.GetSize()[0]), int(bg.GetSize()[1])), "PySFML test")

# Start the game loop
running = True
while running:
    event = sf.Event()
    while window.GetEvent(event):
        if event.Type == sf.Event.Closed:
            running = False

    #Get elapsed time
    ElapsedTime = window.GetFrameTime();

    #Move the sprite
    if (window.GetInput().IsKeyDown(sf.Key.Left)):  sprite.Move(-100 * ElapsedTime, 0)
    if (window.GetInput().IsKeyDown(sf.Key.Right)): sprite.Move( 100 * ElapsedTime, 0)
    if (window.GetInput().IsKeyDown(sf.Key.Up)):    sprite.Move(0, -100 * ElapsedTime)
    if (window.GetInput().IsKeyDown(sf.Key.Down)):  sprite.Move(0,  100 * ElapsedTime)

    #Rotate the sprite
    if (window.GetInput().IsKeyDown(sf.Key.Add)):      sprite.Rotate(-100 * ElapsedTime)
    if (window.GetInput().IsKeyDown(sf.Key.Subtract)): sprite.Rotate( 100 * ElapsedTime)

    # Clear screen, draw the text, and update the window
    window.Clear()
    #window.Draw(text)
    window.Draw(bg)
    window.Draw(sprite)
    window.Display()
