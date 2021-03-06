#!/usr/bin/python3

import os
from sklearn.externals import joblib
from sklearn import svm
import numpy as np

'''
    This class defines a SupervisedModel
'''
class SupervisedModel:
#featurefiles = '/home/d/Documents/shiny-thesis/features/featurefiles/crypto/' 
    cryptoalgs = ['aes', '3des', 'rsa', 'rc4', 'sha1', 'md5']
    modeldir = '/home/d/Documents/shiny-thesis/models/savedModels/'
    myModel = None

    '''
        Initialize the model with the desired classification algorithm
    '''
    def __init__(self, mlAlgorithm, mode):
        self.trainData = []
        self.trainTarget = []
        self.testData = []
        self.testTarget = []
        self.algorithm = mlAlgorithm
        self.mode = mode                #True: ins
                                        #False: cat

    def setTrainData(self, train):
        self.createDataset(train, False)

    def setTestData(self, test):
        self.createDataset(test, True)

    '''
        Create instruction and category datasets
    '''
    def createDataset(self, dataDir, test):
        for root, dirs, files in os.walk(dataDir):
            for fileName in files:

                if 'cat.feature' in fileName and not self.mode:
                    l = self.label(fileName)
                    if l != None:
                        feature = self.extractLines(dataDir+fileName)
                        if test:
                            self.testData.append(feature)
                            self.testTarget.append(l)
                        else:
                            self.trainData.append(feature)
                            self.trainTarget.append(l)
                elif 'ins.feature' in fileName and self.mode:
                    l = self.label(fileName)
                    if l != None:
                        feature = self.extractLines(dataDir+fileName)
                        if test:
                            self.testData.append(feature)
                            self.testTarget.append(l)
                        else:
                            self.trainData.append(feature)
                            self.trainTarget.append(l)

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
        return [float(line.rstrip()) for line in open(fileName, 'r')]

    '''
        Train the model
    '''
    def trainModel(self):
        if (self.algorithm == 'svm'):
            self.svmtrain()
        elif self.algorithm == 'nb':
            self.naiveBayes()
        elif self.algorithm =='kmeans':
            self.kmeans()
        elif self.algorithm == 'dt':
            self.decisionTree()


    def crossValidate(self, k):
        from sklearn import cross_validation

        #TODO play with params
        svc = svm.SVC(C=1, kernel='linear')
        kfold = cross_validation.KFold(len(self.trainTarget), n_folds=k)

        cv = cross_validation.cross_val_score(svc, self.trainData, self.trainTarget, cv=kfold, n_jobs=-1)
        print(cv)


    '''
        Performs testing of model
            classification: True if it's a classification model
                            False if it's clustering
    '''
    def testModel(self, classification):
        predicted = []
        for instance in self.testData:
            predicted.append(self.myModel.predict(instance)[0])
        if classification:
            self.evaluateClassificationModel(predicted)
        else:
            self.evaluateClusteringModel(predicted)

    '''
        This method prints out a number of classification metrics
    '''
    def evaluateClassificationModel(self, predTarget):
        from sklearn.metrics import classification_report, accuracy_score
        print('Classification Report')
        target_names = self.getTargetNames()
        
        print (classification_report(self.testTarget, predTarget, target_names=target_names))
        print ('Accuracy_score')
        print (accuracy_score(self.testTarget, predTarget))
    

    '''
        This method prints out a number of clustering metrics
    '''
    def evaluateClusteringModel(self, predTarget):
        from sklearn.metrics import homogeneity_completeness_v_measure
        print('Clustering report--homogeneity, completeness, v-measure')
        print(homogeneity_completeness_v_measure(self.testTarget, predTarget))

    '''
        Load saved models
    '''
    def loadSavedModel(self, modelFile1):
        self.myModel = joblib.load(modelFile)

    '''
        Train an svm on the data
    '''
    def svmtrain(self):
        self.myModel = svm.SVC()
        self.myModel.fit(self.trainData, self.trainTarget)

    '''
        Save model
    '''
    def saveModel(self, filePrefix):
        if filePrefix == None:
            filePrefix == self.getModelName()
        if self.mode:
            filePrefix += '_ins'
        else:
            filePrefix += '_cat'

        joblib.dump(self.myModel, self.modeldir+filePrefix+'.model')   


    '''
        Naive Bayes classifier
    '''
    def naiveBayes(self):
        from sklearn import naive_bayes
        self.myModel = naive_bayes.GaussianNB()
        self.myModel.fit(np.array(self.trainData, dtype=float), np.array(self.trainTarget,dtype=float))

    '''
        Kmeans clustering
    '''
    def kmeans(self):
        from sklearn import cluster
        self.myModel = cluster.KMeans()
        self.myModel.fit(self.trainData)

    '''
        Gaussian mixture model classification
    '''
    def decisionTree(self):
        from sklearn import tree
        self.myModel = tree.DecisionTreeClassifier()
        self.myModel.fit(self.trainData, self.trainTarget)
        

    def getModelName(self):
        return 'SupervisedModel'

############################## End SupervisedModel Class ###############################
'''
    This model classifies algorithms individually
    this is the default in supervised model
'''
class AlgorithmModel(SupervisedModel):
    def label(self,fileName):
        num = super(AlgorithmModel, self).label(fileName)
        if num >= 0:
            return num
        else:
            return None         #don't train on non crypto
    def getModelName(self):
        return 'AlgorithmModel'

    def getTargetNames(self):
        return self.cryptoalgs

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

    def getModelName(self):
        return 'CryptoModel'

    def getTargetNames(self):
        return ['Not crypto', 'Crypto']


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
        else:
            num = None      #don't use non crypto
        return num

    def getModelName(self):
        return 'TypeModel'

    def getTargetNames(self):
        return ['Crypto', 'Hash']

############################## End TypeModel Class ###############################


import argparse
import sys


def runExperiment(m, k):
    global args

    opt = True
    if args.model == 'kmeans':
        opt = False

    #do cross validation to see how we're doing
    if (args.train != None):
        print ('Cross validation on training set (kfold = %d)' % k)
        m.setTrainData(args.train)
        m.crossValidate(k)


    if (args.load != None):
        m.setTestData(args.test)
        m.loadModel(args.load)
    else:
        m.setTrainData(args.train)
        m.setTestData(args.test)
        m.trainModel()
        if args.save:
            m.saveModel(args.o)
        m.testModel(opt)

def main():
    global args

    parser = argparse.ArgumentParser(description='Create a supervised model')
    parser.add_argument('model',type=str, help='Options: svm (support vector machine), nb (naive bayes), kmeans (clustering), dt (decision tree)',default='svm')
    parser.add_argument('-test', type=str, help='Directory containing feature files for testing')
    parser.add_argument('-train', type=str, help='Directory containing feature files for training')
    parser.add_argument('-load', type=str, help='Provide saved model file to load')
    parser.add_argument('-o', type=str, help='Provide prefix for output model files')
    parser.add_argument('-save', action='store_true', default=False, help='Save trained models')
    parser.add_argument('-ins', action='store_true', default=False, help='Indicate instruction features, defaults tocategory')
    
    args = parser.parse_args()


    if args.load == None and args.test == None and args.train == None:
        print('Please provide saved model files to load or testing and training data to create a model')
        sys.exit()
    if args.load != None and args.test == None:
        print('Please provide both saved model file and testing data')
        sys.exit()

    #ML model we are using
    model = args.model
    if (model not in ['svm', 'nb', 'kmeans', 'dt']):
        model = 'svm'
    

    ####MODEL 1: algorithm vs algorithm
    #Feature mode--for evaluation purposes (assume category mode)
    print('\n---------------------------------------------')
    print('Algorithm Model')
    m = AlgorithmModel(model, args.ins)
    runExperiment(m, 3)

   
    print('\n---------------------------------------------')
    print('Crypto Model')
    m = CryptoModel(model, args.ins)
    runExperiment(m,3)

    print('\n---------------------------------------------')
    print('Type Model')
    m = TypeModel(model, args.ins)
    runExperiment(m,3)

main()
