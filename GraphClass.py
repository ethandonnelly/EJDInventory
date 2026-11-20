from matplotlib.figure import Figure

class Graph:
    def __init__(self, x_values, y_values):
        # X axis values
        self.x_values = x_values
        # Y axis values
        self.y_values = y_values
        # Figure that holds graph
        self.figure = Figure(figsize=(6.5, 4), dpi=100)
        # Axis
        self.ax = self.figure.add_subplot(111)

    # Plotting the graph
    def plot(self):
        self.ax.plot(self.x_values, self.y_values)
        self.figure.tight_layout()
