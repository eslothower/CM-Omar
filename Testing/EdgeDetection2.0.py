from SimpleCV import Camera, Display, Image

cam = Camera()
display = Display()

while display.isNotDone():
    img = cam.getImage()
    edges = img.edges(t2=400)
    blobs = edges.findBlobs()

    if blobs:
        circles = blobs.filter([b.isCircle(0.2) for b in blobs])
        img.drawCircle((blob[0].x, blob[0].y), SimpleCV.Color.BLUE,3)

blobs.show()
