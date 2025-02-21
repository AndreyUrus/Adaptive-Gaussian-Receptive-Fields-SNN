# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 20:16:17 2025

@author: Kiselev Mikhail

Вычисление отношения сохраненой информации о первоначальной выборке величины из треугольного распреднления 
для адпативного метода гауссовых рецептивных полей и его стандартного варианта.

"""

import numpy as np
import random
import matplotlib.pyplot as plt

nPresentationTacts = 10
nTestPoints = 100000   # Число значений в выборке

# Вычисление N центров рецептивных полей для выброки lxsample - адаптивный вариант (2)

def AdaptiveReceptiveFieldCenters(N):
    ret = np.zeros(N)
    d = len(lxsample) / N
    for i in range(N):
        ret[i] = (lxsample[int(i * d)] + (lxsample[int((i + 1) * d)] if i < N - 1 else lxsample[-1])) / 2
    return ret

# Вычисление расстояний от значения x до центров рецептивных полей - адаптивный вариант (4)

def AdaptiveDistances(x, c):
    i = 0
    ret = np.zeros(len(c))
    
    # Определим центры рецептивных полей, ближайшие к x - (il, i)
    
    while i < len(c) and c[i] < x:
        i += 1
    il = i - 1
    
    # итеративное вычисление расстояний до ближайших и остальных центров
    
    if il >= 0:
        d = (x - c[il]) / (c[i] - c[il]) if i < len(c) else 0.
        k = il
        while k >= 0:
            ret[k] = d
            d += 1
            k -= 1
    if i < len(c):
        d = (c[i] - x) / (c[i] - c[il]) if i > 0 else 0.
        while i < len(c):
            ret[i] = d
            d += 1
            i += 1
            
    return ret

# Вычисление N центров рецептивных полей в диапазоне [0, 1024] - стандартный вариант 

def ReceptiveFieldCenters(N):   
    return [(2 * i + 1) * 1024 / (2 * N)  for i in range(N)]

# Вычисление расстояний от значения x до центров рецептивных полей - стандартный вариант

def Distances(x, c):
    return [abs(x - a) for a in c]

# Сколько общиих значащих бит у целых чисел a и b

def nCorrectBits(a, b, maxnbits):
    fl = 1 << (maxnbits - 1)
    ret = 0
    bStart = False
    while fl != 0 and (a & fl) == (b & fl):
        if (a & fl) != 0:
            bStart = True
        if bStart:
            ret += 1
        fl >>= 1
    return ret    

# Количество бит восстановленной информации об исходной выборке lxtest системой рецептивных полей c 
# шириной S при исользовании функции расстояний fnDistance

def Accuracy(S, c, fnDistance):
    acc = 0
    for x in lxtest:
        dists = fnDistance(x, c)
        n = [int(np.exp(-(d / S) ** 2) * nPresentationTacts) for d in dists]
        wx = 0
        w = 0
        for i in range(len(c)):
            wx += n[i] * c[i]
            w += n[i]
        pred = round(wx / w) if w > 0 else 0
        acc += nCorrectBits(x, pred, 10)
    return acc

S = 0.6   # ширина рецептивных полей
logN = np.arange(np.log(5), np.log(110), (np.log(100) - np.log(5)) / 10)   # тестируемые числа рецептивных полей (логарифмы)

ratm = np.zeros(len(logN))   # среднее отношение объемов восстановленной информации в адаптивном и стандартном варианте
ratstddev = np.zeros(len(logN))   # станлаптное отклонение предыдущей величины
lN = []   # тестируемые числа рецептивных полей

for i in range(len(logN)):
    N = int(np.exp(logN[i]))
    relacc = np.zeros(10)
    for j in range(10):
        lxsample = []
        while len(lxsample) < nTestPoints:
            x = random.uniform(-1, 1)
            y = random.uniform(0, 1)
            if y < 1 - abs(x):
                lxsample.append((x + 1) * 512)
        lxsample.sort();
        lxtest = []
        while len(lxtest) < nTestPoints:
            x = random.uniform(-1, 1)
            y = random.uniform(0, 1)
            if y < 1 - abs(x):
                lxtest.append(int((x + 1) * 512))
        c = ReceptiveFieldCenters(N)
        old = Accuracy(S * 1024 / N, c, Distances)
        c = AdaptiveReceptiveFieldCenters(N)
        our = Accuracy(S, c, AdaptiveDistances)
        relacc[j] = our / old
    ratm[i] = np.mean(relacc)
    ratstddev[i] = np.std(relacc)
    lN.append(N)
    print(N, ratm[i], ratstddev[i])

ymin = ratm - ratstddev
ymax = ratm + ratstddev

fig, ax = plt.subplots(figsize=(10,4))
plt.fill_between(lN, ymin, ymax, alpha=0.2)
ax.set_xscale("log")
plt.xlabel('Количество рецептивных полей')
plt.show()
        