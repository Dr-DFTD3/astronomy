# -*- coding: utf-8 -*-

import math
import sys
import numpy as np
from time import gmtime, strftime

# custom lib
from common import (hms2deg,deg2hms)

## accumulation table
std_year_days = [31,28,31,30,31,30,31,31,30,31,30,31]
std_year_acum = [0,31,59,90,120,151,181,212,243,273,304,334]

leap_year_days = [31,29,31,30,31,30,31,31,30,31,30,31]
leap_year_acum = [0,31,60,91,121,152,182,213,244,274,305,335]

## 82° 35' 37.02'' W
TAMPA_LONG = str(82) + ":" + str(35) + ":" + str(37.02) + ":W"
# TAMPA_LONG = 

class Timer:
	def __init__(self):

		gmt = strftime("%H:%M:%S", gmtime())
		year = strftime("%m:%d:%Y", gmtime())

		self.year = year
		self.gmt = gmt

		self._gst_hrs = 0
		self._gst_hms = None
		self._utc = gmt

		self.compute_gst( year )


	@property
	def gst_hms(self):
		return self._gst_hms

	@property
	def gst_hrs(self):
		return self._gst_hrs

	@property
	def utc(self):
		return self._utc



	# this needs to be computed in units
	# of decimal degrees
	## ra in units of H:M:S
	def compute_lha(self,ra):

		longData = TAMPA_LONG.split(":")
		d = float(longData[0])
		m = float(longData[1])
		s = float(longData[2])
		longWest = d + m/60. + s/3600.

		raDeg = float(hms2deg(ra,"RA"))
		gstDeg = float(hms2deg(self._gst_hms,"RA"))

		# print "GST HMS: ", self._gst_hms, "GST HRS: ", self._gst_hrs, "GST DEG ",raDeg
		
		# lst = gstDeg - raDeg

		lha = gstDeg - raDeg - longWest

		# print "LST ", deg2hms(lst,"RA")

		if lha < 0.:
			lha += 360.
		if lha > 360.:
			lha -= 360.

		return lha 


	def compute_gst(self,ydata):
		yrdata = ydata.split(":")
		mo = float(yrdata[0])
		d = float(yrdata[1])
		yr = float(yrdata[2])

		da = d +std_year_acum[int(mo)-1]

		## linear fit to data at
		## http://www.astro.umd.edu/~jph/GST_eqn.pdf
		G = 5.5356 + 0.0005471 * yr

		# compute ut in units of hours
		utime = self._utc.split(":")
		ut = float(utime[0]) + float(utime[1])/60. + float(utime[2])/3600.
		# print ut, float(utime[0]),float(utime[1])/60.,float(utime[2])/3600.

		# GMST = 6.697374558 + 0.06570982441908 D0 + 1.00273790935 H + 0.000026 T2

		self._gst_hrs = G + 0.0657098244 * da + 1.00273791 * ut

		## ensure GST is bounded by 24 hours
		if 24.0 < self._gst_hrs:
			self._gst_hrs -= 24.0

		## get hours and fraction of hours
		remainder,hr = math.modf(self._gst_hrs)

		## get minutes from remainder of hours
		totalMin = remainder * 60.
		remainder,mn = math.modf(totalMin)

		## get seconds from remainder of min
		s = remainder * 60.
		remainder,s = math.modf(s)

		self._gst_hms = str(hr) + ":" + str(mn) + ":" + str(s)

		return self._gst_hms

