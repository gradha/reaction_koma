#!/usr/bin/env python
"""Reaction guys, customizable."""

from contextlib import closing
from optparse import OptionParser

import ConfigParser
import logging
import os
import os.path
import sys
import time


DEFAULT_WIDTH = 500
DEFAULT_CONVERT_PATH = "/usr/bin/convert"
INI_FILE = os.path.expanduser("~/.reaction_koma.ini")
KEY_CONVERT_PATH = "convert_path"
KEY_WIDTH = "strip_width"
INI_TEMPLATE = """; Template for reaction_koma.py
["global"]
%s=/usr/bin/convert
%s=500

; Create image sets through bracketed names, use with "-set cinema"
; Specify the default images you want for each slot, params override them.
;[cinema]
;first=~/Pictures/friends/1.jpg
;second=~/Pictures/friends/1.jpg
;third=~/Pictures/friends/1.jpg
;fourth=~/Pictures/friends/1.jpg
""" % (KEY_CONVERT_PATH, KEY_WIDTH)


def check_input_file(parser, options, attr_name, config):
	"""f(OptionParser, string, string, {}) -> None

	Checks if the filename is a valid file. If not, the process quits. Pass the
	index string of the koma panel to show the user error.

	The config parameter will be used as the default dictionary to grab paths
	from in case the normal parameter doesn't work.
	"""
	# Try the param filename.
	filename = getattr(options, attr_name)
	if filename and os.path.isfile(filename):
		return

	# Try the configuration file.
	filename = ""
	try: filename = config[attr_name]
	except: pass

	if filename and os.path.isfile(filename):
		setattr(options, attr_name, filename)
		return

	logging.error("Specify a valid image for the %s koma panel", attr_name)
	parser.print_help()
	sys.exit(1)


def get_options_from_ini():
	"""f() -> {}

	Tries to read the INI_FILE and returns the sections as python dictionaries.
	If the INI_FILE doesn't exist, it will be populated with defaults for the
	user.
	"""
	ret = {}
	if not os.path.isfile(INI_FILE):
		logging.info("No %r file, creating from template", INI_FILE)
		with closing(open(INI_FILE, "wt")) as out: out.write(INI_TEMPLATE)
		return ret

	try:
		c = ConfigParser.SafeConfigParser()
		c.read(INI_FILE)
		# Retrieve configuration sets along with expanded paths.
		for section in c.sections():
			ret[section] = dict(
				[(x, os.path.expanduser(y)) for x, y in c.items(section)])
			# Convert width option to integer.
			if KEY_WIDTH in ret[section]:
				try:
					ret[section][KEY_WIDTH] = int(
						ret[section][KEY_WIDTH])
				except ValueError, e:
					logging.error("Couldn't parse int for [%s]%s", section, KEY_WIDTH)
					del ret[section][KEY_WIDTH]
	except ConfigParser.NoSectionError, e:
		pass
	return ret


def process_arguments(argv):
	"""f([string, ...]) -> [string, string, string, string]

	Parses the commandline arguments. The function returns an option pseudo
	structure with the parameters as attributes. The input panels are assempled
	into the panels attribute for convenience.
	"""
	config = get_options_from_ini()
	default_convert_path = DEFAULT_CONVERT_PATH
	default_strip_width = DEFAULT_WIDTH
	if "global" in config:
		default_convert_path = config["global"][KEY_CONVERT_PATH]
		default_strip_width = config["global"][KEY_WIDTH]

	parser = OptionParser()
	parser.add_option("-1", "--first", dest="first",
		action="store", help = "path of the first koma panel")
	parser.add_option("-2", "--second", dest="second",
		action="store", help = "path of the second koma panel")
	parser.add_option("-3", "--third", dest="third",
		action="store", help = "path of the third koma panel")
	parser.add_option("-4", "--fourth", dest="fourth",
		action="store", help = "path of the fourth koma panel")
	parser.add_option("-c", "--convert", dest="convert_path",
		action="store", help = "path to Imagemagik's convert binary",
		default=default_convert_path)
	parser.add_option("-t", "--top", dest="first",
		action="store", help = "alias for the first panel")
	parser.add_option("-b", "--bottom", dest="third",
		action="store", help = "alias for the third panel")
	parser.add_option("-w", "--strip-width", dest="strip_width",
		action="store", type="int", help="width for the vertical strip",
		default=default_strip_width)
	parser.add_option("-p", "--photoset", dest="photoset",
		action="store", help = "name of the default photoset from ini file")
	(options, args) = parser.parse_args()

	photoset = {}
	if options.photoset and options.photoset in config:
		photoset = config[options.photoset]

	check_input_file(parser, options, "first", photoset)
	check_input_file(parser, options, "second", photoset)
	check_input_file(parser, options, "third", photoset)
	check_input_file(parser, options, "fourth", photoset)

	options.panels = [options.first, options.second,
		options.third, options.fourth]
	return options


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
	options = process_arguments(sys.argv)
	#sizes = [get_image_size(x) for x in panels]
	# Prepare a target size which is taller than the expected width.
	S = "%dx%d" % (options.strip_width, 10 * options.strip_width)
	if run_command([options.convert_path, options.panels[0], "-resize", S,
			options.panels[1], "-resize", S,
			options.panels[2], "-resize", S,
			options.panels[3], "-resize", S,
			"-quality", "85", "-append", "final.jpg"]):
		logging.error("Unexpected return value from %r", options.convert_path)
	else:
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
