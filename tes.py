import numpy as np
import random



matrix = [["1","1","1","1"],["2","2","2","2"],["3","3","3","3"],["4","4","4","4",]]
label = np.zeros((4,4))
for i in range(len(matrix)):
    matrix[i][0] +=  matrix[i][0] 
    label[i][0] = 1


def findZero(inputlist):
    # print(inputlist)
    for j in range(len(inputlist)):
        if inputlist[j] == 0:
            print(j)
            return j


def checkFull(label):
    for j in label:
        if j == 0:
            return False
    return True


m = 0
for i in range(len(matrix)):
    m = i + 1
    for j in range(len(matrix[0])):
        if label[i][j] == 0:
            
            k = findZero(label[m])
            temp = matrix[i][j]
            matrix[i][j] += matrix[m][k]
            matrix[m][k] += temp
            label[i][j] = 1
            label[m][k] = 1

            m += 1

            print(i,j,m, k)
            print(matrix)
            print(label)
            





for i , j in range(10),range(2):
    print(i,j)

            
        