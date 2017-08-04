#Artifical Intelligence Decision Tree Project - May 15, 2016
#Myles Johnson-Gray
#Kati McLaughlin
#Nikolai Snow

#Code that generates a decision tree from input data and tests data against tree

#imports
import math
from math import log
import random
import csv

#Class to parse CSV file
class ParseCSV:
    def __init__(self, filename):
        """
        This function reads a csv file or data + names file of the same name into a list of
        lists in which each list is a state. It is designed for csv values with column headers.
        """
        filenameparts = filename.split(".")
        type = filenameparts[-1]
        data = list()
        with open(filename, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                rowList = ', '.join(row)
                newList = list()
                var = ''
                for elem in rowList:
                    if elem != ',':
                        var = var + elem
                    else:
                        newList.append(var)
                        var = ''
                newList.append(var)
                data.append(newList)
            if type == "data":
                nfilename = filenameparts[0]
                nfilename += ".names"
                #with open(nfilename, newline='') as f:
                #    head = list(f)
                #    header = head[1].rstrip()
            else:
                header = data[0] # saves column headers in a new list
                data.remove(data[0]) # removes column headers
            stringList = list() # list of column names that were encrypted
            keyList = list() # list of lists of dictionaries where list contains
                             # the strings that were encoded.
                             # The value that each string was encoded to is equal
                             # to its index in the list plus 1

            for dataList in data:
                # for each state in data

                for i in range(len(dataList)):
                    # iterate through each element of the given state
                    try:
                        # if it is a number, typecast string to number
                        dataList[i] = float(dataList[i])
                    except ValueError:
                        # encode string to number
                        """
                        OPTIONAL: can finish this piece of code so that any
                        csv file can be encrypted rather than just our cars csv
                        """

                        """
                        if not header[i] in stringList:
                            # if the category has not yet been encrypted
                            stringList.append(header[i]) # adds category to end of list
                            keyList.append(list()) # adds empty dict for category to end of list
                        for k in range(len(stringList)):
                            # stringList and keyList are the same length in the same order
                            value = 0
                            name = dataList[i]

                            if stringList[k] == header[i]:
                                # the category of the data we're looking at
                                # since stringList and keyList are always
                                # in the same order
                                for m in range(len(keyList[k])):
                                    if name in keyList[k]:
                                        # if string was already found earlier
                                        value = m + 1
                                        # give it the encrypted value that was assigned
                                    else:

                                        # assign a new value for this string
                                        keyList[k][m].append(dataList[i])
                                        value = m + 1
                                        # provide encoded string and value for previously empty dict

                                dataList[i] = value # replace string with encrypted value
                        """

                        # if you don't want to encrypt strings, just replace
                        # the following if statements with:

                        # dataList[i] = dataList[i]

                        #Uncomment for encryption...otherwise keep raw data
                        if dataList[i] == 'Bad':
                            dataList[i] = 1
                        elif dataList[i] == 'OK':
                            dataList[i] = 2
                        elif dataList[i] == 'Good':
                            dataList[i] = 3
                        elif dataList[i] == 'America':
                            dataList[i] = 1
                        elif dataList[i] == 'Asia':
                            dataList[i] = 2
                        elif dataList[i] == 'Europe':
                            dataList[i] = 3


            #self.header = header
            self.data = data
            self.stringList = stringList
            self.keyList = keyList
    """
    def encodeString(list1, index):
        if list1[index]
    """

#calculate the entropy
def entropy(input_data):
    log2=lambda x:log(x)/log(2)
    results = uniquecounts(input_data)

    ent = 0.0
    for r in results.keys():
      #calculate probability of outcome
      p=float(results[r])/len(input_data)
      #calculate entropy
      ent=ent-p*log2(p)
    return ent

print("-----------------------------------------------------------------------")

#----------------------------------------------------------------------------------------------------------------------
class decisionnode:
  def __init__(self,col=-1,value=None,results=None,tb=None,fb=None):
    self.col=col #column index
    self.value=value #the value that the column must match in order to have a true value
    self.results=results #dictionary of results for the branch
    self.tb=tb #true decision node (if result is true then go here)
    self.fb=fb #false decision node (if result is false then go here)

#----------------------------------------------------------------------------------------------------------------------
def buildtree(input_data): #rows is the set, either whole dataset or part of it in the recursive call,

  if len(input_data)==0: return decisionnode() #len(rows) is the number of units in a set

  current_score=entropy(input_data)

  column_count=len(input_data[0])-1   #count the # of attributes/columns - 1(target column)
  #print(column_count)

  # Set up some variables to track the best criteria
  best_gain=0.0
  best_criteria=None
  best_sets=None

  for col in range(0,column_count):
    # Generate the list of all possible different values in the considered column
    global column_values #Added for debugging
    column_values={}

    for row in input_data:
       column_values[row[col]]=1
       #print(column_values)

    # Now try dividing the rows up for each value in this column
    for value in column_values.keys(): #the 'values' here are the keys of the dictionary
        (set1,set2)=divideset(input_data,col,value) #define set1 and set2 as the 2 children set of a division

        # Information gain
        p=float(len(set1))/len(input_data) #p is the size of a child set relative to its parent
        ent1 = 0
        ent2 = 0
        if len(set1)!=0 : ent1 = entropy(set1)

        if len(set2)!=0 : ent2 = entropy(set2)

        gain=current_score-p*ent1-(1-p)*ent2 #cf. formula information gain
        if gain>best_gain and len(set1)>0 and len(set2)>0: #set must not be empty
            best_gain=gain
            best_criteria=(col,value)
            best_sets=(set1,set2)

  # Create the sub branches
  if best_gain>0:
    trueBranch=buildtree(best_sets[0])
    falseBranch=buildtree(best_sets[1])
    return decisionnode(col=best_criteria[0],value=best_criteria[1],
        tb=trueBranch,fb=falseBranch)
  else:
    return decisionnode(results=uniquecounts(input_data))

#----------------------------------------------------------------------------------------------------------------------
#Divides a set on a specific column. Can handle numeric or nominal values
def divideset(input_data,column,value):
   #Make a function that tells us if a row is in the first group (true) or the second group (false)
   split_function=None
   if isinstance(value,int) or isinstance(value,float): # check if the value is a number i.e int or float
      split_function=lambda row:row[column]>=value
   else:
      split_function=lambda row:row[column]==value #otherwise do an equality check

   #Divide the rows into two sets and return them
   set1=[row for row in input_data if split_function(row)] #set that satisfies the condition
   set2=[row for row in input_data if not split_function(row)] # set which doesn't satisfy condition
   return (set1,set2)

#----------------------------------------------------------------------------------------------------------------------
#Splits data into two sets. Value is the length of the first set of data
def splitset(input_data, value):
    from random import randrange
    i = 0
    set1=[]
    set2=[]

    for i in range(value):
        #remove a random item from input_data and append it to set1
        random_index = randrange(len(input_data))
        set1.append(input_data[random_index])
        input_data.remove(input_data[random_index])
    set2 = input_data #the remaining data not removed
    return (set1, set2)

#----------------------------------------------------------------------------------------------------------------------
#Return the count of all possible outcomes (the last column of each row is the result)
def uniquecounts(input_data):
   #Dictionary that holds the outcome(key) and its count(value)
   uniqueOutcomes = {}

   #iterate through input data
   for row in input_data:
      #Holds the outcome result (in the last column)
      outcomeAttribute=row[len(row)-1]

      #assign new outcomes a count of 0 and append them to the attributeList
      if outcomeAttribute not in uniqueOutcomes:
          uniqueOutcomes[outcomeAttribute]=0
      #attributes that have already been seen have their count incremented
      uniqueOutcomes[outcomeAttribute]+=1

   return(uniqueOutcomes)

#----------------------------------------------------------------------------------------------------------------------
#Print tree in a readable format    decisionode = (col:val)       classification = (outcome, count)
def printtree(tree,indent=''):
   # Is this a leaf node?
    if tree.results!=None:
        print(str(tree.results))
    else:
        print(str(tree.col)+':'+str(tree.value)+'? ')
        # Print the branches
        print(indent+'T->', end=" ")
        printtree(tree.tb,indent+'  ')
        print(indent+'F->', end=" ")
        printtree(tree.fb,indent+'  ')

#----------------------------------------------------------------------------------------------------------------------
#Get the width (number of nodes) and depth of the tree
def getwidth(tree):
  if tree.tb==None and tree.fb==None: return 1
  return getwidth(tree.tb)+getwidth(tree.fb)

def getdepth(tree):
  if tree.tb==None and tree.fb==None: return 0
  return max(getdepth(tree.tb),getdepth(tree.fb))+1

#----------------------------------------------------------------------------------------------------------------------

#returns the expected outcome of a observation using a tree
def classify(observation,tree):
  if tree.results!=None:
    for key in tree.results.keys():
        return key
  else:
    v=observation[tree.col]
    branch=None
    if isinstance(v,int) or isinstance(v,float):
      if v>=tree.value: branch=tree.tb
      else: branch=tree.fb
    else:
      if v==tree.value: branch=tree.tb
      else: branch=tree.fb
    return classify(observation,branch)

#----------------------------------------------------------------------------------------------------------------------
#evaluate a dataset by testing it on the decision tree
def testSet(input_data, tree):
    i=0
    correctClass = 0 #number of correct classifications
    totalTests = len(input_data) #total number of observations

    for i in range(len(input_data)):
        #print(str(classify(input_data[i][:len(input_data[0])-1], tree)) + " " + str(input_data[i][len(input_data[0])-1]))

        #if the expected outcome is the same as the observed outcome...
        if (str(classify(input_data[i][:len(input_data[0])-1], tree)) == str(input_data[i][len(input_data[0])-1])):
            correctClass+= 1 #increment
    accuracy = correctClass / totalTests #recall
    return correctClass, accuracy

#----------------------------------------------------------------------------------------------------------------------
#split data and test on 'value' partitions of data (using k-cross)
def kCross(input_data, value):
    i = 0
    totalAccuracy = 0
    for i in range(value):
        set1, set2 = splitset(input_data, int(len(input_data) / value))
        tree = buildtree(set2)
        correctClass, accuracy= testSet(set1, tree)
        totalAccuracy+=accuracy
    totalAccuracy = totalAccuracy / value
    return totalAccuracy



#create a parser for each of our input data and read in information
parser = ParseCSV('mpg_cars.csv')
#attributeNames = parser.header
carData = parser.data

parser2 = ParseCSV('wdbc-test.data')
medTestData = parser2.data

parser3 = ParseCSV('wdbc-train.data')
medTrainData = parser3.data

#----------------------------------------------------------------------------------------------------------------------

#CAR DATA
#split car data into two sets       set1 = random 10% (testing)   set2 = the other 90%(training)initialCarData = carData
set1,set2 = splitset(carData, int(len(carData) / 10))
tree=buildtree(set2) #build tree with training data
print("PRINTING CAR TREE")
print("----------------------------------------------------")
printtree(tree) #print tree format
print("----------------------------------------------------")
print("Width of tree: (# of nodes): "+ str(getwidth(tree)))
print("Depth of tree: "+ str(getdepth(tree)))
print("----------------------------------------------------")

#print testing results
print("(Number of correct classifications, Accuracy)")
print("Recall of test case base: " + str(testSet(set1, tree)))
print("Recall with 10 fold cross validation: " + str(kCross(initialCarData, 10)))
print("Recall of training case base: " + str(testSet(set2, tree)))
#print(carData)
#print(attributeNames)
print("----------------------------------------------------")
#----------------------------------------------------------------------------------------------------------------------

#MED DATA
tree2=buildtree(medTrainData) #train with training data
print("PRINTING MED DATA TREE")
print("----------------------------------------------------")
printtree(tree2)
print("----------------------------------------------------")
print("Width of tree: (# of nodes): "+ str(getwidth(tree2)))
print("Depth of tree: "+ str(getdepth(tree2)))
print("----------------------------------------------------")

print("(Number of correct classifications, Accuracy)")
print("Recall of test case base: " + str(testSet(medTestData, tree2)))
print("Recall of training case base: " + str(testSet(medTrainData, tree2)))
#print(medTrainData)
print("----------------------------------------------------")

#print(kCross(carData, 10))
