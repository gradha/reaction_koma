#!/usr/bin/env python
"""Reaction guys, customizable."""

from contextlib import closing
from optparse import OptionParser

#import Image
import logging
import os
import os.path
import sys
import time


DEFAULT_WIDTH = 500
CONVERT_PATH = "/usr/local/bin/convert"


def check_input_file(parser, filename, help_text):
	"""f(OptionParser, string, string) -> None

	Checks if the filename is a valid file. If not, the process quits. Pass the
	index string of the koma panel to show the user error.
	"""
	if not filename or not os.path.isfile(filename):
		print "Specify a valid image for the %s koma panel" % help_text
		parser.print_help()
		sys.exit(1)


def process_arguments(argv):
	"""f([string, ...]) -> [string, string, string, string]

	Parses the commandline arguments. The function always returns a tuple with
	four paths to the images in sequence.
	"""
	parser = OptionParser()
	parser.add_option("-1", "--first", dest="first",
		action="store", help = "path of the first koma panel")
	parser.add_option("-2", "--second", dest="second",
		action="store", help = "path of the second koma panel")
	parser.add_option("-3", "--third", dest="third",
		action="store", help = "path of the third koma panel")
	parser.add_option("-4", "--fourth", dest="fourth",
		action="store", help = "path of the fourth koma panel")
	(options, args) = parser.parse_args()

	check_input_file(parser, options.first, "first")
	check_input_file(parser, options.second, "second")
	check_input_file(parser, options.third, "third")
	check_input_file(parser, options.fourth, "fourth")

	return [options.first, options.second, options.third, options.fourth]


def get_image_size(filename):
	"""f(string) -> (int, int)

	Returns the size of the image as integers. Quits if there are problems.
	"""
	im = Image.open(filename)
	return im.size


def run_command(args):
	"""f([string, ...]) -> int

	Returns the value of the command being run, including parameters.
	"""
	logging.info("Running %r", args)
	res = os.spawnvp(os.P_WAIT, args[0], args)
	if res:
		logging.warn("Return value %r when running %r", res, args)
	return res


def main():
	"""f() -> None

	Main entry point of the application.
	"""
	panels = process_arguments(sys.argv)
	#sizes = [get_image_size(x) for x in panels]
	# Prepare a target size which is taller than the expected width.
	S = "%dx%d" % (DEFAULT_WIDTH, 2 * DEFAULT_WIDTH)
	run_command([CONVERT_PATH, panels[0], "-resize", S,
		panels[1], "-resize", S,
		panels[2], "-resize", S,
		panels[3], "-resize", S,
		"-quality", "85", "-append", "final.jpg"])

	logging.info("Done.")


if "__main__" == __name__:
	#logging.basicConfig(level = logging.INFO)
	logging.basicConfig(level = logging.DEBUG)
	t1 = time.time()
	main()
	t2 = time.time()
	dif = t2 - t1
	if dif > 1:
		minutes = int(dif / 60)
		seconds = dif - minutes * 60
		logging.info("Time spent %d minutes, %02d seconds", minutes, seconds)

# vim:tabstop=4 shiftwidth=4
