#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 17:23:57 2024

@author: mikhail
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
import statistics

filecsv = "../Workplace/ping_pong_state.ACRF.labelled.csv"
#filecsv = "../Workplace/ping_pong_state.old.labelled.csv"
CVseeds = [8379, 662595671, 608642885, 4114, 4]

tab = pd.read_csv(filecsv).to_numpy()

X = tab[:,1:]
y = tab[:,0]

CVs = []
for i in CVseeds:
    CVs.append(train_test_split(X, y, test_size=0.4, random_state=i))

scores = []
for i in CVs:
    clf = KNeighborsClassifier().fit(i[0], i[2])
    scores.append(clf.score(i[1], i[3]))

print("Nearest neighbor classification accuracy: mean", statistics.mean(scores), "std.dev.", statistics.stdev(scores))

scores = []
for i in CVs:
    clf = RandomForestClassifier().fit(i[0], i[2])
    scores.append(clf.score(i[1], i[3]))

print("RF accuracy: mean", statistics.mean(scores), "std.dev.", statistics.stdev(scores))

scores = []
for i in CVs:
    clf = MLPClassifier().fit(i[0], i[2])
    scores.append(clf.score(i[1], i[3]))

print("MLP accuracy: mean", statistics.mean(scores), "std.dev.", statistics.stdev(scores))

