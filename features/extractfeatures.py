#!/usr/bin/python
import subprocess
import argparse
import os

pindir = '/home/d/Documents/shiny-thesis/pin'
looptool = pindir+'/source/tools/MyPinTool/obj-intel64/simpleloop.so'
categorytool = pindir+'/source/tools/MyPinTool/obj-intel64/categorycount.so'
instructiontool = pindir+'/source/tools/MyPinTool/obj-intel64/arithinscount.so'
pin = pindir+'/pin.sh'
fileDirectory = './featurefiles/'
debug = False

def processDirectory(dirName):
	for root, dirs, files in os.walk(dirName):
		for currFile in files:
			print currFile
			processFile(currFile, dirName+currFile)
	return

def processFile(fileName, filePath):
	loopfeatures = countLoops(filePath)
	instrfeatures = countInstructions(filePath)
	categoryfeatures = countCategories(filePath)

	ifile = open(fileDirectory+fileName+'_ins.feature', 'w+')
	cfile = open(fileDirectory+fileName+'_cat.feature', 'w+')
	
	for feat in instrfeatures:
		ifile.write(str(feat)+'\n')
	for feat in categoryfeatures:
		cfile.write(str(feat)+'\n')
	#for feat in loopfeatures:
	#	ifile.write(str(feat))
	#	cfile.write(str(feat))


def countCategories(currFile):
	categories = [0]*61

	command = [pin, '-t', categorytool, '--', currFile]
	try:
		subprocess.call(command)
	except Exception:
		print 'Error in processing categories for', currFile
		return

	#writes to categorycount.out file, need to open and process file
	with open('categorycount.out', 'r') as f:
		for line in f:
			eles = line.split('\t')
			if int(eles[0]) <= 60:
				categories[int(eles[0])] = eles[2]

	return categories

#TODO i think that everything is index one, soooo index 0 shouldn't be included
#TODO change if statements to exception handling
def countInstructions(currFile):
	instructions = [0]*1134

	command = [pin, '-t', instructiontool, '--', currFile]
	try:
		subprocess.call(command)
	except Exception:
		print 'Error in processing instructions for', currFile
		return

	#writes to instrtypecount.out
	with open('instrtypecount.out', 'r') as f:
		for line in f:
			eles = line.split('\t')
			if int(eles[0]) <= 1133:
				instructions[int(eles[0])] = eles[1]
	return instructions

def countLoops(currFile):
	command = [pin, '-t', looptool, '--', currFile]
	try:
		output = subprocess.check_output(command)
	except Exception:
		print 'Error in processing loops for', currFile
		return

	output = output.split('\n')
	output = output[2:len(output)-1]

	#only keep loops with more than one iteration
	keep = []
	for line in output:
		eles = line.split('\t')
		if int(eles[1]) > 2:
			keep.append(eles)	
	

	if debug:
		f = open('loopfeatures.test', 'a+')
		for item in keep:
			f.write(str(item[1])+'\t' + str(item[2])+'\n')
		f.close()
	
	return parseLoopFeature(keep)

def parseLoopFeature(keep):
	features = [0]*8
	for ele in keep:
		count = ele[1]
		ins = ele[2]
		cmd = ins.split()[0]
		try:
			features[loopidx(cmd)] += int(count)
		except IndexError:
			continue		#not a feature we're keeping
	print features
	return features
			

def loopidx(x):
	return {
		'push':0,
		'jmp':1,
		'repne':2,
		'add':3,
		'lea':4,
		'not':5,
		'and':6,
		'jz':7,
	}.get(x, -1)	#-1, not a feature command

def main():
	global debug

	#setup arguments
	parser = argparse.ArgumentParser(description='Feature Extraction using Pin')
	parser.add_argument('-d', type=str, help='A directory containing files to process')
	parser.add_argument('-f', type=str, help='A file to process')
	parser.add_argument('-debug', action='store_true')
	args = parser.parse_args()

	if (args.debug):
		debug = True

	if (args.d == None and args.f == None):
		print 'Please specify file or directory of files to process'
	elif (args.d != None):
		processDirectory(args.d)
	elif (args.f != None):
		processFile(args.f)
	

main()
