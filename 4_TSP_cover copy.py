import matplotlib.pyplot as plt
import random
import math
import turtle

p = 0.5
alpha = 1
beta = 5
iteratorNum = 50
antNum = 40
CityNum = 20
Citys = []
timeMatrix = []
pheromoneMtx = []


def distance(a, b):
    return math.sqrt(float((b[0]-a[0]) ** 2+(b[1]-a[1]) ** 2))


def getRouteLength(tabu):
    global p, alpha, beta, iteratorNum, antNum, CityNum, Citys, timeMatrix, pheromoneMtx
    length = 0
    for i in range(len(tabu)-1):
        length += timeMatrix[tabu[i]][tabu[i+1]]
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
            math.pow(1.0/timeMatrix[tabu[len(tabu)-1]][CityCnt], beta)

    pb = []
    for CityCnt in range(CityNum):
        if CityCnt in allowed:
            pb.append(math.pow(pheromoneMtx[tabu[len(tabu)-1]][CityCnt], alpha) * math.pow(
                1.0/timeMatrix[tabu[len(tabu)-1]][CityCnt], beta)/sum)
        else:
            pb.append(0.0)

    criticalPb = random.random()
    selectCity = 0
    sum1 = 0.0
    for CityCnt in range(CityNum):
        sum1 += pb[CityCnt]
        if (sum1 >= criticalPb and (CityCnt in allowed)):
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
                pheromoneMtx[i][j] += deltaPheromoneMtx[antCnt][i][j]


def TspSolve():
    global p, alpha, beta, iteratorNum, antNum, CityNum, Citys, timeMatrix, pheromoneMtx
    bestLength = 10000000000
    bestTour = []
    for ItNum in range(0, iteratorNum, 1):  # iteration
        deltaPheromoneMtx = []
        for antCnt in range(0, antNum, 1):  # ant-configuration

            tabu = []
            allowed = set(CityCnt for CityCnt in range(CityNum))

            # random start
            tabu.append(random.randint(0, CityNum-1))
            allowed.remove(tabu[0])
            for i in range(CityNum-1):
                selectNextCity(tabu, allowed)

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
    plot(bestTour)
    print(bestTour)
    print("bestLength:", bestLength)


def plot(Route):
    turtle.screensize(10000, 10000, "white")
    turtle.pensize(1)
    turtle.speed(100)
    turtle.pencolor("blue")
    turtle.penup()
    turtle.goto(Citys[Route[0]])
    turtle.pendown()
    for CityCnt in range(len(Route)):
        turtle.goto(Citys[Route[CityCnt]])
        turtle.dot(4, "red")
    turtle.hideturtle()
    ts = turtle.getscreen()
    ts.getcanvas().postscript(file="radar_cover.eps")
    turtle.done()


Citys = [[347, 128],
         [307, 1257],
         [599, 760],
         [521, 1332],
         [503, 1120],
         [246, 720],
         [365, 763],
         [740, 420],
         [884, 638],
         [505, 987],
         [1213, 243],
         [255, 848],
         [1085, 244],
         [1004, 448],
         [807, 1050],
         [1013, 1280],
         [190, 221],
         [969, 173],
         [1281, 440],
         [1135, 1021]]
initTimeMatrix()
initPheromoneMtx()
TspSolve()
