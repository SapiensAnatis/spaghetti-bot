from sys import argv
from os.path import dirname, realpath, join

def get_script_dir():
	return dirname(realpath(argv[0]))

def local_filepath(filename):
	return join(get_script_dir(), filename)
