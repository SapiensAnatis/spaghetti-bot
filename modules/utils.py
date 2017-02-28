from sys import argv
from os.path import dirname, realpath, join
from datetime import time

def get_script_dir():
	return dirname(realpath(argv[0]))

def local_filepath(filename):
	return join(get_script_dir(), filename)

def time_since(start):
	return (time().seconds * 1000) - start
