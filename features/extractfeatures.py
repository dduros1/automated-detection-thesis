#!/usr/bin/python
import subprocess
import argparse
import os
import time

thesisdir = '/home/d/Documents/shiny-thesis'
pindir = thesisdir+'/pin'
looptool = pindir+'/source/tools/MyPinTool/obj-intel64/simpleloop.so'
categorytool = pindir+'/source/tools/MyPinTool/obj-intel64/categorycount.so'
instructiontool = pindir+'/source/tools/MyPinTool/obj-intel64/arithinscount.so'
pin = pindir+'/pin.sh'
fileDirectory = thesisdir+'/features/featurefiles/'
debug = False
catTime = 0
insTime = 0
loopTime = 0
totalFiles = 0
catErr = 0
insErr = 0
loopErr = 0

def processDirectory(dirName):
	for root, dirs, files in os.walk(dirName):
		for currFile in files:
			print currFile
			processFile(currFile, dirName+currFile)
	return

def processFile(fileName, filePath):
    global totalFiles, loopTime, catTime, insTime

    totalFiles += 1
    if fileName == None:
        fileName = filePath.split('/')[-1]

    print 'processing', fileName, '...'
    startTime = time.time()
    loopfeatures = countLoops(filePath)
    endTime = time.time()
    loopTime += endTime - startTime

    startTime = time.time()
    instrfeatures = countInstructions(filePath)
    endTime = time.time()
    insTime += endTime - startTime
    
    startTime = time.time()
    categoryfeatures = countCategories(filePath)
    endTime = time.time()
    catTime += endTime - startTime

#print instrfeatures

    if test:
        outputdir = fileDirectory+'test/'
    else:
        outputdir = fileDirectory+'train/'

    ifile = open(outputdir+'ins/'+fileName+'_ins.feature', 'w+')
    cfile = open(outputdir+'cat/'+fileName+'_cat.feature', 'w+')
	
    for feat in instrfeatures:
        ifile.write(str(feat).rstrip()+'\n')
    for feat in categoryfeatures:
        cfile.write(str(feat).rstrip()+'\n')
    for feat in loopfeatures:
        ifile.write(str(feat).rstrip()+'\n')
        cfile.write(str(feat).rstrip()+'\n')


def countCategories(currFile):
    global catErr

    categories = [0]*61

    command = [pin, '-t', categorytool, '--', currFile]
    try:
        subprocess.call(command)
    except Exception:
        print 'Error in processing categories for', currFile
        catErr += 1
        return categories

	#writes to categorycount.out file, need to open and process file
    with open('categorycount.out', 'r') as f:
        for line in f:
            eles = line.split('\t')
            if int(eles[0]) <= 60:
                categories[int(eles[0])] = eles[2]

    print 'category features extracted'
    return categories

#TODO i think that everything is index one, soooo index 0 shouldn't be included
#TODO change if statements to exception handling
def countInstructions(currFile):
    global insErr
    instructions = [0]*1134

    command = [pin, '-t', instructiontool, '--', currFile]
    try:
        subprocess.call(command)
    except Exception:
        insErr +=1
        print 'Error in processing instructions for', currFile
        return instructions

	#writes to instrtypecount.out
    with open('instrtypecount.out', 'r') as f:
        for line in f:
            eles = line.split('\t')
#print int(eles[0]), eles[2]
            if int(eles[0]) <= 1133:
                instructions[int(eles[0])] = eles[2]
    print 'Instruction features extracted'	
    return instructions

def countLoops(currFile):
    global loopErr

    command = [pin, '-t', looptool, '--', currFile]
    try:
        output = subprocess.check_output(command)
    except Exception:
        loopErr +=1
        print 'Error in processing loops for', currFile
        return [0]*8

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
	
    print 'Loop features extracted'
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
    global fileDirectory
    global test

	#setup arguments
    parser = argparse.ArgumentParser(description='Feature Extraction using Pin')
    parser.add_argument('-o', type=str, help='Output directory for feature files')
    parser.add_argument('-d', type=str, help='A directory containing files to process')
    parser.add_argument('-f', type=str, help='A file to process')
    parser.add_argument('-test', action='store_true', default=False, help='Indicates that we are generating features for the test set')
    parser.add_argument('-debug', action='store_true', default=False)
    args = parser.parse_args()

#    if (args.debug):
#       debug = True

#   if args.test:
#       test = True

    debug = args.debug
    test = args.test
    if (args.o != None):
        fileDirectory=args.o

    if (args.d == None and args.f == None):
        print 'Please specify file or directory of files to process'
    elif (args.d != None):
        processDirectory(args.d)
    elif (args.f != None):
        processFile(None, args.f)
	

main()

print 'Feature extraction is complete--------------------------'
print 'Average time to process instructions', insTime/totalFiles
print 'Average time to process categories', catTime/totalFiles
print 'Average time to process loops', loopTime/totalFiles
print '------------------------------------'
print 'Failures to process instructions %d/%d' % (insErr, totalFiles)
print 'Failures to process categories %d/%d' % (catErr, totalFiles)
print 'Failures to process loops %d/%d' % (loopErr, totalFiles)


