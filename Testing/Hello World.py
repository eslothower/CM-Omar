from SimpleCV import Camera, Display, Image
import time

cam = Camera()
display = Display()

img = cam.getImage()
#img.drawText("Hello World")
img.save(display)

