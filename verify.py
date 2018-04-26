# -*- coding: utf-8 -*-

import read_file as rf

windowSize=100
fragmentLength=25
alphabetSize=20

i = rf.Input('Car_TRAIN')
bow = i.train(windowSize, fragmentLength, alphabetSize)
i.read_test("Car_TEST", bow)
