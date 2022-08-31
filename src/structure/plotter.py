import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

class TrussPlot2D:
    def __init__(self, coords, elems, n_num, e_num, start_points, end_points, bars_center, axis):
        self.nodes_x = coords[0:n_num, 0]
        self.nodes_y = coords[0:n_num, 1]
        self.n_num = n_num
        self.e_num = e_num
        self.start_points = start_points
        self.end_points = end_points
        self.bars_center = bars_center
        self.n_index = []
        for i in range(0, n_num):
            self.n_index.append(i)

        self.e_index = []
        for j in range(0, e_num):
            self.e_index.append(j)

        self.nodes_plot()
        self.bars_plot()
        self.ax.set(xlim=(axis[0]-2, axis[1]+2), ylim=(axis[2]-2, axis[3]+2))
        plt.show()

    def nodes_plot(self):
        self.fig, self.ax = plt.subplots()
        self.ax.plot(self.nodes_x, self.nodes_y, 'ro', markersize=7)

        for x, y, idx in zip(self.nodes_x, self.nodes_y, self.n_index):
            self.ax.annotate('{}'.format(idx+1), xy=(x, y), xytext=(
                10, 3), textcoords='offset points', color='red')

    def bars_plot(self):
        for k in range(0, self.e_num):
            bars_x = self.start_points[k, 0], self.end_points[k, 0]
            bars_y = self.start_points[k, 1], self.end_points[k, 1]
            plt.plot(bars_x, bars_y, 'k')
        self.bars_numbers_plot()

    def bars_numbers_plot(self):
        for m in range(0, self.e_num):
            bars_cx = self.bars_center[m, 0]
            bars_cy = self.bars_center[m, 1]
            plt.plot(bars_cx, bars_cy, 'b,')
            self.ax.annotate('{}'.format(self.e_index[m]+1), xy=(
                bars_cx, bars_cy), color='blue', bbox=dict(boxstyle="round", fc="w"))

    # def supports_plot(self):
    #     for sup in self.supports:

    #         sup_x = self.nodes_x[sup]
    #         sup_y = self.nodes_y[sup]
    #         plt.plot(sup_x, sup_y, color='green', marker=6, markersize=11)


class TrussPlot3D:
    def __init__(self, coords, elems, n_num, e_num, start_points, end_points, bars_center, axis):
        self.nodes_x = coords[0:n_num, 0]
        self.nodes_y = coords[0:n_num, 1]
        self.nodes_z = coords[0:n_num, 2]
        self.n_num = n_num
        self.e_num = e_num
        self.start_points = start_points
        self.end_points = end_points
        self.bars_center = bars_center
        self.n_index = []
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

        for i in range(0, n_num):
            self.n_index.append(i)

        self.e_index = []
        for j in range(0, e_num):
            self.e_index.append(j)

        self.nodes_plot()
        self.bars_plot()
        #self.ax.set(xlim=(axis[0]-2, axis[1]+2), ylim=(axis[2]-2, axis[3]+2))
        plt.show()

    def nodes_plot(self):
        self.ax.plot(self.nodes_x, self.nodes_y,self.nodes_z, 'ro', markersize=7)

        for x, y, z, idx in zip(self.nodes_x, self.nodes_y,self.nodes_z, self.n_index):
            self.ax.text(x,y,z, idx+1,bbox=dict(facecolor='red', alpha=0.2,boxstyle='round,pad=0.5'))

    def bars_plot(self):
        for k in range(0, self.e_num):
            bars_x = self.start_points[k, 0], self.end_points[k, 0]
            bars_y = self.start_points[k, 1], self.end_points[k, 1]
            bars_z = self.start_points[k, 2], self.end_points[k, 2]
            self.ax.plot(bars_x, bars_y, bars_z, 'k')
        self.bars_numbers_plot()

    def bars_numbers_plot(self):
        for m in range(0, self.e_num):
            bars_cx = self.bars_center[m, 0]
            bars_cy = self.bars_center[m, 1]
            bars_cz = self.bars_center[m, 2]
            self.ax.plot(bars_cx, bars_cy, bars_cz,'b,')
            self.ax.text(bars_cx,bars_cy,bars_cz,self.e_index[m]+1,bbox=dict(facecolor='blue', alpha=0.3))

    # def supports_plot(self):
    #     for sup in self.supports:

    #         sup_x = self.nodes_x[sup]
    #         sup_y = self.nodes_y[sup]
    #         sup_z = self.nodes_z[sup]
    #         plt.plot(sup_x, sup_y, sup_z, color='green', marker=6, markersize=11)
