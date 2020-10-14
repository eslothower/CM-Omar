from SimpleCV import Camera, Color, Image
import time

cam = Camera()

img = cam.getImage()

black_distance = img.colorDistance(Color.WHITE).invert()

blobs = black_distance.findBlobs()

blobs.draw(color=Color.PUCE, width=3)
black_distance.show()

img.addDrawingLayer(black_distance.dl())
img.show()

