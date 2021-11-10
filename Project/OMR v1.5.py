from SimpleCV import Camera, Image, Display, Color, Blob
from datetime import datetime
from time import sleep
import math, sys, pygame, pygame.midi, os, random



    

def startupChime():
    try:
        #Welcome sound
        player.note_on(76,0) # plays a silent sound to prevent shortened first note (timidity plays the first played note short for some reason, so I'm doing that with a silent one so that the real first note will play for the correct duration)
        sleep(0)
        player.note_off(76,0)
        sleep(1)

        player.note_on(95,volume) 
        sleep(.1)
        player.note_off(95,volume)

        player.note_on(98,volume) 
        sleep(.1)
        player.note_off(98,volume)

        player.note_on(100,volume) 
        sleep(.1)
        player.note_off(100,volume)

        player.note_on(102,volume) 
        sleep(.05)
        player.note_off(102,volume)

        player.note_on(105,volume) 
        sleep(1)
        player.note_off(105,volume)
    except:
        print("You must enter 'timidity -iA' into the terminal before running. Please enter that into the terminal first and then run the program again.")
        sys.exit()

def displayStartupInfo():
    print("Omar v1.0 (" + str(os.path.dirname(os.path.abspath(__file__))) + ")")
    print("Author: Eli Slothower")
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
    print("Hello!\n")
    print("I'm Omar. I'm an optical music recognition algorthim. I can be used to play back sheets of music that I scan in using the webcam. I can also play the music back to you in a variety of instruments, with more coming very soon!\n")
    sleep(2)
    print("Here are your current settings\n\tInstrument: Piano\n\tVolume: High\n\tTempo: .25 seconds/beat\n")
    sleep(2)



#Initialize Camera
cam = Camera()

#Initialize Display
display = Display()

#Used to keep track of which iteration of captured photo it is on 
iteration = 0

#Messages displayed to the user at random while the camera is initializing
messages = ["Warming the camera up...", "INITIALIZING SOFTWARE...", "Spinning up the hamster...",  "Programming the flux capacitor...", "Downloading more RAM...", "Retreiving information from the fifth dimension...", "Please stand by..."]



#Setup midi player
#MUST DO 'timidity -iA' IN TERMINAL BEFORE RUNNING. DO NOT INCLUDE THE APOSTROPHES
TIMIDITYPORT = 3
TIMIDITYINSTRUMENT = 2 #There are 127 instruments to play from
number = 90
volume = 127 #127 is max volume
velocity = .25

global player
pygame.midi.init()
player = pygame.midi.Output(TIMIDITYPORT) 
player.set_instrument(TIMIDITYINSTRUMENT)

startupChime()

displayStartupInfo()



while True:

    settingsInput = ""

    while settingsInput.strip() != "4":

        settingsInput = raw_input("What settings would you like to change? Enter the number that corresponds to your selection, and then hit enter.\n\t1. Instrument\n\t2. Volume\n\t3. Tempo\n\t4. Exit Settings\n")

        print("\n" * 100)

        if settingsInput.strip() == "1":
            print("What instrument would you like to set it to? Enter the number that corresponds to your selection, and then hit enter.")
            print("\t1. Piano")
            print("\t2. Xylophone")
            print("\t3. Bells")
            print("\t4. Tin Can")
            print("\t5. Steel Drum")

            instrumentInput = raw_input()
            
            while True:
                if instrumentInput.strip() == "1":
                    TIMIDITYINSTRUMENT = 2
                    break
                elif instrumentInput.strip() == "2":
                    TIMIDITYINSTRUMENT = 10
                    break
                elif instrumentInput.strip() == "3":
                    TIMIDITYINSTRUMENT = 14
                    break
                elif instrumentInput.strip() == "4":
                    TIMIDITYINSTRUMENT = 113
                    break
                elif instrumentInput.strip() == "5":
                    TIMIDITYINSTRUMENT = 114
                    break
                else:
                    print("Please enter a valid digit, such as '1' and hit enter.")
                    instrumentInput = raw_input()
                    


            player.set_instrument(TIMIDITYINSTRUMENT)
            print("Your instrument selection has been updated.\n\n")
            sleep(1)
                

                
        elif settingsInput.strip() == "2":
            print"What would you like to set the volume to? Enter the number that corresponds to your selection, and then hit enter."
            print"\t1. Low"
            print"\t2. Medium"
            print"\t3. High"

            volumeInput = raw_input()
            while True:
                if volumeInput.strip() == "1":
                    volume = 30
                    break
                elif volumeInput.strip() == "2":
                    volume = 75
                    break
                elif volumeInput.strip() == "3":
                    volume = 127
                    break
                else:
                    print("Please enter a valid digit, such as '1' and hit enter.")
                    volumeInput = raw_input()
                

            print("Your volume has been updated.\n\n")
            sleep(1)

        elif settingsInput.strip() == "3":
            print"How fast would you like the song to play? Enter the number that corresponds to your selection, and then hit enter."
            print"\t1. Slow"
            print"\t2. Normal"
            print"\t3. Fast"

            tempoInput = raw_input()
            while True:
                if tempoInput == "1":
                    velocity = 0.5
                    break
                elif tempoInput == "2":
                    velocity = 0.1
                    break
                elif tempoInput == "3":
                    velocity = 0.05
                    break
                else:
                    print("Please enter a valid digit, such as '1' and hit enter.")
                    tempoInput = raw_input()

            print("The tempo has been updated.\n\n")
            sleep(1)

        elif settingsInput.strip() == "4":
            
            randomMessage = random.randint(0, (len(messages)-1))
            print(messages[randomMessage] + "\n")

            sleep(1)

            print("Time to scan your music! Please put your music sheet where I can see it, and make sure it is positioned correctly. When you are ready for me to scan it, hit the spacebar.\n")

            sleep(1)

            keyboardPressed = False
            while keyboardPressed == False:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.KEYUP:
                        keyboardPressed = True
                        break
                liveImg = cam.getImage()
                liveImg.show()


            iteration += 1
            print("Iteration: " + str(iteration))

            #Take photo
            img = cam.getImage().invert()

            

            #Find blobs from edges
            blobs = img.findBlobs()

            #Check to see how many blobs detected
            length = len(blobs)

            #If any blobs were detected
            if length > 0:
                
                
                #Find all the necessary coordinates of the staff
                tpLftCd = blobs[0].topLeftCorner()
                btmLftCd = blobs[0].bottomLeftCorner()
                center = blobs.coordinates()



                

                #if the entire staff line and notes are detected as one blob (as it should), then move to looking for the cirles
                if length == 1:

                        #Transforming image (BROKEN WITH .COLORDISTANCE(). It makes the image completely unrecognizable. Looks like corrupted data
                        #transformed = img.rotate(angle).crop(CORNER COORDINATES GO HERE) #Broken when using .colorDistance, as described in the line above


                        #Detect circles by looking dilating, which gets rid of the staff lines, then colorDistance makes it look for anything white. And since the image is inverted, the only white things left on the image at this point are the circles
                        dist = img.colorDistance(Color.WHITE).dilate(3)
                        #Invert again, since findBlobs prioritizes black color, while colorDistanance prioriizes white color
                        dist = dist.invert()
                        circles = dist.findBlobs()

                        
                        #Populate array with the amount of circles found
                        circleAmount = len(circles)

                        #If any circles are found, continue
                        if circleAmount > 0:

                                i = 0
                                
                                #Array that is populated with the coordinates (tuples) of the circles found
                                circleCoordinates = []
                        
                                #Variables for drawing the dots on top of the staff line and the found circles
                                drawnCircleSize = 5
                                fill = True

                                #Draws the dots on the center of the found circles
                                for circle in circles:

                                        circleCoordinates.append(circles[i].coordinates())
##                                        img.dl().circle((circleCoordinates[i][0], circleCoordinates[i][1]), drawnCircleSize, Color.RED, filled = fill)
                                        i += 1
                                 

                                #Sorts the found circles in the circleCoordinates array by their x value, least to greatest
                                circleCoordinates.sort(key=lambda x: x[0])
                                
                                #Dividing staff line into 9 parts algorithm
                                partToDivideBy = (btmLftCd[1] - tpLftCd[1])/8

                                one = tpLftCd[1]
                                two = one + partToDivideBy
                                three = two + partToDivideBy
                                four = three + partToDivideBy
                                five = four + partToDivideBy
                                six = five + partToDivideBy
                                seven = six + partToDivideBy
                                eight = seven + partToDivideBy
                                nine = btmLftCd[1]

                                #Array this is populated with the nine values of the divided staff line positions
                                nineParts = [nine, eight, seven, six, five, four, three, two, one]


                                #Used for x coordinate of the drawn dots on the nine positions of the staff lines
                                if tpLftCd[0] < btmLftCd[0]:
                                        staffLineXAssignment = tpLftCd[0]
                                else:
                                        staffLineXAssignment = btmLftCd[0]




                                #Draws the nine dots on the nine positions of the staff lines for reference
##                                img.dl().circle((staffLineXAssignment, one), drawnCircleSize, Color.GREEN, filled = fill)
##                                img.dl().circle((staffLineXAssignment, two), drawnCircleSize, Color.GREEN, filled = fill)
##                                img.dl().circle((staffLineXAssignment, three), drawnCircleSize, Color.GREEN, filled = fill)
##                                img.dl().circle((staffLineXAssignment, four), drawnCircleSize, Color.GREEN, filled = fill)
##                                img.dl().circle((staffLineXAssignment, five), drawnCircleSize, Color.GREEN, filled = fill)
##                                img.dl().circle((staffLineXAssignment, six), drawnCircleSize, Color.GREEN, filled = fill)
##                                img.dl().circle((staffLineXAssignment, seven), drawnCircleSize, Color.GREEN, filled = fill)
##                                img.dl().circle((staffLineXAssignment, eight), drawnCircleSize, Color.GREEN, filled = fill)
##                                img.dl().circle((staffLineXAssignment, nine), drawnCircleSize, Color.GREEN, filled = fill)

                                #Show the image and the dots
                                #img.show()
                                
                                #Array that is populated with the nine notes on the staff line
                                letters = ["64", "65", "67", "69", '71', "72", "74", "76", "77"]
                            
                                #A value that will never be reached. Used for determining which note/nineParts position the circle is closest to
                                highValue = 1000000
                                
                                #Placeholder for the note of the circle
                                actualNote = letters[0]
                                
                                #Array that is populated with the note assignements for each circle. The elements in the array correspond to the circles on the page, left to right, or, in other words, the circles' x values least to greatest, which is already sorted up above in circleCoordinates
                                finalNoteValues = []


                                print("Number of Notes: " + str(len(circleCoordinates)))
                                #print("Notes Detected: " )
                                
                                #For the amount of circles there are:
                                for circle in range(0, len(circleCoordinates)):
                                        #For each position of the nine positions on the staff line:
                                        for position in range(0, len(nineParts)):
                                                #Check to see if the position value - the y coordinate of the circle is less than the highValue:
                                                if abs(nineParts[position] - circleCoordinates[circle][1]) < highValue:
                                                        #If so, then set highValue to that new value of the position value - the y coordinate of the circle
                                                        highValue = abs(nineParts[position] - circleCoordinates[circle][1])
                                                        #Set the note for that circle according to the position 
                                                        actualNote = letters[position]
                                        #Add the note for that circle to the finalNoteValues array that stores all of the note assignemnts in order of the circles' x value
                                        finalNoteValues.append(actualNote)
                                        #Reset highValue for the next circle
                                        highValue = 1000000

                                        #print("\t" + str(finalNoteValues[circle]))
                                        


                                        
                                        #Play the notes
                                        player.note_on(int(finalNoteValues[circle]),127) 
                                        sleep(velocity)
                                        player.note_off(76,127)
                                        sleep(velocity)

                                
                                        
                                
                                
                                        


                        #Else for if no circles are detected
                        else:
                            print("NO CIRCLES DETECTED")
                            img.show()
                        
                #Else for if more than one blob is detected when trying to detect only one blob (only one blob, as in one whole staff line)
                else:
                    print("MORE THAN 1 BLOB DETECTED - STAFF LINE DETECTION STEP")
                    img.show()
                        
            #Else for if no blobs are detected at all from the very beginning      
            else:
                print("NO STAFF LINE DETECTED")
                orignialImg.show()
                

            #Slow down the printed results to the console

            print("----------------------------------------------------------------------------")
            #sleep(1)
            exit
        else:
            print("Please enter a valid digit, such as '1' and hit enter.")

    print("Would you like to restart the application or exit the application? Enter the number that corresponds to your selection, and then hit enter.")
    print("\t1. Play the song again")
    print("\t2. Restart the application")
    print("\t3. Exit the application")

    playAgain = raw_input()

    while True:
        if playAgain.strip() == "1":
            for circle in range(0, len(circleCoordinates)):
                #Play the notes
                player.note_on(int(finalNoteValues[circle]),127) 
                sleep(velocity)
                player.note_off(76,127)
                sleep(velocity)
            print("Would you like to restart the application or exit the application? Enter the number that corresponds to your selection, and then hit enter.")
            print("\t1. Play the song again")
            print("\t2. Restart the application")
            print("\t3. Exit the application")
            playAgain = raw_input()
        elif playAgain.strip() == "2":
            break
        elif playAgain.strip() == "3":
            print("Goodbye :(")
            exit()
        else:
            print("Please enter a valid digit, such as '1' and hit enter.")
            playAgain = raw_input()
