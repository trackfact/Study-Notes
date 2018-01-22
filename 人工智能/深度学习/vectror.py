'''
qqqqqqqqq
'''
import time
import numpy as np

a = np.random.rand(1000000)

print(a)

b = np.random.rand(1000000)

tic = time.time()

c = np.dot(a,b)


toc = time.time()

print(tic)