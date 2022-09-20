# -*- coding: utf-8 -*-
import sys
import argparse
import textwrap


def get_arguments(argv):

	cli = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\
           Utility to perform various astrometric analysis tasks given
           an image of the sky. Simple plate solving is achieved via
           the Astrometry.net engine. A goto option offers suggested moves
           for to achieve target coordinates relative to the input image. 
           Other options to come....
         -----------------------------------------------------------------
         '''),
    epilog=textwrap.dedent('''\
         examples:
         -----------------------------------------------------------------
            %(prog)s m45.jpg
            %(prog)s m45.CR2 --solve
            %(prog)s --zero --ra="5:35.4" --dec="-5:27" m45.jpg
         '''))

	cli.add_argument(
		"imgFile",
		help="input file containig astrophotographic data to analyze",
		type=str
		)
	cli.add_argument(
		"-l","--lookup",
		dest="lObj",
		help="Print detailed info on a specifc object in one of the DBs",
		action="store_true"
		)
	cli.add_argument(
		"-o","--objects",
		dest="printObjList",
		help="Run plate solver to analyze input image. If any objects are found, print them to the screen",
		action="store_true"
		)
	cli.add_argument(
		"-s","--solve",
		dest="solveOnly",
		help="Run the image through the plate solve routine to accurately determine RA/DEC of the scope",
		action="store_true"
		)
	# cli.add_argument(
	# 	"-g","--goto=", 
	# 	dest="goto",
	# 	default="empty",
	# 	help="Calculate the moves necessary to point the scope at a target given a image. Currently Messier and NGC objects are accepted. Pass \"list\" as an argument to see the dictionary of objects",
	# 	type=str
	# 	)
	cli.add_argument(
		"-d","--dec=", 
		dest="targetDEC",
		metavar="D:M",
		help="Calculate moves to get from current DEC to targetDEC in degrees and arc-minutes. Must be specified with -r/--ra=.",
		type=str,
		default="empty"
		)
	cli.add_argument(
		"-r","--ra=", 
		dest="targetRA",
		metavar="H:M",
		help="Calculate moves to get from current RA to targetRA in degrees and arc-minutes. Must be specified with -d/--dec=.",
		type=str,
		default="empty"
		)
	cli.add_argument(
		"-q","--quick",
		dest="quick",
		help="Run code in fast mode. This does not produce annotated images and skips some fits pre-processing steps. Agressive image resizing is also done. (default=regular)",
		action="store_true"
		)
	cli.add_argument(
		"-m","--messier=", 
		metavar="<M_ID>",
		dest="messObj",
		help="Assuming the scope is pointing at the RA/DEC of imgFile, calculate moves to goto a specific \"Messier\" DSO defined in the \"$DATA/messier_dso.dat\" file. Pass \"list\" as an argument to see the dictionary of objects",
		type=str,
		default="empty"
		)
	cli.add_argument(
		"-n","--ngc=",
		metavar="<NGC_ID>",
		dest="ngcObj",
		help="Assuming the scope is pointing at the RA/DEC of imgFile, calculate moves to goto a specific \"NGC\" DSO defined in the \"$DATA/ngc_dso.dat\" file. Pass \"list\" as an argument to see the dictionary of objects",
		type=str,
		default="empty"
		)
	cli.add_argument(
		"-u","--user=",
		metavar="\"OBJ_NAME\"",
		dest="userObj",
		help="Assuming the scope is pointing at the RA/DEC of imgFile, calculate moves to goto a specific \"User\" DSO defined in the \"$DATA/user_dso.conf\" file. Pass \"list\" as an argument to see the dictionary of objects",
		type=str,
		default="empty"
		)
	cli.add_argument(
		"--max-dim=", 
		dest="maxDim",
		help="Maximum dimension for resizing the JPG image. Original image left untouched. (default=%(default)s)",
		default=640,
		type=float
		)
	# cli.add_argument(
	# 	"-z","--zero", 
	# 	dest="zeroIn",
	# 	help="Zero in to a specific RA/DEC coordinate pair. Must be near the target location, use -g other wise. MUST specify -r/-d coordinates!",
	# 	action="store_true"
	# 	)


	cli.add_argument("-v", dest="verb",help="increase output verbosity",default=0,action="count")
	cli.add_argument("--debug", dest="verb",help="extensive info, equivalent to \"-vvvv\"",action="store_true")
	cli.add_argument('--version', action='version', version='%(prog)s 3.0.')
	args = cli.parse_args()

	return args