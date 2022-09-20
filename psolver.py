# -*- coding: utf-8 -*-
import math
import sys
import numpy as np
import os

# custom lib
from common import (hms2deg,deg2hms)

def get_alt_az(ra,dec):
	az=1

def solve_field(imgFile):

	fast = False

	if fast is True:
		plate_solve_cmd = "solve-field --no-plots --overwrite " + imgFile + " 2> /dev/null"
	else:
		plate_solve_cmd = "solve-field --overwrite " + imgFile + " 2> /dev/null"

	screen = os.popen(plate_solve_cmd,"r")

	imgRA = ""
	imgDEC = ""

	objList = False
	while 1:
	    line = screen.readline()
	    if not line: break
	    if "Field center: (RA H:M:S, Dec D:M:S)" in line:
	    	data = [str(x) for x in line.split()]
	    	imgRA = data[7]
	    	imgDEC = data[8]

	    # if parameters.printObjList is True:
    	if "Your field contains:" in line: objList = True
    	if objList is True: print line

	# clean up the output foramtting of astrometery.nte
	imgRA = imgRA.replace("(", "")
	imgRA = imgRA.replace(",", "")

	imgDEC = imgDEC.replace(")", "")
	imgDEC = imgDEC.replace(".", "")	

	return imgRA,imgDEC
	
def zero_target(imgRA,imgDEC,targetRA,targetDEC):

	imgRAStr = str(imgRA.hour) + ":" + str(imgRA.minutes) + ":0"
	targetRAStr = str(targetRA.hour) + ":" + str(targetRA.minutes) + ":0"

	imgRAdm = float(hms2deg(imgRAStr,"RA"))
	targetRAdm = float(hms2deg(targetRAStr,"RA"))

	imgDECdm = imgDEC.deg + imgDEC.minutes/60.
	targetDECdm = targetDEC.deg + targetDEC.minutes/60.

	decDiff = targetDECdm - imgDECdm
	raDiff = targetRAdm - imgRAdm

	raHMS = deg2hms(raDiff,"RA")
	decHMS = deg2hms(decDiff,"DEC")

	return raHMS,decHMS
