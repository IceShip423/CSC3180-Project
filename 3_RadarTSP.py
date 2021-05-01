import matplotlib.pyplot as plt
import random
import math
import turtle
import copy

# TSP parameter
p = 0.5
alpha = 1
beta = 5
iteratorNum = 50
antNum = 40
# City info
CityNum = 21
Citys = []
# TSP data
timeMatrix = []
pheromoneMtx = []
# Radar
radarCenter = [0, 0]
radarRadius = 50.0


def distance(a, b):  # return distance between vector2 a, b
    return math.sqrt(float((b[0]-a[0]) ** 2+(b[1]-a[1]) ** 2))


def getRouteLength(tabu):  # return length of a tour
    global p, alpha, beta, iteratorNum, antNum, CityNum, Citys, timeMatrix, pheromoneMtx, radarRadius
    length = 0
    for i in range(len(tabu)-1):
        length += timeMatrix[tabu[i]][tabu[i+1]]
    return length


def initTimeMatrix():  # timeMatrix[i][j] -> distance from i to j
    global p, alpha, beta, iteratorNum, antNum, CityNum, Citys, timeMatrix, pheromoneMtx, radarRadius
    timeMatrix = [[0 for i in range(CityNum)]for i in range(CityNum)]
    for i in range(CityNum-1):
        for j in range(CityNum-1):
            timeMatrix[i][j] = distance(Citys[i], Citys[j])
    # index CityNum-1 is used as radar boarder
    for i in range(CityNum-1):
        timeMatrix[CityNum-1][i] = timeMatrix[i][CityNum -
                                                 1] = radarRadius - distance(Citys[i], Citys[CityNum-1])


def initPheromoneMtx():  # pheromoneMtx[i][j] -> pheromone from i to j
    global p, alpha, beta, iteratorNum, antNum, CityNum, Citys, timeMatrix, pheromoneMtx, radarRadius
    pheromoneMtx = [[0.2 for i in range(CityNum)]for i in range(CityNum)]


# choose the next city to go to, based on tabu and allowed
def selectNextCity(tabu, allowed):
    global p, alpha, beta, iteratorNum, antNum, CityNum, Citys, timeMatrix, pheromoneMtx, radarRadius
    # calculate probability of each road
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
    # roulette process
    criticalPb = random.random()
    selectCity = 0
    sum1 = 0.0
    for CityCnt in range(CityNum):
        sum1 += pb[CityCnt]
        if (sum1 >= criticalPb and (CityCnt in allowed)):
            selectCity = CityCnt
            break
    # update tabu list
    allowed.remove(selectCity)
    tabu.append(selectCity)


# after each iteraation, update pheromoneMtx
def updatePheromoneMtx(deltaPheromoneMtx):
    global p, alpha, beta, iteratorNum, antNum, CityNum, Citys, timeMatrix, pheromoneMtx, radarRadius
    for i in range(CityNum):
        for j in range(CityNum):
            pheromoneMtx[i][j] *= p
    for i in range(CityNum):
        for j in range(CityNum):
            for antCnt in range(antNum):
                pheromoneMtx[i][j] += deltaPheromoneMtx[antCnt][i][j]


def TspSolve():  # Solve TSP
    global p, alpha, beta, iteratorNum, antNum, CityNum, Citys, timeMatrix, pheromoneMtx, radarRadius
    bestLength = 10000000000
    bestTour = []
    for ItNum in range(0, iteratorNum, 1):  # iteration
        deltaPheromoneMtx = []
        for antCnt in range(0, antNum, 1):  # ant-configuration

            # initialize tabu
            tabu = []
            allowed = set(CityCnt for CityCnt in range(CityNum))

            # random start
            tabu.append(random.randint(0, CityNum-1))
            allowed.remove(tabu[0])
            for i in range(CityNum-1):
                selectNextCity(tabu, allowed)
            # return to first city
            tabu.append(tabu[0])

            # keep the best solution
            antLength = getRouteLength(tabu)
            if (antLength < bestLength):
                bestLength = antLength
                bestTour = tabu

            # left pheromone in path
            deltaPheromoneMtx_i = [
                [0 for i in range(CityNum)]for j in range(CityNum)]
            for i in range(len(tabu)-1):
                deltaPheromoneMtx_i[tabu[i]][tabu[i+1]
                                             ] = deltaPheromoneMtx_i[tabu[i+1]][tabu[i]] = float(1.0/antLength)
            deltaPheromoneMtx.append(deltaPheromoneMtx_i)
        # update pheromone
        updatePheromoneMtx(deltaPheromoneMtx)
    # form coordinate route based on tour
    Route = FormalizeRoute(copy.deepcopy(bestTour[0:len(bestTour)-1]))
    # Result
    print("bestLength:", bestLength)
    print("solution:")
    # x,y
    for i in Route:
        print(i[0], i[1])
    plot(Route)


def FormalizeRoute(Tour):  # form coordinate route based on tour
    global p, alpha, beta, iteratorNum, antNum, CityNum, Citys, timeMatrix, pheromoneMtx, radarRadius
    idx = Tour.index(CityNum-1)
    Tour = Tour[idx+1:]+Tour[0:idx]
    Route = []
    for CityCnt in Tour:
        Route.append(Citys[CityCnt])
    Route = [[Route[0][0]*radarRadius/distance(Route[0], (0, 0)),
              Route[0][1]*radarRadius/distance(Route[0], (0, 0))]]+Route+[[Route[len(Route)-1][0]*radarRadius/distance(Route[len(Route)-1], (0, 0)),
                                                                           Route[len(Route)-1][1]*radarRadius/distance(Route[len(Route)-1], (0, 0))]]
    return Route


def plot(Route):
    global p, alpha, beta, iteratorNum, antNum, CityNum, Citys, timeMatrix, pheromoneMtx, radarRadius
    # pen set
    turtle.screensize(1000, 1000, "white")
    turtle.pensize(1)
    turtle.speed(100)
    turtle.pencolor("blue")
    # draw boarder
    turtle.penup()
    turtle.goto(0, -radarRadius)
    turtle.pendown()
    turtle.circle(radarRadius)
    turtle.penup()
    # draw route
    turtle.goto(Route[0])
    turtle.pendown()
    for CityCnt in range(len(Route)):
        turtle.goto(Route[CityCnt])
        turtle.dot(3, "red")
    turtle.mainloop()


Citys = []
for i in range(CityNum-1):
    Citys.append([random.randint(-35, 35), random.randint(-35, 35)])
Citys.append(radarCenter)  # the last 'node' is radar boarder
initTimeMatrix()
initPheromoneMtx()
print("problem:")
# x,y
for i in Citys:
    print(i[0], " ", i[1])
TspSolve()
