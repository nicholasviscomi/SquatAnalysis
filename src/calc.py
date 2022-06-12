import matplotlib.pyplot as plt
from typing import Any, List, Tuple, Dict
import numpy as np

def analyze_points(point_dict: Dict[np.signedinteger, Tuple[int, int]]):
    print(len(point_dict))
    print(point_dict)

    x_vals, y_vals = [], []
    time_vals = []
    for key, val in point_dict.items():
        time_vals.append(key)
        x_vals.append(val[0])
        y_vals.append(val[1])

    y_disp = [y - y_vals[0] for y in y_vals]

    plt.xlabel("Time (seconds)")
    plt.ylabel("Displacement (pixels)")
    plt.title("Displacement Over Time of a Barbell During a Squat")
    plt.scatter(time_vals, y_disp)

    plt.show()

    # x_vals, y_vals = map(list, zip(*points)) # https://stackoverflow.com/questions/68783326/unpack-list-of-list-python
    # start_x, start_y = x_vals[0], y_vals[0]

    # # find the x and y displacement, the distance from the origin
    # x_disp, y_disp = [x - start_x for x in x_vals], [y - start_y for y in y_vals]
    # print(len(x_disp))
    # print(len(y_disp))

    # max_y = 0
    # max_y_index = 0, 0
    # for i, y in enumerate(y_disp):
    #     if y > max_y:
    #         max_y = y
    #         max_y_index = i

    # # ----------------------DESCENT----------------------
    # # descent of a squat is from the beginning to the highest y-value
    # y_descent = y_disp[0: max_y_index]

    # # uses max_y_index because the descent points need to have the same length
    # x_descent = x_disp[0: max_y_index] 
    
    # # @params = 2 rows, 1 column, and this is the first (aka top) graph
    # plt.subplot(3, 1, 1)
    # plt.title("Filtered Squat Descent")
    # plt.scatter(x_descent, y_descent)

    # m, b = np.polyfit(x_descent, y_descent, 1)
    # y_descent = []
    # for elem in x_descent:
    #     x = np.float64(elem)
    #     y_descent.append((m * x) + b)
    #     # y_descent.append((a * (x**2)) + (b * x) + c)

    # plt.plot(time_vals[0 : max_y_index], y_descent, color='black')

    # # ----------------------ASCENT----------------------
    # # ascent of a squat is from the highest y-value (lowest point) back to the top
    # y_ascent = y_disp[max_y_index : ]

    # # uses max_y_index because the descent points need to have the same length
    # x_ascent = x_disp[max_y_index : ] 
    
    # # @params = 2 rows, 1 column, and this is the first (aka top) graph
    # plt.subplot(3, 1, 3)
    # plt.title("Filtered Squat Ascent")
    # plt.scatter(x_ascent, y_ascent)

    # m, b = np.polyfit(x_ascent, y_ascent, 1)
    # y_ascent = []
    # for elem in x_descent:
    #     x = np.float64(elem)
    #     y_ascent.append((m * x) + b)
    #     # y_descent.append((a * (x**2)) + (b * x) + c)
    
    # plt.plot(time_vals[max_y_index : ], y_ascent, color='black')
    
    # plt.show()