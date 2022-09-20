# -*- coding: utf-8 -*-

import sys
import numpy as np

# custom lib
from common import (hms2deg,deg2hms)


sky_object_types = {
		'1' : "Open Cluster", 
		'2' : "Globular Cluster", 
		'3' : "Planetary Nebula", 
		'4' : "Starforming Nebula", 
		'5' : "Spiral Galaxy",
		'6' : "Elliptical Galaxy", 
		'7' : "Irregular Galaxy", 
		'8' : "Lenticular (S0) Galaxy", 
		'9' : "Supernova Remnant", 
		'A' : "Asterism - System of 4 stars",
		'B' : "Milky Way Patch",
		'C' : "Binary star"
		}

class User:
	def __init__(self):
		self.objects = []
		self._raHMS = []
		self._decHMS = []
		self._objType = []
		self._constellation = []

		self.index = 200
		self.loaded = False

	@property
	def raHMS(self):
		return self._raHMS[self.index]

	@property
	def decHMS(self):
		return self._decHMS[self.index]

	@property
	def object(self):
		return self.objects[self.index]

	@property
	def NGC(self):
		return self._ngc[self.index]

	@property
	def objType(self):
		return self._objType[self.index]

	@property
	def constellation(self):
		return self._constellation[self.index]

	@property
	def distance(self):
		return self._distance[self.index]

	def add_to_db(self):
		obji = raw_input('Object Name: > ')
		rai  = raw_input('Object RA  : > ')
		deci = raw_input('Object DEC : > ')
		messier.add_to_db(obji,rai,deci)
		resp = raw_input('Start search (y/n)? ')

class NGC:
	def __init__(self):
		self.objects = []
		self._raHMS = []
		self._decHMS = []
		self._objType = []
		self._constellation = []

		self.index = 5000
		self.loaded = False

	@property
	def raHMS(self):
		return self._raHMS[self.index]

	@property
	def decHMS(self):
		return self._decHMS[self.index]

	@property
	def object(self):
		return self.objects[self.index]

	@property
	def NGC(self):
		return self._ngc[self.index]

	@property
	def objType(self):
		return self._objType[self.index]

	@property
	def constellation(self):
		return self._constellation[self.index]

	@property
	def distance(self):
		return self._distance[self.index]

	def load_data(self):
		## if the data was already loaded
		## clear the new lists since a new
		## object was recently added
		if self.loaded is True:
			self.objects = []
			self._raHMS = []
			self._decHMS = []
			self._constellation = []
			self._objType = []
			self._distance = []
			self._ngc = []

		with open("data/ngc.dat") as f:
			for line in f:
				if "#" in line: continue
				else:
					try:
						data = line.split()
						o = data[0]
						ra = data[1]
						dec = data[2]
						t = data[3]
						c = data[4]
						ngc = data[5]
						d = data[6]
						self.objects.append( o )
						self._raHMS.append( ra )
						self._decHMS.append( dec )

						self._objType.append( t )
						self._constellation.append( c )
						self._distance.append( d )
						self._ngc.append( ngc )

					except IndexError:
						break
			    	
		self.loaded = True
		f.close()


class Messier:
	def __init__(self):

		self.objects = []
		self._raHMS = []
		self._decHMS = []
		self._ngc = []
		self._objType = []
		self._constellation = []
		self._distance = []
		self.index = 200

		self.loaded = False

	@property
	def raHMS(self):
		return self._raHMS[self.index]

	@property
	def decHMS(self):
		return self._decHMS[self.index]

	@property
	def object(self):
		return self.objects[self.index]

	@property
	def NGC(self):
		return self._ngc[self.index]

	@property
	def objType(self):
		return self._objType[self.index]

	@property
	def constellation(self):
		return self._constellation[self.index]

	@property
	def distance(self):
		return self._distance[self.index]


	def show_type(self):
		t = sky_object_types[self.objType]
		print "Type (%s) : %s " % (self.objType,t)

	
	def add_to_db(self,obj,ra,dec):
		with open("data/messier.dat", 'a') as f:
			f.write('%s %s %s\n' % (obj,ra,dec)) 
		f.close() 

	def load_data(self):
		## if the data was already loaded
		## clear the new lists since a new
		## object was recently added
		if self.loaded is True:
			self.objects = []
			self._raHMS = []
			self._decHMS = []
			self._constellation = []
			self._objType = []
			self._distance = []
			self._ngc = []

		with open("data/messier.dat") as f:
			for line in f:
				if "#" in line: continue
				else:
					try:
						data = line.split()
						o = data[0]
						ra = data[1]
						dec = data[2]
						t = data[3]
						c = data[4]
						ngc = data[5]
						d = data[6]
						self.objects.append( o )
						self._raHMS.append( ra )
						self._decHMS.append( dec )

						self._objType.append( t )
						self._constellation.append( c )
						self._distance.append( d )
						self._ngc.append( ngc )

					except IndexError:
						break
			    	
		self.loaded = True
		f.close()


	def object_info(self,qobj):
		i = self.index
		try:
			mobj = self.objects[i]
			ra   = self._raHMS[i]
			dec  = self._decHMS[i]
			ot   = sky_object_types[self._objType[i]]
			cons = self._constellation[i]
			print "%-5s   %-10s  %10s   %-14s   %4s" % ("ID","RA(HMS)","DEC(HMS)","Constellation","Object Type")
			print "%-5s  %-10s   %10s   %-14s  %-14s" % ("----","---------","---------","-------------","-------------")
			print "%-5s  %-10s  %10s    %-14s  %-4s" % (mobj,ra,dec,cons,ot)
		except IndexError:
			print "ERROR: Cannot look at coordinates, they have not been set"
			sys.exit()

	def show_object(self):
		i = self.index
		try:
			mobj = self.objects[i]
			ra   = self._raHMS[i]
			dec  = self._decHMS[i]
			ot   = sky_object_types[self._objType[i]]
			cons = self._constellation[i]
			print "%-5s   %-10s  %10s   %-14s   %4s" % ("ID","RA(HMS)","DEC(HMS)","Constellation","Object Type")
			print "%-5s  %-10s   %10s   %-14s  %-14s" % ("----","---------","---------","-------------","-------------")
			print "%-5s  %-10s  %10s    %-14s  %-4s" % (mobj,ra,dec,cons,ot)
		except IndexError:
			print "ERROR: Cannot look at coordinates, they have not been set"
			sys.exit()

	def show_dictionary(self):
		if self.loaded is True:
			print "            =============================="
			print "                Messier Object Catalog:   "
			print "            =============================="
			print "%-5s   %-10s  %10s   %-14s   %4s" % ("ID","RA(HMS)","DEC(HMS)","Constellation","Object Type")
			print "%-5s  %-10s   %10s   %-14s  %-14s" % ("----","---------","---------","-------------","-------------")
			for i in range(len(self.objects)):
				mobj = self.objects[i]
				ra   = self._raHMS[i]
				dec  = self._decHMS[i]
				ot   = sky_object_types[self._objType[i]]
				cons = self._constellation[i]
				print "%-5s  %-10s  %10s    %-14s  %-4s" % (mobj,ra,dec,cons,ot)
		else:
			print "ERROR: MESSIER_DATA_BASE not loaded"



	def lookup(self,qobj):

		index = -1
		# print "Q",qobj
		if self.loaded is True:
			for i in range(len(self.objects)):
				mobj = self.objects[i]
				
				if mobj == qobj:
					# print "M",mobj
					index = i
					self.index = i

			if index > 0:
				ra = self._raHMS[index]
				dec = self._decHMS[index]
				return index
		else:
			print "ERROR: MESSIER_DATA_BASE not loaded"
		
		return index



