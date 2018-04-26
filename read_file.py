# -*- coding: utf-8 -*-

import sax

class Input:
    
    def __init__(self, file_name):
        line_num=0
        self.values = []
        self.arr = []
        self.classes = []
        
        with open(file_name, encoding='utf-8') as file_in:
            for line in file_in:
                self.classes.append(line[0])
                line_num+=1
                line = line.replace('\n', '')
                self.values = line.split(',')
                del self.values[0]
                self.arr.append(self.values)
   
    def train (self, fragmentLength, alphabetSize):        
        bow1 = []
        bow2 = []
        bow3 = []
        bow4 = []

        self.saxVar = sax.Sax(fragmentLength, alphabetSize)
        for j in range(0, len(self.arr)):
            s = self.saxVar.discretize(self.arr[j])
            
            if self.classes[j] == '1':
                bow1.append(s)
            elif self.classes[j] == '2':
                bow2.append(s)
            elif self.classes[j] == '3':
                bow3.append(s)
            elif self.classes[j] == '4':
                bow4.append(s)
            
        return bow1, bow2, bow3, bow4 

    def bow_dist(self, bow, string):
        s = self.saxVar
        dist = []
        for i in range(0, len(bow)):
            dist.append(s.dist1(bow[i], string, len(self.arr)))
        return dist       
        
    def test (self, bow, refString):
        dist1 = self.bow_dist(bow[0], refString)
        dist2 = self.bow_dist(bow[1], refString)        
        dist3 = self.bow_dist(bow[2], refString)        
        dist4 = self.bow_dist(bow[3], refString)
        
        min1 = min(dist1)
        min2 = min(dist2)
        min3 = min(dist3)
        min4 = min(dist4)        
        
        minimum = min(dist1 + dist2 + dist3 + dist4)
        min_ind = 0

        if minimum == min1:
            min_ind = 1
        elif minimum == min2:
            min_ind = 2
        elif minimum == min3:
            min_ind = 3
        else:
            min_ind = 4
        
        return min_ind
        
    def read_test (self, filename, bow):
        line_num=0
        testClasses = []
        valuesTest = []
        myClasses = []
        err = 0
        
        with open(filename, encoding='utf-8') as file_in:
            for line in file_in:
                testClasses.append(int(line[0]))
                line_num+=1
                line = line.replace('\n', '')
                valuesTest = line.split(',')
                del valuesTest[0]
                a = self.saxVar.discretize(valuesTest)
                myClasses.append(self.test(bow, a))
        for i in range(0, len(testClasses)):
            if testClasses[i] != myClasses[i]:
                err += 1
        print('err: ' + str(err) + '/' + str(len(testClasses)))
        print('correct: ' + str(len(testClasses) - err) + '/' + str(len(testClasses)))
        return err
        
        
    
    
    
    
    
    
    
        