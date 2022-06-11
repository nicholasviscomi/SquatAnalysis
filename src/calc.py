import matplotlib.pyplot as plt
from typing import List

import numpy as np

def analyze_points(points: List[list]):
    # x_vals, y_vals = map(list, zip(*points)) # https://stackoverflow.com/questions/68783326/unpack-list-of-list-python
    # start_x, start_y = x_vals[0], y_vals[0]

    # find the x and y displacement, the distance from the origin
    # x_disp, y_disp = [x - start_x for x in x_vals], [y - start_y for y in y_vals]
    x_disp = [0, 6, 1, -1, 3, 3, 15, 19, 8, 27, 28, 36, 28, 45, 63, 71, 72, 82, 86, 92, 100, 116, 126, 131, 134, 142, 150, 161, 164, 168, 181, 182, 216, 211, 219, 216, 202, 207, 212, 206, 207, 223, 224, 224, 224, 227, 232, 232, 238, 248, 244, 242, 225, 220, 222, 211, 224, 198, 191, 154, 148, 168, 167, 129, 110, 109, 108, 109, 86, 94, 117, 71, 97, 110, 60, 92, 93, 94, 57, 90]
    y_disp = [0, 3, -11, -17, -16, -11, 15, 35, 48, 97, 138, 192, 246, 322, 416, 504, 589, 684, 769, 860, 954, 1061, 1159, 1245, 1328, 1416, 1503, 1586, 1651, 1712, 1777, 1820, 1930, 1940, 1961, 1975, 1974, 1984, 1992, 1985, 1985, 1996, 1995, 1992, 1990, 1992, 1990, 1976, 1964, 1952, 1930, 1824, 1730, 1648, 1570, 1478, 1400, 1279, 1172, 1163, 1049, 827, 714, 697, 584, 476, 377, 291, 210, 159, 137, 96, 101, 107, 93, 105, 101, 96, 82, 97]
    print(x_disp)
    print(y_disp)


    max_y = 0
    max_y_index = 0, 0
    for i, y in enumerate(y_disp):
        if y > max_y:
            max_y = y
            max_y_index = i

    # ----------------------DESCENT----------------------
    # descent of a squat is from the beginning to the highest y-value
    y_descent = y_disp[0: max_y_index]
    # uses max_y_index because the descent points need to have the same length
    x_descent = x_disp[0: max_y_index] 
    
    # @params = 2 rows, 1 column, and this is the first (aka top) graph
    plt.subplot(3, 1, 1)
    plt.title("Squat Descent")
    plt.scatter(x_descent, y_descent)

    m, b = np.polyfit(x_descent, y_descent, 1)
    plt.plot(x_descent, m * np.float64(x_descent) + b, color='black')


    # ----------------------ASCENT----------------------
    # ascent of a squat is from the highest y-value (lowest point) back to the top
    y_ascent = y_disp[max_y_index: ]
    # uses max_y_index because the descent points need to have the same length
    x_ascent = x_disp[max_y_index: ] 
    
    # @params = 2 rows, 1 column, and this is the first (aka top) graph
    plt.subplot(3, 1, 3)
    plt.title("Squat Ascent")
    plt.scatter(x_ascent, y_ascent)

    m, b = np.polyfit(x_ascent, y_ascent, 1)
    plt.plot(x_ascent, m * np.float64(x_ascent) + b, color='black')

    plt.show()
