from turtle import color
import matplotlib.pyplot as plt
from typing import Any, List, Tuple, Dict
import numpy as np

def graph_calculus(y_vals: List, time_vals: List):
    y_disp = [y - y_vals[0] for y in y_vals]

    plt.xlabel("Time (seconds)")
    plt.title("Tracking a Barbell During a Squat")
    plt.scatter(time_vals, y_disp)

    # line of best fit: ax^2 + bx + c
    a, b, c = np.polyfit(time_vals, y_disp, 2)
    print(f"{a}x^2 + {b}x + {c}")

    lbf_vals = [ (a * (x**2) + (b * x) + c) for x in time_vals ]
    plt.plot(time_vals, lbf_vals, color='black', label='Displacement')

    # velocity function (1st derivative)
    velocity_vals = [((2 * a * x) + 4703) for x in time_vals]
    plt.plot(time_vals, velocity_vals, color='purple', label='Velocity')

    acc_vals = [ 2 * a for _ in time_vals ]
    plt.plot(time_vals, acc_vals, color='orange', label='Acceleration')

    plt.legend(loc='upper left')
    plt.show()