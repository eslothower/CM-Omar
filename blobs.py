from SimpleCV import Image, Camera, Color
import sys

cam = Camera()

#img = Image("/home/pi/Desktop/Eli Slothower OMR Project/Testing/Images/StaffLines.png")
img= cam.getImage()


edges_in_image = img.edges(t2=400)

final = edges_in_image.findBlobs().show()



#final = img.sideBySide(edges_in_image.sideBySide(blob_img))
#final.drawText("Input", y=100, x=375)
#final.drawText("Output", y=100, x=1200)
#edges_in_image.findCorners(maxnum=5).show()
#final.show()

chooseToSave = ""
while chooseToSave != "y" or chooseToSave != "n":
    chooseToSave = raw_input("Would you like to save this image? y or n. ")
    if chooseToSave == "y":
        fileName = raw_input("What would you like to name this file? Do not add the file extension to your response. ")
        filePath = raw_input("Where would you like to store this file? If you would like to store it in the default location, hit enter. ")
        
        if filePath == "":
                final.save("/home/pi/Desktop/Eli Slothower OMR Project/Testing/Images/" + fileName + ".jpg")
        else:
                final.save(filePath + fileName + ".jpg")
        sys.exit()
    elif chooseToSave == "n":
        sys.exit()

    else:
        print("Please choose respond with either 'y' or 'n'.")

print("Success!")
