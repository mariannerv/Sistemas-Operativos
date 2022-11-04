import os, time

sum=0
def calc_sum(num):
    global sum
    for i in range(num+1):
        sum += i
    print ("soma na funcao: ", str(sum))
n=5
