import random
Citys = []
CityNum = 20  # City Num
for i in range(CityNum):
    Citys.append([random.randint(100, 1400), random.randint(100, 1400)])  # range

# x
print("x")
for i in Citys:
    print(i[0])


# y
print("y")
for i in Citys:
    print(i[1])
