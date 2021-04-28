import random
import math

# aca parameters
iteratorNum = 100
antNum = 100
p = 0.5
q = 2
# ......
timeMtx = []
pheromoneMtx = []
maxPheromoneMtx = []
criticalPointMtx = []
resultData = []


def initRandomArray(Num, LowerBound, UpperBound):
    Array = list()
    for i in range(Num):
        Array.append(float(random.randint(LowerBound, UpperBound)))
    return Array


def initMtx(Rows, Cols, Val):
    return [[Val for i in range(Cols)]for j in range(Rows)]


def initTimeMtx(tasks=[], nodes=[]):
    global antNum, iteratorNum, p, q, timeMtx, pheromoneMtx, maxPheromoneMtx, criticalPointMtx, resultData
    timeMtx = []
    for i in range(0, len(tasks), 1):
        timeMtx_i = []
        for j in range(0, len(nodes), 1):
            timeMtx_i.append(tasks[i]/nodes[j])
        timeMtx.append(timeMtx_i)


def initPheromoneMtx(tasks, nodes):
    global antNum, iteratorNum, p, q, timeMtx, pheromoneMtx, maxPheromoneMtx, criticalPointMtx, resultData
    pheromoneMtx = []
    for i in range(0, len(tasks), 1):
        pheromoneMtx_i = []
        for j in range(0, len(nodes), 1):
            pheromoneMtx_i.append(1.0)
        pheromoneMtx.append(pheromoneMtx_i)


def assignOneTask(antCnt, taskCnt, nodes):
    global antNum, iteratorNum, p, q, timeMtx, pheromoneMtx, maxPheromoneMtx, criticalPointMtx, resultData
   # print(antCnt, "  ", criticalPointMtx, "  ",
    #    criticalPointMtx[taskCnt], "\n")
    if (antCnt <= criticalPointMtx[taskCnt]):
        return maxPheromoneMtx[taskCnt]
    else:
        return random.randint(0, len(nodes)-1)


def callTime_oneIt(pathMtx_allAnt, tasks, nodes):
    global antNum, iteratorNum, p, q, timeMtx, pheromoneMtx, maxPheromoneMtx, criticalPointMtx, resultData
    time_allAnt = []
    for antIdx in range(0, len(pathMtx_allAnt), 1):
        pathMtx = pathMtx_allAnt[antIdx]
        maxTime = -1
        for nodeIdx in range(0, len(nodes), 1):
            time = 0
            for taskIdx in range(0, len(tasks), 1):
                if (pathMtx[taskIdx][nodeIdx] == 1):
                    time += timeMtx[taskIdx][nodeIdx]
            if (time > maxTime):
                maxTime = time
        time_allAnt.append(maxTime)
    return time_allAnt


def updatePheromoneMtx(pathMtx_allAnt, timeArray_oneIt, tasks, nodes):
    global antNum, iteratorNum, p, q, timeMtx, pheromoneMtx, maxPheromoneMtx, criticalPointMtx, resultData
    for i in range(0, len(tasks), 1):
        for j in range(0, len(nodes), 1):
            pheromoneMtx[i][j] *= p

    minTime = 100000000
    minIdx = -1
    for antIdx in range(0, antNum, 1):
        if (timeArray_oneIt[antIdx] < minTime):
            minTime = timeArray_oneIt[antIdx]
            minIdx = antIdx

    for taskIdx in range(0, len(tasks), 1):
        for nodeIdx in range(0, len(nodes), 1):
            if(pathMtx_allAnt[minIdx][taskIdx][nodeIdx] == 1):
                pheromoneMtx[taskIdx][nodeIdx] *= q

    maxPheromoneMtx = []
    criticalPointMtx = []
    for taskIdx in range(0, len(tasks), 1):
        maxPheromone = pheromoneMtx[taskIdx][0]
        maxIdx = 0
        sumPheromone = pheromoneMtx[taskIdx][0]
        isAllSame = True

        for nodeIdx in range(1, len(nodes), 1):
            if (pheromoneMtx[taskIdx][nodeIdx] > maxPheromone):
                maxPheromone = pheromoneMtx[taskIdx][nodeIdx]
                maxIdx = nodeIdx

            if (pheromoneMtx[taskIdx][nodeIdx] != pheromoneMtx[taskIdx][nodeIdx-1]):
                isAllSame = False

            sumPheromone += pheromoneMtx[taskIdx][nodeIdx]

        if (isAllSame == True):
            maxIdx = random.randint(0, len(nodes)-1)
            maxPheromone = pheromoneMtx[taskIdx][maxIdx]

        maxPheromoneMtx.append(maxIdx)
        criticalPointMtx.append(int(antNum*(maxPheromone/sumPheromone)))


def acaSearch(tasks, nodes):
    global antNum, iteratorNum, p, q, timeMtx, pheromoneMtx, maxPheromoneMtx, criticalPointMtx, resultData
    for itCnt in range(0, iteratorNum, 1):  # iteration
        pathMtx_allAnt = []
        for antCnt in range(0, antNum, 1):  # ant-configuration
            pathMtx_oneAnt = initMtx(len(tasks), len(nodes), 0)
            for taskCnt in range(0, len(tasks), 1):  # task assignment
                nodeCnt = assignOneTask(antCnt, taskCnt, nodes)
                pathMtx_oneAnt[taskCnt][nodeCnt] = 1
            pathMtx_allAnt.append(pathMtx_oneAnt)
        timeArray_oneIt = callTime_oneIt(pathMtx_allAnt, tasks, nodes)
        resultData.append(timeArray_oneIt)
        updatePheromoneMtx(pathMtx_allAnt, timeArray_oneIt, tasks, nodes)


def acaAlgorithm(tasks=[], nodes=[]):
    global antNum, iteratorNum, p, q, timeMtx, pheromoneMtx, maxPheromoneMtx, criticalPointMtx, resultData
    # initialization
    initTimeMtx(tasks, nodes)
    initPheromoneMtx(tasks, nodes)
    criticalPointMtx = [-1 for i in range(len(tasks))]
    # iteration & search
    acaSearch(tasks, nodes)

    # final config
    nodeProcessTasks = []
    for i in range(len(nodes)):
        nodeProcessTasks_i = []
        for j in range(len(tasks)):
            if(maxPheromoneMtx[j] == i):
                nodeProcessTasks_i.append(j)
        nodeProcessTasks.append(nodeProcessTasks_i)

    for i in range(len(nodes)):
        print(i, ": ", nodeProcessTasks[i])

    # history total time

    print("resultData:(time for one ant)", resultData, "\n")


# if __name__ == "main":
# problem data
tasks = initRandomArray(100, 10, 100)
nodes = initRandomArray(10, 10, 100)
print("tasks: ", tasks, "\n")
print("nodes: ", nodes, "\n")
# Run
acaAlgorithm(tasks, nodes)
