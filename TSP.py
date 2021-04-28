import random
import math

p = 0.7
alpha = 1
beta = 5
iteratorNum = 10
antNum = 10
CityNum = 10
Citys = []
timeMatrix = []
pheromoneMtx = []


def distance(a, b):
    return math.sqrt(float((b[0]-a[0]) ** 2+(b[1]-a[1]) ** 2))


def getRouteLength(tabu):
    global p, alpha, beta, iteratorNum, antNum, CityNum, Citys, timeMatrix, pheromoneMtx
    length = 0
    for i in range(len(tabu)-1):
        length += distance(Citys[tabu[i]], Citys[tabu[i+1]])
    return length


def initTimeMatrix():
    global p, alpha, beta, iteratorNum, antNum, CityNum, Citys, timeMatrix, pheromoneMtx
    for i in range(CityNum):
        timeMatrix_i = []
        for j in range(CityNum):
            timeMatrix_i.append(distance(Citys[i], Citys[j]))
        timeMatrix.append(timeMatrix_i)


def initPheromoneMtx():
    global p, alpha, beta, iteratorNum, antNum, CityNum, Citys, timeMatrix, pheromoneMtx
    pheromoneMtx = [[0.2 for i in range(CityNum)]for i in range(CityNum)]


def selectNextCity(tabu, allowed):
    global p, alpha, beta, iteratorNum, antNum, CityNum, Citys, timeMatrix, pheromoneMtx
    sum = 0.0
    for CityCnt in allowed:
        sum += math.pow(pheromoneMtx[tabu[len(tabu)-1]][CityCnt], alpha) * \
            math.pow(1.0/timeMatrix[len(tabu)-1][CityCnt], beta)

    pb = []
    for i in range(CityNum):
        flag = False
        for j in allowed:
            if(i == j):
                pb.append(math.pow(pheromoneMtx[tabu[len(tabu)-1]][CityCnt], alpha) * math.pow(
                    1.0/timeMatrix[len(tabu)-1][CityCnt], beta)/sum)
                flag = true
                break
        if (flag == False):
            pb.append(0.0)

    criticalPb = random.random()
    selectCity = 0
    sum1 = 0.0
    for CityCnt in range(CityNum):
        sum1 += pb[CityCnt]
        if (sum1 >= criticalPb):
            selectCity = CityCnt
            break

    allowed.remove(selectCity)
    tabu.append(selectCity)


def updatePheromoneMtx(deltaPheromoneMtx):
    global p, alpha, beta, iteratorNum, antNum, CityNum, Citys, timeMatrix, pheromoneMtx
    for i in range(CityNum):
        for j in range(CityNum):
            pheromoneMtx[i][j] *= p
    for i in range(CityNum):
        for j in range(CityNum):
            for antCnt in range(antNum):
                pheromoneMtx[i][j] += deltaPheromoneMtx[k][i][j]


def TspSolve():
    global p, alpha, beta, iteratorNum, antNum, CityNum, Citys, timeMatrix, pheromoneMtx
    bestlength = 10000000000
    bestTour = []
    for itCnt in range(0, iteratorNum, 1):  # iteration
        deltaPheromoneMtx = []
        for antCnt in range(0, antNum, 1):  # ant-configuration

            tabu = []
            allowed = set(CityCnt for CityCnt in range(CityNum))

            # random start
            tabu.append(random.randint(0, CityNum-1))
            allowed.remove(tabu[0])
            for i in range(CityNum-1):
                tabu.append(selectNextCity(tabu, allowed))
            # return to first city
            tabu.append(tabu[0])

            antLength = getRouteLength(tabu)
            if (antLength < bestLength):
                bestLength = antLength
                bestTour = tabu

            deltaPheromoneMtx_i = [
                [0 for i in range(CityNum)]for j in range(CityNum)]
            for i in range(len(tabu)-1):
                deltaPheromoneMtx_i[tabu[i]][tabu[i+1]
                                             ] = deltaPheromoneMtx_i[tabu[i+1]][tabu[i]] = float(1.0/antLength)
            deltaPheromoneMtx.append(deltaPheromoneMtx_i)
        updatePheromoneMtx(deltaPheromoneMtx)


for i in range(CityNum):
    Citys.append([random.randint(0, 100), random.randint(0, 100)])
# print("citys: ", Citys, "\n")
initTimeMatrix()
# print("timeMatrix: ", timeMatrix, "\n")
initPheromoneMtx()
print("timeMatrix: ", timeMatrix, "\n")
TspSolve()


# tabu = []
# allowed = set(CityCnt for CityCnt in range(CityNum))
# print("allowed: ", allowed, "\n")
# print("tabu: ", tabu, "\n")
# tabu.append(random.randint(0, CityNum-1))
# allowed.remove(tabu[0])
# print("allowed: ", allowed, "\n")
# print("tabu: ", tabu, "\n")
