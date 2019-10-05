#K-Nearest Neighbor Implementation Project
#Alexander Alvarez
#Matt Wintersteen
#Kyle Webster
import math
import random

#generalized minkowski distance, where p is either input integer or string 'inf'
def minkowskiDistance(v1,v2,p):
    if type(p)==str:
        maxDistance = 0
        for x in range(len(v1)):
            maxDistance = max(maxDistance, abs(v1[x]-v2[x]))
        return maxDistance
    else:
        distance = 0
        # assume: v1 and v2 are equal length
        for x in range(len(v1)-1):
            distance += pow((abs(v1[x]-v2[x])),p)
        return pow(distance, 1.0/p)

#randomize data so that when we select training and test sets, we get a variety of each class
def randomizeData(data):
    randomSet = []
    copy = list(data)
    while len(randomSet) < len(data):
        index = random.randrange(len(copy))
        randomSet.append(copy.pop(index))
    return randomSet

#class for storing the data sets
class dataset:
    total_set = []

    # training set is a list of training set data
    # test set is a list of test set data
    # changing the k for k fold cross validation will change the size
    training_set = [[]]
    test_set = [[]]

    def __init__(self,data):
        self.total_set = data
        self.kFoldCross(10)
        
    def getTotalSet(self):
        return self.total_set
    
    def getTrainingSet(self):
        return self.training_set

    def getTestSet(self):
        return self.test_set

    def kFoldCross(self, k):
        training_set = []
        test_set = []
        splitRatio = .9
        for i in range(k):
            testSize = int(len(self.total_set) - len(self.total_set) * splitRatio)
            index = i*testSize

            trainSet = list(self.total_set)
            testSet = []

            for j in range(testSize):
                testSet.append(trainSet.pop(index))

            training_set.append(trainSet)
            test_set.append(testSet)
        self.training_set = training_set
        self.test_set = test_set

#class containing methods for preprocessing the datasets
class pre_processing:
    data = []
    def __init__(self, file_name):
        data = []
        #open input and output files
        with open(file_name) as readIn:
            #iterate over each line in input file
            for line in readIn:
                if(file_name[:16] == "data/winequality"):
                    features = line.split(";")
                else:
                    features = line.split(",")
                data.append(features)

        if(file_name == "data/forestfires.csv" or file_name == "data/winequality-red.csv" or file_name ==  "data/winequality-white.csv"):
            data = self.removeHeaders(data, 1)
        elif(file_name == "data/segmentation.data"):
            data = self.removeHeaders(data, 5)
        data = self.removeStrings(data)
        
        self.data = data
    def removeHeaders(self, data, rows):
        for i in range(rows):
            print("Deleting Header Row")
            print(data[0])
            del data[0]
        return data

    def removeStrings(self, data):
        stringlist = []
        for i in range(len(data)):
            for j in range(len(data[i])):
                d = data[i][j].strip()
                
                split = d.split(".")
                
                if((not d.isnumeric()) and (not split[0].isnumeric()) and (d[:1] != "-")):
                    if(d not in stringlist):
                        stringlist.append(d)
                        d = len(stringlist)
                    else:
                        d = stringlist.index(d)
                data[i][j] = float(d)
        if(len(stringlist) > 0):
            print("Removed Strings")
            for s in stringlist:
                print(s)
        return data
    
    def getData(self):
        return self.data

        

#class containing methods implementing the K-NN algorithms
class k_nearest_neighbor:
    def __init__(self):
        print("init knn")
    def knn(trainingSet, t, k):
        distances = []
        for x in range(len(trainingSet)):
            dist = minkowskiDistance(t, trainingSet[x], 1)
            distances.append((trainingSet[x], dist))
        # Sort by the second value in sub list
        distances.sort(key = lambda x: x[1])
        neighbors = []
        for x in range(k):
            neighbors.append(distances[x][0])
        return neighbors
    
    def getClass(neighbors):
        classVotes = {}
        for x in range(len(neighbors)):
            response = neighbors[x][0]
            if response in classVotes:
                classVotes[response] += 1
            else:
                classVotes[response] = 1
        sortedVotes = sorted(classVotes.items(),key = lambda x: x[1],reverse=True)
        return sortedVotes[0][0]
    
    def getAccuracy(testSet, predictions):
        correct = 0
        for x in range(len(testSet)):
            if testSet[x][0] is predictions[x]:
                correct += 1
        return (correct/float(len(testSet))) *100.0
    
    def k_nearest(data, k):
        dataset.k_split(k)

#class for driving the program
class main:
    files = ["data/abalone.data",
             "data/car.data",
             "data/forestfires.csv",
             "data/machine.data",
             "data/segmentation.data",
             "data/winequality-red.csv",
             "data/winequality-white.csv"]

    #temp testing
    classification = ["data/segmentation.data",
                      "data/car.data",
                      "data/abalone.data"
                      ]

    for f in classification:
        print("////////\n{}\n//////////\n".format(f))
        p = pre_processing(f)
        randomizedData = randomizeData(p.getData())
        data = dataset(randomizedData)
        training_set = data.getTrainingSet()
        test_set = data.getTrainingSet()

        for i in range(len(training_set)):
            trainSet = training_set[i]
            testSet = test_set[i]
            
            k = 3
            predictions = []
            k_nearest_neighbor()
            for x in range(len(testSet)):
                neighbors = k_nearest_neighbor.knn(trainSet, testSet[x], k)
                result = k_nearest_neighbor.getClass(neighbors)
                predictions.append(result)
                #print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][0]))
            accuracy = k_nearest_neighbor.getAccuracy(testSet,predictions)
            print('Accuracy: ' + repr(accuracy) + '%')

    trainSet = [[2, 2, 2, 'a'], [4, 4, 4, 'b'],[2, 3, 2, 'a'], [4, 4, 5, 'b']]
    testSet = [[5, 5, 5, 'b'],[2, 2, 1, 'a']]

driver = main()
#main.run()
