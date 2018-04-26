# -*- coding: utf-8 -*-


import numpy

class Sax:
    
    def __init__(self, w, a):
        self.alphabetSize = a
        self.wSize = w*1.0
        self.breakpoints = {'3' : [-0.43, 0.43],
                           '4' : [-0.67, 0, 0.67],
                           '5' : [-0.84, -0.25, 0.25, 0.84],
                           '6' : [-0.97, -0.43, 0, 0.43, 0.97],
                           '7' : [-1.07, -0.57, -0.18, 0.18, 0.57, 1.07],
                           '8' : [-1.15, -0.67, -0.32, 0, 0.32, 0.67, 1.15],
                           '9' : [-1.22, -0.76, -0.43, -0.14, 0.14, 0.43, 0.76, 1.22],
                           '10': [-1.28, -0.84, -0.52, -0.25, 0, 0.25, 0.52, 0.84, 1.28],
                           '11': [-1.34, -0.91, -0.6, -0.35, -0.11, 0.11, 0.35, 0.6, 0.91, 1.34],
                           '12': [-1.38, -0.97, -0.67, -0.43, -0.21, 0, 0.21, 0.43, 0.67, 0.97, 1.38],
                           '13': [-1.43, -1.02, -0.74, -0.5, -0.29, -0.1, 0.1, 0.29, 0.5, 0.74, 1.02, 1.43],
                           '14': [-1.47, -1.07, -0.79, -0.57, -0.37, -0.18, 0, 0.18, 0.37, 0.57, 0.79, 1.07, 1.47],
                           '15': [-1.5, -1.11, -0.84, -0.62, -0.43, -0.25, -0.08, 0.08, 0.25, 0.43, 0.62, 0.84, 1.11, 1.5],
                           '16': [-1.53, -1.15, -0.89, -0.67, -0.49, -0.32, -0.16, 0, 0.16, 0.32, 0.49, 0.67, 0.89, 1.15, 1.53],
                           '17': [-1.56, -1.19, -0.93, -0.72, -0.54, -0.38, -0.22, -0.07, 0.07, 0.22, 0.38, 0.54, 0.72, 0.93, 1.19, 1.56],
                           '18': [-1.59, -1.22, -0.97, -0.76, -0.59, -0.43, -0.28, -0.14, 0, 0.14, 0.28, 0.43, 0.59, 0.76, 0.97, 1.22, 1.59],
                           '19': [-1.62, -1.25, -1, -0.8, -0.63, -0.48, -0.34, -0.2, -0.07, 0.07, 0.2, 0.34, 0.48, 0.63, 0.8, 1, 1.25, 1.62],
                           '20': [-1.64, -1.28, -1.04, -0.84, -0.67, -0.52, -0.39, -0.25, -0.13, 0, 0.13, 0.25, 0.39, 0.52, 0.67, 0.84, 1.04, 1.28, 1.64]
                           }

        self.beta = self.breakpoints[str(self.alphabetSize)]
        self.dist_create()
    
    def normalize(self, time_serie):
        a = numpy.asarray(time_serie).astype(numpy.float)
        if numpy.nanstd(a) == 0:
            a = (a - numpy.nanmean(a))
        else:
            a = (a - numpy.nanmean(a)) / numpy.nanstd(a)
        return a
        

    def paa(self, time_serie):
        n = numpy.alen(time_serie)
        w = int(self.wSize)
        step = n/w
        self.lentgh = n*1.0
        
        red = []
        
        for i in range(0, w):
            lower_bound = int(step * i)
            upper_bound = int(step * (i+1) -1)            
            
            if upper_bound >= n:
                upper_bound = n-1
            if lower_bound >= n:
                lower_bound = n-1
                
            frame = numpy.array(time_serie[lower_bound:upper_bound])
            red.append(numpy.mean(frame))

        return red

    def toAlphabet(self, reduced):        
        string = ''
        
        for i in range (0, len(reduced)):
            found = False
            for j in range (0, len(self.beta)):
                if reduced[i]<self.beta[j]:
                    string += chr(ord('a')+j)
                    found = True
                    break
            if found == False:
                string += chr(ord('a')+len(self.beta))
                
        return string
        
        
    def dist_create(self):
        cardinal = range(0, self.alphabetSize)
        alphabet = [chr(x + ord('a')) for x in cardinal]
        
        '''
        Dictionary key = sum of 2 letters, e.g. a+b, and the value
        will be the distance netween a and b
        '''
        self.dictionary = {}
        
        for i in range(0, self.alphabetSize):
            for j in range(0, self.alphabetSize):
                if numpy.abs(cardinal[i] - cardinal[j]) <= 1:
                    self.dictionary[alphabet[i] + alphabet[j]] = 0
                else:
                    maxim = max(cardinal[i], cardinal[j]) - 1
                    minim = min(cardinal[i], cardinal[j])
                    self.dictionary[alphabet[i] + alphabet[j]] = self.beta[maxim] - self.beta[minim]    

    def discretize(self, time_serie):
        norm = self.normalize(time_serie)
        red = self.paa(norm)
        alpha = self.toAlphabet(red)
        return alpha
    
            
    def dist1(self, a, b, length):
        '''
        for same length strings
        '''
        distance = 0.0
        for i in range(0, len(a)):
            distance += ((self.dictionary[a[i]+b[i]])**2)
        return (numpy.sqrt(length/self.wSize)) * (numpy.sqrt(distance))
    
    
    def slidWind (self, time_serie, windowSize):
        m = len(time_serie)
        s = []
        for i in range(0,m):
            if len(time_serie[i:i+windowSize]) == windowSize:
                s.append(self.discretize(time_serie[i:i+windowSize]))
        return s














