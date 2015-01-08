#!/usr/bin/python
import subprocess
import argparse
import os

looptool = '../pin/source/tools/MyPinTool/obj-intel64/simpleloop.so'

def processDirectory(dirName):
	for root, dirs, files in os.walk(dirName):
		for currFile in files:
			print currFile
			#processFile(currFile)
	return

def processFile(fileName):
	countLoops(fileName)
	countArithmeticInstructions(fileName)

	return


def countArithmeticInstructions(currFile):
	#currently just counting instructions. need to write the damn pintool
	return

def countLoops(currFile):
	import re
	#./pin.sh -t source/tools/MyPinTool/obj-intel64/simpleloop.so -- ../binaries/aestest_gcc_fno-pic_Og > looptest3.out
	command = ['./../pin/pin.sh', '-t', looptool, '--', currFile]
	output = subprocess.check_output(command)

	output = output.split('\n')
	output = output[2:len(output)-1]

	#only keep loops with more than one iteration
	keep = []
	for line in output:
		eles = line.split('\t')
		if int(eles[1]) > 2:
			keep.append(eles)	
	for item in keep:
		print item
	
	#TODO currently keeping instruction and number of loops. Need to figure out a way to represent that as a feature


	return

def main():
	#setup arguments
	parser = argparse.ArgumentParser(description='Feature Extraction using Pin')
	parser.add_argument('-d', type=str, help='A directory containing files to process')
	parser.add_argument('-f', type=str, help='A file to process')
	args = parser.parse_args()

	if (args.d == None and args.f == None):
		print 'Please specify file or directory of files to process'
	elif (args.d != None):
		processDirectory(args.d)
	elif (args.f != None):
		processFile(args.f)
	

main()
