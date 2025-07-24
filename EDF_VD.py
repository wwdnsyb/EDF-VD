import random as r
from math import gcd
import sys
from os import system, name

# ************************* 清屏功能相关部分 *************************
# define our clear function
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

clear()

# ************************* 读取任务集相关部分 *************************
# Reading Task Set
def Task_Set():
    Temp = []
    Task_Set = []
    Tasks = []
    # Reading file to a list
    data = open('Tasks.txt', 'r', encoding='utf-8')
    # data.seek(22)  # 不再跳过首行，直接读取全部
    tasks = data.readlines()
    for line in tasks:
        stripped_task = line.strip('\n')
        Temp.append(stripped_task)
    # split item
    for i in Temp:
        li = list(i.split(","))
        Tasks.append(li)
    # 只转换数值字段，名称和描述保留字符串
    for task in Tasks:
        Task_Set.append([
            int(task[0]),      # 任务ID
            task[1],           # 任务名称
            task[2],           # 任务描述
            int(task[3]),      # C(LO)
            int(task[4]),      # C(HI)
            int(task[5]),      # D
            int(task[6]),      # P
            int(task[7])       # L
        ])
    # 保持原始字段顺序，不再插入额外字段，保证与后续索引兼容
    return Task_Set

tasks = Task_Set()
tasks_show = Task_Set()
n = len(tasks)
# print(Len_Task_Set)

# ************************* 计算X参数相关部分 *************************
def X(tasks, n):
    u_lo_lo, u_hi, u_lo_hi, u_lo_total = 0, 0, 0, 0
    for i in range(n):
        if tasks[i][7] == 0:  # L
            u_lo_lo += tasks[i][3] / tasks[i][6]  # C(LO)/P
        elif tasks[i][7] == 1:
            u_hi += tasks[i][4] / tasks[i][6]     # C(HI)/P
            u_lo_hi += tasks[i][3] / tasks[i][6]  # C(LO)/P
        else:
            break
    u_lo_total = u_lo_lo + u_lo_hi
    X = u_lo_hi / (1 - u_lo_lo) if (1 - u_lo_lo) != 0 else 0
    chk = X * u_lo_lo + u_hi
    if chk <= 1:
        return round(X, 2)
    else:
        return 1

X = X(tasks, n)

# ************************* 展示任务相关部分 *************************
def show_Tasks(Task_show, n, X):
    for i in range(n):
        if tasks_show[i][7] > 0:
            tasks_show[i].append(round(X * tasks[i][3], 2))  # VD = X * C(LO)
        else:
            tasks_show[i].append('-')
    return tasks_show

show = show_Tasks(tasks_show, n, X)
print("TID\tC(LO)\tC(HI)\tD\tP\tL\tRT\tVD")
for i in show:
    print("")
    for j in i:
        print(j, end='\t')
print("\n")

# ************************* 提取高临界任务相关部分 *************************
def tasks_HI():
    tasks = Task_Set()
    n = len(tasks)
    tasks_HI = []
    for i in range(n):
        if tasks[i][7] == 1:
            tasks_HI.append(tasks[i])
        else:
            tasks_HI.append(0)
    return tasks_HI

tasks_HI = tasks_HI()

# ************************* 处理低临界任务相关部分 *************************
def tasks_LO(X):
    tasks = Task_Set()
    n = len(tasks)
    tasks_LO = []
    for i in range(n):
        tasks_LO.append(tasks[i])
        if tasks_LO[i][7] == 1:
            tasks_LO[i][3] = X * tasks_LO[i][3]
            # tasks_LO[i][2]=tasks_LO[i][3]
    return tasks_LO

tasks_LO = tasks_LO(X)
# print("\nQLO:",tasks_LO)
# print("QHI:",tasks_HI)

# ************************* 计算超周期（最小公倍数）相关部分 *************************
# Calculating Hyper Perios as LCM
def LCM(Task_Set):
    P = []
    for i in range(n):
        P.append(tasks[i][6])
    lcm = P[0]
    for i in P[1:]:
        lcm = int(lcm * i / gcd(lcm, i))
    return lcm

lcm = LCM(Task_Set)
print("Hyper Period is: ", lcm)
print("X-parameter is : %s" % (X))

# ************************* 计算利用率相关部分 *************************
def utilization(Task_Set, Len_Task_Set, X):
    u_lo_lo, u_hi_lo, u_hi, u_lo_hi, u_lo_total, u_hi_total = 0, 0, 0, 0, 0, 0
    for i in range(n):
        if show[i][7] == 0:
            u_lo_lo += show[i][3] / show[i][6]
            u_hi_lo += show[i][4] / show[i][6]
        elif show[i][7] == 1:
            u_hi += show[i][4] / show[i][6]
            u_lo_hi += show[i][3] / show[i][6]
        else:
            break
    if X == 0:
        print("警告：X参数为0，无法计算利用率，可能是任务集参数设置不合理导致。")
        return None
    u_lo_total = u_lo_lo + (u_lo_hi / X)
    u_hi_total = X * u_lo_lo + (1 - X) * u_hi_lo + u_hi
    print("Utilization in Low Criticality mode: %s" % round(u_lo_total, 2))
    print("Utilization in High Criticality mode: %s" % round(u_hi_total, 2))
    if u_hi_total <= 1 and u_lo_total <= 1:
        return 1
    else:
        return 2

util = utilization(tasks, n, X)
# print('utilization of task set is %s'%util,end='\n')
print()

# ************************* 计算剩余时间相关部分 *************************
def TimeLeft(Task_Set, Len_Task_Set):
    time_left = []
    for i in range(Len_Task_Set):
        if Task_Set[i][6] == 0:
            time_left.append(Task_Set[i][1])
        else:
            time_left.append(int(0))
    return time_left

timeLeft = TimeLeft(tasks, n)
# print('\nTime left set:\n%s\n\n'%timeLeft)

# ************************* 数组排序相关部分 *************************
def array_sort(instances, index=1):
    for i in range(len(instances)):
        tmp = instances[i].copy()
        k = i
        while k > 0 and tmp[index] < instances[k - 1][index]:
            instances[k] = instances[k - 1].copy()
            k -= 1
        instances[k] = tmp.copy()
    return instances

# ************************* EDF-VD调度算法相关部分 *************************
def EDF_VD(tasks, n, lcm, util):
    i = 0
    instances = []
    for i in range(n):
        j = 0
        while 1:
            if tasks[i][3] + j * tasks[i][6] <= lcm:
                instances.append([[tasks[i][0], tasks[i][1], tasks[i][2], tasks[i][3] + j * tasks[i][6],
                                   (j + 1) * tasks[i][3], tasks[i][5], 0], j * tasks[i][3]])
                j += 1
                # f tasks[i][5]==1:
                #   instances[0][6]=X*(j+1)*tasks[i][3]
            else:
                break

        # for k in range(n):
        #    print(tasks[k])
        # for i in range(len(instances)):
        #    print(instances[i])

    instances = array_sort(instances)
    # for x in range(len(instances)):
    #    print(instances[x])
    timeLine = []
    time = 0
    while (time < lcm):
        if util == 1:
            sig = 1
            last_criticality = criticality = 0
            while time < lcm:
                for i in range(n):
                    if (time > 1 and ((time % tasks[i][3] == 0 and time > tasks[i][6]) or
                                      time == tasks[i][6])):  # or (last_criticality!=criticality and timeLeft[i]==tasks[i][1]):
                        if criticality == 1:
                            timeLeft[i] = tasks[i][2]
                        elif criticality == 0:
                            timeLeft[i] = tasks[i][1]
                last_criticality = criticality
                anyrun = 0
                for j in range(len(instances)):
                    is_break = False
                    is_pop = False

                    # a=input("bede:")
                    if timeLeft[instances[j][0][0] - 1] > 0:
                        for k in range(j + 1, len(instances)):
                            if j < len(instances) - 1 and \
                                    (instances[j][1] == instances[k][1] or (time >= instances[k][1] and (
                                            instances[j][0][5] < instances[k][0][5] \
                                            or (instances[j][0][5] == 1 and instances[k][0][5] == 1)))) and (
                                    (criticality == 0 and \
                                     instances[k][1] + tasks_LO[instances[k][0][0] - 1][3] < instances[j][1] + tasks_LO[
                                         instances[j][0][0] - 1][3]) or \
                                    (criticality == 1 and instances[k][1] + instances[k][0][3] < instances[j][1] + instances[j][0][3])):

                                instances[j], instances[k] = instances[k], instances[j]

                        # if criticality==1 and instances[j][0][5]==0:
                        #    criticality=0
                        if criticality == 0 or (criticality == 1 and instances[j][0][5] >= 0):
                            if time + timeLeft[instances[j][0][0] - 1] > instances[j][1] + instances[j][0][3]:
                                timeLine.append(['%s X' % instances[j][0][0], criticality])
                                if time + 1 == instances[j][1] + instances[j][0][3]:
                                    timeLeft[instances[j][0][0] - 1] = 1
                            else:
                                timeLine.append([instances[j][0][0], criticality])
                            timeLeft[instances[j][0][0] - 1] -= 1
                            anyrun = 1
                            if timeLeft[instances[j][0][0] - 1] == 0:
                                is_pop = True
                            is_break = True
                    # timespend
                    time_spend = {}
                    for i in range(n):
                        time_spend[tasks[i][0]] = 0
                        # print('lll',len(timeLine))
                        for k in range(len(timeLine) - 1, -1, -1):
                            # print(tasks[i][0],timeLine[k][0])
                            if tasks[i][0] == timeLine[k][0] and timeLine[k][0]!= str(tasks[i][0]) + " X":
                                time_spend[tasks[i][0]] += 1
                            else:
                                break
                    # print("___",timeLine)
                    # print("___",time_spend)
                    # Overrun Mode
                    if anyrun == 1 and instances[j][0][5] > 0 and timeLeft[instances[j][0][0] - 1] == 0 and criticality == 0:
                        signal = int(input("Task (" + str(instances[j][0][0]) + ") Time (" + str(time + 1) + ") signal %d/0:" % (
                        sig)))
                        # signal =r.randint(1, 1)
                        if sig == signal:
                            print('No Completion Signal for Task %s at %s' % (instances[j][0][0], time + 1))
                            timeLeft[instances[j][0][0] - 1] = (instances[j][0][2] - instances[j][0][1])

                            temp = 1
                            for k in range(j + 1, len(instances)):
                                if instances[k][0][0] == instances[j][0][0]:
                                    temp = k
                                    break
                            for k in range(len(instances) - 1, j, -1):
                                if instances[k][0][5] == 1:
                                    # print(instances[k][0][0],time_spend[instances[k][0][0]],timeLeft[instances[k][0][0]-1],instances[k][0][2])
                                    timeLeft[instances[k][0][0] - 1] = instances[k][0][2] - time_spend[instances[k][0][0]]
                                if instances[k][0][5] == 0 and instances[k][1] >= instances[j][1] and instances[k][1] <= instances[
                                    temp][1]:
                                    if time_spend[instances[k][0][0]] >= instances[k][0][2]:
                                        timeLeft[instances[k][0][0] - 1] = 0
                                        is_pop = True
                                        # instances.pop(k)
                                    else:
                                        timeLeft[instances[k][0][0] - 1] = instances[k][0][2]  # - time_spend[instances[k][0][0]]
                                        # instances.pop(k)

                                    if is_pop and k == j:
                                        is_pop = False

                            criticality = 1
                            is_pop = False
                            is_break = True

                    if is_pop:
                        instances.pop(j)
                    if is_break:
                        break
                if anyrun == 0:
                    timeLine.append(['-', 'I'])
                    criticality = 0
                time += 1
            mn = 0
            mx = 0

            print('Starting Scheduling Task Set:', end='\n')
            print('*********************************************************************')
            print("* Start Time\t", "End Time\t", "Task ID\t", "System Criticality *")
            for i in range(lcm):
                if i > 0 and (timeLine[i][0]!= timeLine[i - 1][0] or timeLine[i][1]!= timeLine[i - 1][1]):
                    mx = i
                    print("*", mn, "\t\t", mx, "\t\t", "[" + str(timeLine[i - 1][0]) + "]\t\t\t", timeLine[mn][1],
                          "\t    *")

                    mn = i
                if i == lcm - 1:
                    mx = lcm
                    print("*", mn, "\t\t", mx, "\t\t", "[" + str(timeLine[i][0]) + "]\t\t\t", timeLine[mn][1],
                          "\t    *")
            print('*********************************************************************')
        else:
            print('Task set is not feasible.(Utilization Must be <=1.)')
            break

# for x in range(100):
c(tasks, n, lcm, util)