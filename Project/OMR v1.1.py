from SimpleCV import Camera, Image, Display, Color, Blob
import math, time, sys, winsound

#Initialize Camera
cam = Camera()

#Initialize Display
display = Display()

#Used to keep track of which iteration of captured photo it is on 
iteration = 0


while display.isNotDone():

	
	iteration += 1
	print("ITERATION: " + str(iteration))

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


		print("Staff Line Blobs: " + str(length))
		print("Top Left Corner of Staff Line: " + str(tpLftCd))
		print("Center of Staff Line: " + str(center))
		print("Bottom Left Corner of Staff Line: " + str(btmLftCd))
		

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
					img.dl().circle((circleCoordinates[i][0], circleCoordinates[i][1]), drawnCircleSize, Color.RED, filled = fill)
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
				img.dl().circle((staffLineXAssignment, one), drawnCircleSize, Color.GREEN, filled = fill)
				img.dl().circle((staffLineXAssignment, two), drawnCircleSize, Color.GREEN, filled = fill)
				img.dl().circle((staffLineXAssignment, three), drawnCircleSize, Color.GREEN, filled = fill)
				img.dl().circle((staffLineXAssignment, four), drawnCircleSize, Color.GREEN, filled = fill)
				img.dl().circle((staffLineXAssignment, five), drawnCircleSize, Color.GREEN, filled = fill)
				img.dl().circle((staffLineXAssignment, six), drawnCircleSize, Color.GREEN, filled = fill)
				img.dl().circle((staffLineXAssignment, seven), drawnCircleSize, Color.GREEN, filled = fill)
				img.dl().circle((staffLineXAssignment, eight), drawnCircleSize, Color.GREEN, filled = fill)
				img.dl().circle((staffLineXAssignment, nine), drawnCircleSize, Color.GREEN, filled = fill)

				
				#Array that is populated with the nine notes on the staff line
				letters = ["lE", 'C:/Users/bbahn/Desktop/OMR Wav Files/lowF.wav', "lG", "A", 'C:/Users/bbahn/Desktop/OMR Wav Files/middleB.wav', "C", 'C:/Users/bbahn/Desktop/OMR Wav Files/middleD.wav', 'C:/Users/bbahn/Desktop/OMR Wav Files/highE.wav', "hF"]
				
				#A value that will never be reached. Used for determining which note/nineParts position the circle is closest to
				highValue = 1000000
				
				#Placeholder for the note of the circle
				actualNote = letters[0]
				
				#Array that is populated with the note assignements for each circle. The elements in the array correspond to the circles on the page, left to right, or, in other words, the circles' x values least to greatest, which is already sorted up above in circleCoordinates
				finalNoteValues = []

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
					
					#Play the notes
					winsound.PlaySound(finalNoteValues[circle], winsound.SND_FILENAME)
					
				#Show the notes in order of the circles
				print(str(finalNoteValues))
					
				#Show the image and the dots
				img.show()

			#Else for if no circles are detected
			else:
				print("NO CIRCLES DETECTED")
			
		#Else for if more than one blob is detected when trying to detect only one blob (only one blob, as in one whole staff line)
		else:
			print("MORE THAN 1 BLOB DETECTED - STAFF LINE DETECTION STEP")
			
	#Else for if no blobs are detected at all from the very beginning      
	else:
		print("NO STAFF LINE DETECTED")
		

	#Slow down the printed results to the console
	print("----------------------------------------------------------------------------")
	time.sleep(1)
	exit





	

