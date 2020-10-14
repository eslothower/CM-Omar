from SimpleCV import Image, Camera, Color
import sys

cam = Camera()

img = cam.getImage()

circles = img.findCircle(canny=10,thresh=100)

circles = circles.sortArea()

circles.draw(width=4)

circles[0].draw(color=Color.BLACK, width=4)

img_with_circles = img.applyLayers()

edges_in_image = img.edges(t2=400)

final = img.sideBySide(edges_in_image.sideBySide(img_with_circles)).scale(0.5)

edges_in_image.show()

chooseToSave = ""

while chooseToSave != "y" or chooseToSave != "n":
    chooseToSave = raw_input("Would you like to save this image? y or n. ")
    if chooseToSave == "y":
        fileName = raw_input("What would you like to name this file? Do not add the file extension to your response. ")
        filePath = raw_input("Where would you like to store this file? If you would like to store it in the default location, respond with 'default'. ")
        
        if filePath == "Default":
                final.save("/home/pi/Desktop/Eli Slothower OMR Project/Testing/Images/" + fileName + ".jpg")
        else:
                final.save(filePath + fileName + ".jpg")
        exit
    elif chooseToSave == "n":
        sys.exit()
    else:
        print("Please choose respond with either 'y' or 'n'.")

print("Success!")
