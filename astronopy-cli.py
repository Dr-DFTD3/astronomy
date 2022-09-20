#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

## TODO:
## Add internal support for conversion from RAW to JPEG


## add dictionary of NGC objects
## 

## Add polar alignment help

## Add goto help. Need to decide simplest 
## move to goto target.  Currently works if
## very close. NOT WORKING if on different 
## side of meridian....

## do careful check on DEC. things
## probably meed to change since 
## phi in [ -90,90 ] ... 
## -90 -> 270
## 90 -> 0
## two zeros for east west...


## 
## ./astronopy.py --ra="5:35.4:12" --dec="-5:27:10"  m45-test.jpg 
## ./astronopy.py -m42 m45-test.jpg
##



import math
import sys
import argparse
import numpy as np
import textwrap
import os

from time import gmtime, strftime

# custom functions and classes
from common import *
from time_data import Timer
from catalogs import Messier,NGC,User

import cli
import psolver as ps


# status and error messages 
mesgs = sys.stderr 

# output for calculated data
info = sys.stdout

verb = 0

def main(argv):

	messier = Messier()
	ngc = NGC()
	user = User()
	timeData = Timer()


	## if the user wants to see the objects in the dictionary
	## print them and bail
	if "list" in str(argv):
		mesgs.write("Which sky-catalog would you like to view [ (m)essier/(n)gc/(u)ser ]?\n")
		resp = raw_input('> ')
		if "m" in resp.lower():
			messier.load_data()
			messier.show_dictionary()
			sys.exit()
		elif "n" in resp.lower():
			ngc.load_data()
			ngc.show_dictionary()
			sys.exit()
		elif "u" in resp.lower():
			user.load_data()
			user.show_dictionary()
			sys.exit()
		else:
			mesgs.write("ERROR: Unknown sky catalog \" %s \"\n" % resp)
			sys.exit()



	parameters = cli.get_arguments( argv )

	inputFile = parameters.imgFile

	# verbosity during the run
	verb = parameters.verb

	solveField = False
	gotoTarget = False
	lookup = False

	## first check if user wants to goto 
	## a specific DSO from one of the DBs
	if parameters.messObj is not "empty":
		# load data from text file 
		messier.load_data()
		# print "getting messier now"
		objStr = "M" + parameters.messObj
		messier.lookup(objStr)
		raHMS = messier.raHMS.split(":")
		decHMS = messier.decHMS.split(":")
		# print messier.raHMS,messier.decHMS
		gotoTarget = True
	elif parameters.ngcObj is not "empty":
		ngc=1
		objStr = "NGC" + parameters.ngcObj
		gotoTarget = True
	elif parameters.userObj is not "empty":
		mesgs.write("ERROR: Database error, the object \" %s \" is unknown\n")
		mesgs.write("       Would you like to add it to the user DB? (y/n)\n")
		resp = raw_input('> ')
		if resp.lower() == "y":
			user.add_to_db()
		else:
			sys.exit()

		resp = raw_input('Calculate moves to new target? (y/n)? ')
		if resp.lower() == "y":
			user.load_data()
		else:
			mesgs.write("OK, exiting now...\n")
			sys.exit()
		objStr = parameters.userObj
		gotoTarget = True
	elif parameters.targetRA is not "empty":
		if parameters.targetDEC == "empty":
			mesgs.write("ERROR: DEC not specified along with RA coordinates, try \"astronopy.py --help\" for more info.\n")
			sys.exit()
		else:
			gotoTarget = True
			raHMS = parameters.targetRA.split(":")
			decHMS = parameters.targetDEC.split(":")
	elif parameters.targetDEC is not "empty":
		if parameters.targetRA == "empty":
			mesgs.write("ERROR: RA not specified along with DEC coordinates, try \"astronopy.py --help\" for more info.\n")
			sys.exit()
		else:
			gotoTarget = True
			raHMS = parameters.targetRA.split(":")
			decHMS = parameters.targetDEC.split(":")
	elif parameters.lObj is True:
		lookup = parameters.lObj
	else:
		## if no targets specified
		## then just plate solve 
		## the image and bail
		solveField = True


	if gotoTarget is False and solveField is False and lookup is False:
		mesgs.write("ERROR: I don't understand what you want to do, exiting\n")
		sys.exit()

	if gotoTarget is True:
		solveField = True
		targetRA = RightAcsension(float(raHMS[0]),float(raHMS[1]))
		targetDEC = Declination(float(decHMS[0]),float(decHMS[1]))

	resp = ""


	## if image is already a JPEG, just resize it
	## if image is RAW, convert to JPEG, then resize
	if ".jpg" in inputFile:
		jpegIn = True
		resize_jpg_image(parameters,"img_resized.jpg")	
	else:
		jpegIn = False	
		convert_image(parameters.imgFile,"img_converted.jpg")
		parameters.imgFile = "img_converted.jpg"
		resize_jpg_image(parameters,"img_resized.jpg")	



	if solveField is True:
		if verb > 1:
			mesgs.write("*)  Analyzing stars in your image [ " + inputFile + " ]\n")

		imgRAStr,imgDECStr = ps.solve_field("img_resized.jpg",parameters)

		# parse the coordinates of where the 
		# scope is currently pointing
		if verb > 1:
			info.write("*)  Determining the field center...\n")
		ra = imgRAStr.split(":")
		dec = imgDECStr.split(":")

		imgRA = RightAcsension(float(ra[0]),float(ra[1]),float(ra[2]))
		imgDEC = Declination(float(dec[0]),float(dec[1]),float(dec[2]))
		
		info.write( "=========================================\n")
		heading = "++ Star Field Analysis:"
		print_data( heading,imgRA,imgDEC)

	## if the user only wanted to get the RA/DEC
	## for where the scope is pointing then bail
	if solveField is True and gotoTarget is False:
		info.write( "=========================================\n")
		sys.exit()
	elif gotoTarget is True:
		raDiff = []
		decDiff = []

		if verb > 1:
			mesgs.write( "*)  calculating optimal moves to zero-in target...\n" )

		raDiff,decDiff = ps.zero_target(imgRA,imgDEC,targetRA,targetDEC)
		heading = "++ Target:"
		print_data( heading,targetRA,targetDEC)
		get_moves(raDiff,decDiff)
		info.write( "=========================================\n")
		
	elif lookup is True:
		messier.show_object()



	


	# messier.show_type()

	# lha = timeData.compute_lha(targetRA.hms)
	# lha0 = timeData.compute_lha(imgRAStr)

	# lha_hms = deg2hms(lha,"RA")
	# lha0_hms = deg2hms(lha0,"RA")

	# print "LHA(img) : ",lha0, "°  ",lha0_hms
	# print "LHA(tar) : ",lha, "°  ",lha_hms



if __name__ == "__main__": main(sys.argv[1:])


