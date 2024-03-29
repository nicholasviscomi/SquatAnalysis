import matplotlib.pyplot as plt
from typing import List
import numpy as np

# @param y_vals --> the y value of the center of the circle enclosing the fiducial
# @param time_vals --> tells how much time has elapsed at each frame
# @param isAScending --> denotes that the object being analyzed is going up. Since the
#   y coordinates in an image increase going down, the absolute value of the displacement 
#   needs to be taken. Otherwise, the displacement would be negative which is not what
#   is actually happening
def graph_calculus(y_vals: List, time_vals: List, isAscending: bool, title: str, fiducial_radius: int):
    # ~135 pixels = 2 inches (radius of real circle) ==> 67.5 pixels per real world inch
    ppi = fiducial_radius/2
    y_disp = []
    start_y = pixels_to_meters(y_vals[0], ppi)
    for y in y_vals:
        y = pixels_to_meters(y, ppi)
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
    plt.plot(time_vals, lbf_vals, color='black', label='Displacement (m)')

    r2 = r_squared(time_vals, y_disp, lbf_vals)
    print(f"R^2 = {r2}")
    #----------------------------------------

    #----------------------------------------
    # velocity function (1st derivative)
    velocity_vals = [((2 * a * x) + b) for x in time_vals]
    plt.plot(time_vals, velocity_vals, color='red', label='Velocity (m/s)')
    #----------------------------------------

    #----------------------------------------
    # acceleration function (2nd derivative)
    acc_vals = [ 2 * a for _ in time_vals ]
    plt.plot(time_vals, acc_vals, color='orange', label='Acceleration(m/s^2)')
    #----------------------------------------

    if not isAscending:
        # show graphs then exit
        # the force/work/power output during the descent is irrelevant
        plt.legend(loc='upper left')
        plt.show()
        return

    #----------------------------------------
    # force = mass * acceleration
    m = 95 / 2.2 # lbs --> kg
    acc = 2 * a # convert from in/s^2 --> m/s^2
    force = m * acc

    print(f"Force: {force} Newtons")
    #----------------------------------------

    #----------------------------------------
    # work = force * displacement
    max_y_index = lbf_vals.index(max(lbf_vals))
    min_y_index = lbf_vals.index(min(lbf_vals))
    # distance traveled from top to bottom of squat
    dist_traveled = lbf_vals[max_y_index] - lbf_vals[min_y_index]
    print(f"Distance Traveled: {dist_traveled} meters")

    work = force * dist_traveled

    print(f"Work: {work} Joules")
    #----------------------------------------

    #----------------------------------------
    # power = work / change in time
    ds = time_vals[len(time_vals) - 1] - time_vals[0] # delta s
    print(f"delta s: {ds} seconds")
    power = work / ds

    print(f"Power: {power} Watts")
    #----------------------------------------

    plt.legend(loc='upper left')
    plt.show()

# @param n = number of pixels (the value being converted to inches)
# @param ppn = pixels per inch: raidus of the drawn circle / radius of real circle in inches
# returns value in inches
def pixels_to_meters(n, ppi):
    return n / ppi * 0.0254

def check_barpath(x_vals: List, time_vals: List, fiducial_radius:int):
    # graph x displacement, find line of best fit at the zeroth degree, 
    # find r squared, if r squared is poor, their bar path is prolly shaky

    ppi = fiducial_radius/2
    x_disp = []
    start_x = pixels_to_meters(x_vals[0], ppi)
    for x in x_vals:
        x = pixels_to_meters(x, ppi)
        x_disp.append(abs(x - start_x))

    plt.scatter(time_vals, x_disp)

    y = np.polyfit(time_vals, x_disp, 0)[0]
    best_fit = [ y for _ in time_vals ] # make a straight line at the best fit

    plt.ylim(-2, 7) # make it easy to see if bar path is ok
    plt.plot(time_vals, best_fit, color='black')

    # CANNOT use r-squared because the line of best fit is the average of the data points
    # r2 will just be 0 because the error and distance from mean are the same
    # instead see classify it by how much it deviates
    #   ≤1 inch is elite, ≤3 inches is good, ≤5 needs work, anything more is dangerous

    plt.ylabel('X-value Displacement (in)')
    plt.xlabel('time (s)')
    plt.title("Horizontal Shift in Bar Path")
    plt.show()

# py_vals = predicted y values
def r_squared(x_vals: List, y_vals: List, py_vals: List) -> float:
    assert len(x_vals) == len(y_vals) == len(py_vals)
    
    sqrd_err = [] # predicted - real squared
    sqrd_y_from_mean = [] 
    mean = average(y_vals)
    print(f"mean: {mean}")

    for i, x in enumerate(x_vals):
        # print(f"Sqrd err: {(py_vals[i] - y_vals[i]) ** 2}")
        sqrd_err.append(
            (py_vals[i] - y_vals[i]) ** 2
        ) 
        # print(f" Sqrd y from mean: {(y_vals[i] - mean) ** 2}")
        sqrd_y_from_mean.append(
            (y_vals[i] - mean) ** 2
        )

    sum_sqrd_err = total(sqrd_err)
    print(f"sum_sqrd_err: {sum_sqrd_err}")
    sum_sqrd_y_from_mean = total(sqrd_y_from_mean)
    print(f"sum_sqrd_y_from_mean {sum_sqrd_y_from_mean}")

    # 1 - how much error in the line / how much deviation is there inherently 
    #   --> 1 - (how much variation is not explained by a change in x-value)
    # closer to 1 = less variation that is unexplained by a change in x
    return float(1 - (sum_sqrd_err / sum_sqrd_y_from_mean))

def average(arr: List) -> float:
    total = 0
    for elem in arr:
        total += elem
    return total / len(arr)

def total(arr: List) -> float:
    total = 0
    for elem in arr:
        total += elem
    return total