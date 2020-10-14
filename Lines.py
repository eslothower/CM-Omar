from SimpleCV import Camera, Display, Image


cam = Camera()
display = Display()

img = cam.getImage()
lines = img.findLines()
lines.draw(width=5)
img.show()


