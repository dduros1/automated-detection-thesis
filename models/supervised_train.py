#!/usr/bin/python

import os
import pickle
from sklearn.externals import joblib
from sklearn import svm


'''
    This class defines a SupervisedModel
'''
class SupervisedModel:
    featurefiles = '/home/d/Documents/shiny-thesis/features/featurefiles/crypto/' 
    cryptoalgs = ['aes', '3des', 'rsa', 'rc4', 'sha1', 'md5']
    modeldir = '/home/d/Documents/shiny-thesis/models/savedModels/'

    '''
        Initialize the model with the desired classification algorithm
    '''
    def __init__(self, mlAlgorithm):
        self.categoryData = SupervisedDataSet(69,1)
        self.instructionData = SupervisedDataSet(1142,1)
        self.algorithm = mlAlgorithm

    '''
        Create instruction and category datasets
    '''
    def createDatasets(self):
        for root, dirs, files in os.walk(self.featurefiles):
            for fileName in files:
                l = self.label(fileName)
                feature = self.extractLines(self.featurefiles+fileName)
                if 'cat.feature' in fileName:
                    self.categoryData.addSample(feature, l)
                elif 'ins.feature' in fileName:
                    self.instructionData.addSample(feature, l)


    '''
        Generate labeled data from filename based on model type
        Default model type is algorithmmodel
    '''
    def label(self, fileName):
        num = -1
        for alg in self.cryptoalgs:
            if alg in fileName:
                num = self.cryptoalgs.index(alg)
    
        return num

    '''
        Extract feature values from lines of feature file
    '''
    def extractLines(self,fileName):
        return [line.rstrip() for line in open(fileName, 'r')]

    '''
        Train the model
    '''
    def trainModel(self, *args):
        if  args == None:
            filePrefix = 'algorithmModel'
        elif len(args) == 1:
            filePrefix = args
        elif len(args) == 2:
            self.loadSavedModels(args[0], args[1])


        self.createDatasets()
        if (self.algorithm == 'svm'):
            self.svmtrain(filePrefix)
        elif self.algorithm=='ann':
            self.anntrain(filePrefix)

    '''
        Load saved models
    '''
    def loadSavedModels(self, modelFile1, modelFile2):
        svm1 = SVMUnit(modelFile1)
        svm2 = SVMUnit(modelFile2)

    '''
        Train an svm on the data
    '''
    def svmtrain(self, filePrefix):
        catSVM = SVMUnit()
        insSVM = SVMUnit()

        cTrainer = SVMTrainer(catSVM, categoryData)
        iTrainer = SVMTrainer(insSVM, instructionData)

        #save model
        catSVM.saveModel(self.modeldir+filePrefix+'_cat.model')
        insSVM.loadModel(self.modeldir+filePrefix+'ins.model')


    '''
        Train an artificial neural net on the data
    '''
    def anntrain(self):
        pass

############################## End SupervisedModel Class ###############################
'''
    This model classifies algorithms individually
    this is the default in supervised model
'''
class AlgorithmModel(SupervisedModel):
    def label(self,fileName):
        return super(AlgorithmModel,self).label(fileName)


############################## End AlgorithmModel Class ###############################
'''
    This model classifies crypto vs non
'''
class CryptoModel(SupervisedModel):


    def label(self,fileName):
        num = super(CryptoModel, self).label(fileName)
        if num > -1:
            num = 1
        else:
            num = 0
        return num


############################## End CryptoModel Class ###############################
'''
    This model classifies encryption vs hashing
'''
class TypeModel(SupervisedModel):

    def label(self,fileName):
        num = super(TypeModel, self).label(fileName)
        if num > 3:
            num = 1
        elif num > -1 and num < 4:
            num = 0
        return num


############################## End TypeModel Class ###############################


import argparse

def main():
    parser = argparse.ArgumentParser(description='Create a supervised model')
    parser.add_argument('model',type=str, help='Options: svm (support vector machine) or ann (artificial neural net)',default='svm')
    parser.add_argument('-s', nargs=2, type=str, help='Provide saved model files')
    parser.add_argument('-o', type=str, help='Provide prefix for output model files')
    args = parser.parse_args()
    
    model = args.model
    if (model not in ['svm', 'ann']):
        model = 'svm'
    m = SupervisedModel(model)

    if (args.s != None and len(args.s) == 2):
        m.trainModel(args.s[1], args.s[2])
    else:
        m.trainModel(args.o)


main()
