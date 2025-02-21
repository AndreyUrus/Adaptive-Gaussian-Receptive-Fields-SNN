#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 10:40:40 2025

@author: mike
"""

import csv
import numpy as np

filein = "ping_pong_state.csv"
fileout = "ping_pong_state.labelled.csv"

RACKET_SIZE = 0.18

def state(x, y, vx, vy, yr):
    if x >= 0:
        return -1
    if vx >= 0:
        return -1
    ddx = x + 0.5
    dyint = y - ddx * vy / vx + 0.5
    dyint -= np.floor(dyint / 2) * 2
    d = yr + 0.5
    if d - RACKET_SIZE / 2 < dyint and dyint < d + RACKET_SIZE / 2:
        return 0
    d = 2 - d
    return 0 if d - RACKET_SIZE / 2 < dyint and dyint < d + RACKET_SIZE / 2 else 1

with open(filein, newline = '') as filin, open(fileout, 'w') as filout:
    csr = csv.reader(filin)
    for row in csr:
        xball = float(row[1])
        yball = float(row[2])
        vxball = float(row[3])
        vyball = float(row[4])
        yracket = float(row[5])
        sta = state(xball, yball, vxball, vyball, yracket)
        if sta >= 0:
            filout.write('{},{},{},{},{},{}\n'.format(xball, yball, vxball, vyball, yracket, 1 - sta))
            
