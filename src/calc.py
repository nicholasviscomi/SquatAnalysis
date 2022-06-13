import matplotlib.pyplot as plt
from typing import Any, List, Tuple, Dict
import numpy as np

# @param y_vals --> the y value of the center of the circle enclosing the fiducial
# @param time_vals --> tells how much time has elapsed at each frame
# @param isAScending --> denotes that the object being analyzed is going up. Since the
#   y coordinates in an image increase going down, the absolute value of the displacement 
#   needs to be taken. Otherwise, the displacement would be negative which is not what
#   is actually happening
def graph_calculus(y_vals: List, time_vals: List, isAscending: bool, title: str):
    # ~135 pixels = 2 inches (radius of real circle) ==> 67.5 pixels per real world inch
    ppi = 135/2
    y_disp = []
    start_y = pixels_to_inches(y_vals[0], ppi)
    for y in y_vals:
        y = pixels_to_inches(y, ppi)
        if isAscending:
            y_disp.append(abs(y - start_y))
        else:
            y_disp.append(y - start_y)
            

    plt.xlabel("Time (seconds)")
    plt.title(title)
    plt.scatter(time_vals, y_disp)

    #----------------------------------------
    # line of best fit: ax^2 + bx + c
    a, b, c = np.polyfit(time_vals, y_disp, 2)
    print(f"{a}x^2 + {b}x + {c}")

    lbf_vals = [ (a * (x**2) + (b * x) + c) for x in time_vals ]
    plt.plot(time_vals, lbf_vals, color='black', label='Displacement (in)')
    #----------------------------------------

    #----------------------------------------
    # velocity function (1st derivative)
    velocity_vals = [((2 * a * x) + b) for x in time_vals]
    plt.plot(time_vals, velocity_vals, color='red', label='Velocity (in/s)')
    #----------------------------------------

    #----------------------------------------
    # acceleration function (2nd derivative)
    acc_vals = [ 2 * a for _ in time_vals ]
    plt.plot(time_vals, acc_vals, color='orange', label='Acceleration(in/s^2)')
    #----------------------------------------

    #----------------------------------------
    # force = mass * acceleration
    # m = 95 / 2.2 # lbs --> kg
    # acc = 2 * a
    # force_vals = [ m * acc for _ in time_vals]

    # plt.subplot(1, 3, 2)
    # plt.plot(time_vals, force_vals, color='purple', label='Force')
    # #----------------------------------------

    # #----------------------------------------
    # # work = force * displacement
    # force = m * acc

    # max_y_index = y_disp.index(max(y_disp))
    # # distance traveled from beginning to maximum
    # dist_traveled = y_disp[max_y_index] - y_disp[0]

    # if max_y_index < (len(y_disp) - 1):
    #     # if there is more after the maximum, add it to the total
    #     dist_traveled += y_disp[max_y_index] - y_disp[len(y_disp) - 1]

    # work_vals = [ force * dist_traveled for _ in time_vals ]

    # plt.subplot(1, 3, 3)
    # plt.plot(time_vals, work_vals, color='brown', label='Work')
    #----------------------------------------


    plt.legend(loc='upper left')
    plt.show()

# @param n = number of pixels (the value being converted to inches)
# @param ppn = pixels per inch: raidus of the drawn circle / radius of real circle in inches
# returns value in inches
def pixels_to_inches(n, ppi):
    return n / ppi