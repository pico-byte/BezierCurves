import math

import numpy as np
import matplotlib.pyplot as plt
from math import comb


# Initial control points
points = [
    [0, 20],
    [0, 0],
    [0,5],
    [0,2]
]

alpha = np.pi * 0.1

for p in points:
    p[0] = p[0] + math.tan(alpha) * p[1]


def bezier_curve(points, num=500):
    n = len(points) - 1
    t_values = np.linspace(0, 1, num)

    curve = []

    for t in t_values:
        x = 0
        y = 0

        for i, (px, py) in enumerate(points):
            basis = comb(n, i) * (1 - t)**(n - i) * t**i
            x += basis * px
            y += basis * py

        curve.append((x, y))

    return np.array(curve)


class BezierEditor:
    def __init__(self, points):
        self.points = points
        self.selected = None

        self.fig, self.ax = plt.subplots()

        self.control_line, = self.ax.plot([], [], 'o--', picker=5)
        self.curve_line, = self.ax.plot([], [], lw=2)

        self.update_plot()

        self.fig.canvas.mpl_connect(
            'button_press_event',
            self.on_press
        )
        self.fig.canvas.mpl_connect(
            'button_release_event',
            self.on_release
        )
        self.fig.canvas.mpl_connect(
            'motion_notify_event',
            self.on_motion
        )

 #       img = plt.imread("sigma.jpg")
#
        #self.ax.imshow(
          #  img,
         #   extent=[0, 100, 0, 100],  # coordinate system
        #    origin="lower",
       #
      #  )

        plt.show()

    def update_plot(self):
        curve = bezier_curve(self.points)

        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]

        self.control_line.set_data(xs, ys)
        self.curve_line.set_data(curve[:, 0], curve[:, 1])

        self.ax.relim()
        #self.ax.autoscale_view()

        self.fig.canvas.draw_idle()

    def on_press(self, event):
        if event.inaxes != self.ax:
            return

        for i, (x, y) in enumerate(self.points):
            distance = np.hypot(event.xdata - x,
                                event.ydata - y)

            xmin, xmax = self.ax.get_xlim()
            if distance < 0.2 * (xmax - xmin):
                self.selected = i
                break

    def on_release(self, event):
        self.selected = None

    def on_motion(self, event):
        if self.selected is None:
            return

        if event.inaxes != self.ax:
            return

        self.points[self.selected][0] = event.xdata
        self.points[self.selected][1] = event.ydata

        self.update_plot()


BezierEditor(points)
