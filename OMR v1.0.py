from SimpleCV import Camera, Image, Display, Color, Blob, Feature, FeatureSet, ShapeContextDescriptor
import math, time, sys


#Initialize Camera
cam = Camera()

#Initialize Display
display = Display()

iteration = 0
centerCircleCoordinate = []

while display.isNotDone():

    #Used to keep track of which iteration of captured photo it is on 
    iteration += 1
    print("ITERATION: " + str(iteration))

    #Take photo
    img = cam.getImage().invert()

    #Find blobs from edges
    blobs = img.findBlobs()

    #Check to see how many blobs detected
    length = len(blobs)

    if length > 0:
        
        
        #Find all the necessary coordinates of the staff, such as the coordinates and what angle it's tilted at
        tpLftCd = blobs[0].topLeftCorner()
        tpRtCd = blobs[0].topRightCorner()
        btmLftCd = blobs[0].bottomLeftCorner()
        btmRtCd = blobs[0].bottomRightCorner()
        center = blobs.coordinates()
        angle = blobs.angle()
        height = blobs.height()
        width = blobs.width()

        print("Blobs: " + str(length))
        print("")
        print("Top Left Corner: " + str(tpLftCd))
        print("Top Right Corner: " + str(tpRtCd))
        print("Center: " + str(center))
        print("Bottom Left Corner: " + str(btmLftCd))
        print("Bottom Right Corner: " + str(btmRtCd))
        print("Angle: " + str(angle))
        print("Height: " + str(height))
        print("Width: " + str(width))
        

        #if the entire staff line and notes are detected as one blob (as it should), then transform it, crop it, etc.
        if length == 1:

            #Transform image (BROKEN WITH .COLORDISTANCE()
            #transformed = img.rotate(angle).crop(CORNER COORDINATES GO HERE)


            #Detect Circles
            dist = img.colorDistance(Color.WHITE).dilate(3)
            dist = dist.invert()
            circles = dist.findBlobs()

            circleAmount = len(circles)
            circleCoordinatesArray = []

            if circleAmount > 0:

                i = 0

                for circle in circles:
                    circleCoordinatesArray.append(circles[i].coordinates())
                    print(str(circleCoordinatesArray[i]))
                    i += 1

                #Dividing staff line into 9 parts algorithm
                nineParts = (btmLftCd[1] - tpLftCd[1])/8
                1 = tpLftCd[1]
                2 = 1 + nineParts
                3 = 2 + nineParts
                4 = 3 + nineParts
                5 = 4 + nineParts
                6 = 5 + nineParts
                7 = 6 + nineParts
                8 = 7 + nineParts
                9 = btmLftCd[1]

                

                

                






                #Draw dots for reference
                drawnCircleSize = 5
                fill = True

                img.dl().circle((338, 315), drawnCircleSize, Color.RED, filled = fill)
                img.dl().circle((441, 208), drawnCircleSize, Color.RED, filled = fill)
                img.dl().circle((232, 270), drawnCircleSize, Color.RED, filled = fill)
                img.dl().circle((120, 340), drawnCircleSize, Color.RED, filled = fill)

                img.dl().circle((50, 176), drawnCircleSize, Color.GREEN, filled = fill)
                img.dl().circle((50, 200), drawnCircleSize, Color.GREEN, filled = fill)
                img.dl().circle((50, 224), drawnCircleSize, Color.GREEN, filled = fill)
                img.dl().circle((50, 248), drawnCircleSize, Color.GREEN, filled = fill)
                img.dl().circle((50, 272), drawnCircleSize, Color.GREEN, filled = fill)
                img.dl().circle((50, 296), drawnCircleSize, Color.GREEN, filled = fill)
                img.dl().circle((50, 320), drawnCircleSize, Color.GREEN, filled = fill)
                img.dl().circle((50, 344), drawnCircleSize, Color.GREEN, filled = fill)
                img.dl().circle((50, 369), drawnCircleSize, Color.GREEN, filled = fill)
                
                #circles.show()
                img.show()

##                chooseToSave = ""
##                while chooseToSave != "y" or chooseToSave != "n":
##                    chooseToSave = raw_input("Would you like to save this image? y or n. ")
##                    if chooseToSave == "y":
##                        fileName = raw_input("What would you like to name this file? Do not add the file extension to your response. ")
##                        filePath = raw_input("Where would you like to store this file? If you would like to store it in the default location, hit enter. ")
##                        
##                        if filePath == "":
##                                img.save("/home/pi/Desktop/Eli Slothower OMR Project/Testing/Images/" + fileName + ".jpg")
##                        else:
##                                img.save(filePath + fileName + ".jpg")
##                        sys.exit()
##                    elif chooseToSave == "n":
##                        sys.exit()
##
##                    else:
##                        print("Please choose respond with either 'y' or 'n'.")
##
##                print("Successfully saved!")

            else:
                print("NO CIRCLES DETECTED")


            
            

            
        else:
            print("MORE THAN 1 BLOB DETECTED - STAFF LINE DETECTION STEP")
            
    else:
        print("NO STAFF LINE DETECTED")
        

    #Slow down the printed results to the console
    print("----------------------------------------------------------------------------")
    time.sleep(1.5)
    exit





    

