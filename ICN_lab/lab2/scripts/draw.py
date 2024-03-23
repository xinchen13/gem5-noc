import matplotlib.pyplot as plt
import numpy as np
import math

injection_rate = np.arange(0.02, 1, 0.02).tolist()

topology = ["mesh", "flattenedbutterfly"]
traffic = ["uniform_random", "tornado", "neighbor"]
curve_1 = []
curve_2 = []

for traf in traffic:
    # read from files: mesh
    curve_1.clear()
    f_1 = open("./results/" + topology[0] + "_" + traf + ".txt")
    line = f_1.readline() # drop "average packet latency"
    line = f_1.readline()
    while(line):               
        print(line, end = '')
        curve_1.append(math.log(float(line)))
        line = f_1.readline()  
    f_1.close()  
    # read from files: flattenedbutterfly
    curve_2.clear()
    f_2 = open("./results/" + topology[1] + "_" + traf + ".txt")
    line = f_2.readline() # drop "average packet latency"
    line = f_2.readline()
    while(line):               
        print(line, end = '')
        curve_2.append(math.log(float(line)))
        line = f_2.readline()  
    f_2.close() 
    # plot and save the fig
    plt.plot(injection_rate[0:-10], curve_1[0:-10], label='Mesh_XY - '+traf, marker='o')
    plt.plot(injection_rate[0:-10], curve_2[0:-10], label='FlattenedButterfly - '+traf, marker='o')
    plt.title("average packet latency VS injection rate")
    plt.xlabel('injection rate')
    plt.ylabel('log(average packet latency)')
    plt.legend()
    plt.savefig("./results/" + traf + ".png")
    plt.clf()
