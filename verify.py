# -*- coding: utf-8 -*-

import read_file as rf

i = rf.Input('Car_TRAIN')
        
fragmentLength=22
alphabetSize=20

bow = i.train(fragmentLength, alphabetSize)
i.read_test("Car_TEST", bow)
      