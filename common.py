# -*- coding: utf-8 -*-
import math
import sys
import os
import argparse
import numpy as np
import PIL 
from PIL import Image

class Parameters:
	def __init__(self):
		self.imageLoaded = False
		self.rawImage = False
		self.jpgImage = False
		self.targetSet = False
		# parameters.jpgImage
		self.solveFieldOnly = False
		self.fieldSolved = False
		self.gotoTarget = False
		self.inputImageName = ""

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class RightAcsension:
	def __init__(self,hours,minutes,seconds=0.0):
		self.hour = hours
		self.minutes = minutes
		self.seconds = seconds
		self._hms = str(hours) + ":" + str(minutes) + ":" + str(seconds)

	@property
	def hms(self):
		return self._hms
	


class Declination:
	def __init__(self,degrees,minutes,seconds=0.0):
		self.deg = degrees
		self.minutes = minutes	
		self.seconds = seconds
		self._hms = str(degrees) + ":" + str(minutes) + ":" + str(seconds)

	@property
	def hms(self):
		return self._hms
	

def format_hms(data,form="DEC"):
	HMS = ""
	try:
		if form == "RA":
			HMS = str(data.hour) + ":" + str(data.minutes) + ":" + str(data.seconds)
		else:
			HMS = str(data.deg) + ":" + str(data.minutes) + ":" + str(data.seconds)
		return HMS
	except AttributeError:
		print "ERROR: DATA not in proper data structure!, try again"
		return None

def deg2hms(data,axis="RA",rounding=False):
	dsign = ""
	rsign = ""
	if axis is "DEC":
		dec = data
		if dec<0.: dsign,dec = "-", math.fabs(dec)

		#get degrees minutes and seconds from decimal degrees
		remainder,deg = math.modf(dec)
		totalMin = remainder * 60.

		remainder,mn = math.modf( totalMin )

		sec = remainder * 60.
		remainder,sec = math.modf(sec)

		DEC = [dsign,str(deg),str(mn),str(sec)]
		return DEC

	if axis is "RA":
		ra = data
		if ra<0.: rsign,ra = "-",math.fabs(ra)
		remainder,hr = math.modf(ra/15.)
		totalMin = remainder * 60.
		remainder,mn = math.modf( totalMin )
		sec = remainder * 60.
		remainder,sec = math.modf( sec )

		RA = [rsign,str(hr),str(mn),str(sec)]
		return RA



def hms2deg(hmsData,axis="RA"):
	data = hmsData.split(":")
	rsign = 1
	dsign = 1
	if axis is "DEC":
		d = float(data[0])
		m = float(data[1])
		s = float(data[2])
		if str(d)[0] == '-':
			dsign,d = -1,math.fabs(d)
		deg = d + (m/60.) + (s/3600.)
		DEC = '{0}'.format(deg*dsign)
		return DEC
	

	if axis is "RA":
		hr = float(data[0])
		mn = float(data[1])
		sec = float(data[2])
		if str(hr)[0] == '-':
			rsign,hr = -1,math.fabs(hr)
		deg = (hr*15.) + (mn/4.) + (sec/240.)
		RA = '{0}'.format(deg*rsign)
		return RA
	

def convert_image(imgFile,ofile):
	mesgs = sys.stderr 
	# if parameters.verb > 2:
	# 	mesgs.write("**) Converting RAW to JPEG ...\n")

	sip_convert_cmd = "sips -s format jpeg --out " + ofile + " " + imgFile + " &> sip_mesgs"
	os.system(sip_convert_cmd)


def resize_jpg_image(imgFile,ofile):

	maxDim = 640
	# mesgs = sys.stderr 
	# if parameters.verb > 2:
	# 	mesgs.write("**) Resizing JPEG image...\n")
	# 	mesgs.write("    -> largest dim = %4.2f \n" % maxDim)

	try:
		img = Image.open(imgFile)
		wpercent = (maxDim / float(img.size[0]))
		hsize = int((float(img.size[1]) * float(wpercent)))
		img = img.resize((maxDim, hsize), PIL.Image.ANTIALIAS)
		img.save(ofile)
	except IOError:
		print "ERROR: cannot resize your image '%s'" % imgFile


def print_data( heading,ra,dec ):
	# output for calculated data
	info = sys.stdout
	raHMS = format_hms( ra,"RA" )
	decHMS = format_hms( dec,"DEC" )

	info.write( "%s\n" % heading )
	info.write( "   RA ......: %-14s | %4.1f °\n"  % (raHMS,float(hms2deg(raHMS,"RA"))) )
	info.write( "   DEC .....: %-14s | %4.1f °\n"  % (decHMS,float(hms2deg(decHMS,"DEC"))) )

def get_moves(raDiff,decDiff):
	info = sys.stdout

	decMove = decDiff[1] + " ° " + decDiff[2] + " ' " 
	raMove = raDiff[1] + " H " + raDiff[2] + " M "

	if raDiff[0] == '-':
		direction = "WEST"
	else:
		direction = "EAST"

	info.write("++ Move scope:\n" )
	raDir = direction
	info.write(bcolors.RED + bcolors.BOLD)
	info.write("   %-5s  %s \n" % (direction,raMove))
	info.write(bcolors.ENDC)

	if decDiff[0] == '-':
		direction = "SOUTH"
	else:
		direction = "NORTH"

	decDir = direction
	info.write("++ Move scope:\n" )
	info.write(bcolors.RED + bcolors.BOLD)
	info.write("   %-5s  %s \n" % (direction,decMove))
	info.write(bcolors.ENDC)

	return raDir,raMove,decDir,decMove


	