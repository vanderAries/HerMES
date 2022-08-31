import numpy as np
from structure.plotter import TrussPlot2D, TrussPlot3D


class Truss2D:
    def __init__(self, data):
        self._E = data.E
        self._A = data.A
        self.__coords = data.coords
        self.__elems = data.elems
        self.__supports = data.supports
        try:
            self.__forces = data.forces
        except:
            print('')
        else:
            self.ext = "Forces"

        try:
            self.__displacements = data.displacements
        except:
            print('')
        else:
            self.ext = "Displacements"

        self.axis = [(self.min_coords), (self.max_coords),
                     (self.min_coords), (self.max_coords)]
        self.L = None

    @property
    def n_num(self):
        """Total number od nodes"""
        n_num = np.shape(self.__coords)
        return n_num[0]

    @property
    def e_num(self):
        """Total number of elements"""
        e_num = np.shape(self.__elems)
        return e_num[0]

    @property
    def n_idx(self):
        """Nodes index"""
        n_index = np.zeros((self.n_num, 2))
        h = 0
        for k in range(0, self.n_num):
            n_index[k, :] = h+1, h+2
            h += 2
        return n_index.astype(int)

    @property
    def e_coords(self):
        """Elements coordinates"""
        elem_coords = np.zeros((self.e_num, 2, 2))
        for k in range(0, self.e_num):
            elem_coords[k] = np.array(
                [self.__coords[self.__elems[k, 0]], self.__coords[self.__elems[k, 1]]])
        return elem_coords

    @property
    def start_points(self):
        """Coordinates of start points of elements"""
        return self.e_coords[:, 0]

    @property
    def end_points(self):
        """Coordinates of end points of elements"""
        return self.e_coords[:, 1]

    @property
    def bars_center(self):
        """Coordinates of center points of elements"""
        return 0.5*(self.start_points + self.end_points)

    @property
    def max_coords(self):
        return np.amax(self.__coords)

    @property
    def min_coords(self):
        return np.amin(self.__coords)

    @property
    def length(self):
        """Length of the elements"""
        if self.L is None:
            self.L = np.linalg.norm(
                self.start_points - self.end_points, axis=1)
        return self.L

    def edof(self):
        """Degrees of freedom matrix"""
        edof = np.zeros((self.e_num, 2, 2))
        for k in range(0, self.e_num):
            edof[k] = np.array(
                [self.n_idx[self.__elems[k, 0]], self.n_idx[self.__elems[k, 1]]])
        return edof.reshape(self.e_num, 4)

    def ex(self):
        """Elements x coordinates"""
        ex = np.zeros((self.e_num, 2))
        for k in range(0, self.e_num):
            ex[k, 0] = self.start_points[k, 0]
            ex[k, 1] = self.end_points[k, 0]
        return ex

    def ey(self):
        """Elements y coordinates"""
        ey = np.zeros((self.e_num, 2))
        for k in range(0, self.e_num):
            ey[k, 0] = self.start_points[k, 1]
            ey[k, 1] = self.end_points[k, 1]
        return ey

    def supports(self):
        """Supports as blocked degrees of freedom"""
        sup = self.__supports.reshape(self.max_edof, 1)
        bc = []
        for i in range(0, self.max_edof):
            if sup[i] == 1:
                bc.append(i+1)
        return np.array(bc)

    def forces(self):
        """Forces applied to degrees of freedom"""
        return self.__forces.reshape(self.max_edof, 1)

    def displacements(self):
        """Displacements applied to degrees of freedom"""
        return self.__displacements.reshape(self.max_edof, 1)

    def build_model(self):
        """Function that builds model and show info about it"""
        self.edof = self.edof().astype(int)
        self.ex = self.ex()
        self.ey = self.ey()
        self.max_edof = int(np.amax(self.edof))
        self.supports = self.supports()
        if self.ext == "Forces":
            self.forces = self.forces()

        if self.ext == "Displacements":
            self.displacements = self.displacements()

        # Printing section
        print("Number of nodes: ", self.n_num)
        print("Number of elements: ", self.e_num)
        print("Total degrees of freedom: \n", self.max_edof)
        print("Degrees of freedom matrix: \n", self.edof)
        print("Supports: \n", self.supports)
        if self.ext == "Forces":
            print("Forces: \n", self.forces)

        if self.ext == "Displacements":
            print("Displacements: \n", self.displacements)

        # Edof
        elem_edof = []
        for i in range(0, self.e_num):
            elem_edof.append(
                [f"Element-{i+1}:-", str(self.edof[i]).replace(" ", "-")])
        self.elem_edof = str(np.array(elem_edof).reshape(self.e_num, 2))
        self.elem_edof = self.elem_edof.replace(",", "")
        self.elem_edof = self.elem_edof.replace("[", "")
        self.elem_edof = self.elem_edof.replace("]", "")
        self.elem_edof = self.elem_edof.replace("'", "")
        self.elem_edof = self.elem_edof.replace(" ", "")
        self.elem_edof = self.elem_edof.replace("-", " ")

        # Supports
        supports = []
        for j in range(0, self.n_num):
            if 1 in self.__supports[j]:
                supports.append(f"Node-{j+1}:")
            for g in range(0, 2):
                if g == 0:
                    if self.__supports[j][g] == 1:
                        supports[-1] += "-blocked-X"
                    else:
                        supports[-1] += "---------------"
                elif g == 1:
                    if self.__supports[j][g] == 1:
                        supports[-1] += "-blocked-Y"
        self.blocked_dir = str(np.array(supports).reshape(len(supports), 1))
        self.blocked_dir = self.blocked_dir.replace(",", "")
        self.blocked_dir = self.blocked_dir.replace("[", "")
        self.blocked_dir = self.blocked_dir.replace("]", "")
        self.blocked_dir = self.blocked_dir.replace("'", "")
        self.blocked_dir = self.blocked_dir.replace(" ", "")
        self.blocked_dir = self.blocked_dir.replace("-", " ")

        # Forces
        if self.ext == "Forces":
            forces = []
            for h in range(0, self.n_num):
                forces.append(
                    [f"Node_{h+1}:_", str(self.__forces[h]).replace(" ", "_")])
            self.show_external = str(np.array(forces).reshape(self.n_num, 2))
            self.show_external = self.show_external.replace(",", "")
            self.show_external = self.show_external.replace("[", "")
            self.show_external = self.show_external.replace("]", "")
            self.show_external = self.show_external.replace("'", "")
            self.show_external = self.show_external.replace(" ", "")
            self.show_external = self.show_external.replace("_", " ")

        if self.ext == "Displacements":
            displacements = []
            for h in range(0, self.n_num):
                displacements.append(
                    [f"Node_{h+1}:_", str(self.__displacements[h]).replace(" ", "_")])
            self.show_external = str(
                np.array(displacements).reshape(self.n_num, 2))
            self.show_external = self.show_external.replace(",", "")
            self.show_external = self.show_external.replace("[", "")
            self.show_external = self.show_external.replace("]", "")
            self.show_external = self.show_external.replace("'", "")
            self.show_external = self.show_external.replace(" ", "")
            self.show_external = self.show_external.replace("_", " ")

        E = []
        A = []
        for e in range(0, self.e_num):
            E.append([f"Element-{e+1}:-", self._E[e]])
            A.append([f"Element-{e+1}:-", self._A[e]])
        self.show_E = str(np.array(E).reshape(self.e_num, 2))
        self.show_A = str(np.array(A).reshape(self.e_num, 2))
        self.show_E = self.show_E.replace(",", "")
        self.show_E = self.show_E.replace("[", "")
        self.show_E = self.show_E.replace("]", "")
        self.show_E = self.show_E.replace("'", "")
        self.show_E = self.show_E.replace(" ", "")
        self.show_E = self.show_E.replace("-", " ")
        self.show_A = self.show_A.replace(",", "")
        self.show_A = self.show_A.replace("[", "")
        self.show_A = self.show_A.replace("]", "")
        self.show_A = self.show_A.replace("'", "")
        self.show_A = self.show_A.replace(" ", "")
        self.show_A = self.show_A.replace("-", " ")

    def print_model(self):
        """Function that print the model using Matplotlib"""
        TrussPlot2D(self.__coords, self.__elems, self.n_num, self.e_num, self.start_points,
                    self.end_points, self.bars_center, self.axis)


class Truss3D:
    def __init__(self, data):
        self._E = data.E
        self._A = data.A
        self.__coords = data.coords
        self.__elems = data.elems
        self.__supports = data.supports
        try:
            self.__forces = data.forces
        except:
            print('')
        else:
            self.ext = "Forces"

        try:
            self.__displacements = data.displacements
        except:
            print('')
        else:
            self.ext = "Displacements"
        self.axis = [(self.min_coords), (self.max_coords),
                     (self.min_coords), (self.max_coords)]
        self.L = None

    @property
    def n_num(self):
        """Total number od nodes"""
        n_num = np.shape(self.__coords)
        return n_num[0]

    @property
    def e_num(self):
        """Total number of elements"""
        e_num = np.shape(self.__elems)
        return e_num[0]

    @property
    def n_idx(self):
        """Degrees of freedom index in nodes"""
        n_index = np.zeros((self.n_num, 3))
        h = 0
        for k in range(0, self.n_num):
            n_index[k, :] = h+1, h+2, h+3
            h += 3
        return n_index.astype(int)

    @property
    def e_coords(self):
        """Elements coordinates"""
        elem_coords = np.zeros((self.e_num, 2, 3))
        for k in range(0, self.e_num):
            elem_coords[k] = np.array(
                [self.__coords[self.__elems[k, 0]], self.__coords[self.__elems[k, 1]]])
        return elem_coords

    @property
    def start_points(self):
        return self.e_coords[:, 0]

    @property
    def end_points(self):
        return self.e_coords[:, 1]

    @property
    def bars_center(self):
        return 0.5*(self.start_points + self.end_points)

    @property
    def max_coords(self):
        return np.amax(self.__coords)

    @property
    def min_coords(self):
        return np.amin(self.__coords)

    @property
    def length(self):
        if self.L is None:
            self.L = np.linalg.norm(
                self.start_points - self.end_points, axis=1)
        return self.L

    def edof(self):
        """Degrees of freedom matrix"""
        edof = np.zeros((self.e_num, 2, 3))
        for k in range(0, self.e_num):
            edof[k] = np.array(
                [self.n_idx[self.__elems[k, 0]], self.n_idx[self.__elems[k, 1]]])
        return edof.reshape(self.e_num, 6)

    def ex(self):
        """Elements x coordinates"""
        ex = np.zeros((self.e_num, 2))
        for k in range(0, self.e_num):
            ex[k, 0] = self.start_points[k, 0]
            ex[k, 1] = self.end_points[k, 0]
        return ex

    def ey(self):
        """Elements y coordinates"""
        ey = np.zeros((self.e_num, 2))
        for k in range(0, self.e_num):
            ey[k, 0] = self.start_points[k, 1]
            ey[k, 1] = self.end_points[k, 1]
        return ey

    def ez(self):
        """Elements y coordinates"""
        ez = np.zeros((self.e_num, 2))
        for k in range(0, self.e_num):
            ez[k, 0] = self.start_points[k, 2]
            ez[k, 1] = self.end_points[k, 2]
        return ez

    def supports(self):
        """Supports as blocked degrees of freedom"""
        sup = self.__supports.reshape(self.max_edof, 1)
        bc = []
        for i in range(0, self.max_edof):
            if sup[i] == 1:
                bc.append(i+1)
        return np.array(bc)

    def forces(self):
        """Forces applied to degrees of freedom"""
        return self.__forces.reshape(self.max_edof, 1)

    def displacements(self):
        """Displacements applied to degrees of freedom"""
        return self.__displacements.reshape(self.max_edof, 1)

    def build_model(self):
        """Function that builds model and show info about it"""
        self.edof = self.edof().astype(int)
        self.ex = self.ex()
        self.ey = self.ey()
        self.ez = self.ez()
        self.max_edof = int(np.amax(self.edof))
        self.supports = self.supports()
        if self.ext == "Forces":
            self.forces = self.forces()

        if self.ext == "Displacements":
            self.displacements = self.displacements()

        print("Number of nodes: ", self.n_num)
        print("Number of elements: ", self.e_num)
        print("Total degrees of freedom: \n", self.max_edof)
        print("Degrees of freedom matrix: \n", self.edof)
        print("Supports: \n", self.supports)
        if self.ext == "Forces":
            print("Forces: \n", self.forces)

        if self.ext == "Displacements":
            print("Displacements: \n", self.displacements)

        # DoF in elements
        elem_edof = []
        for i in range(0, self.e_num):
            elem_edof.append(
                [f"Element-{i+1}:-", str(self.edof[i]).replace(" ", "-")])
        self.elem_edof = str(np.array(elem_edof).reshape(self.e_num, 2))
        self.elem_edof = self.elem_edof.replace(",", "")
        self.elem_edof = self.elem_edof.replace("[", "")
        self.elem_edof = self.elem_edof.replace("]", "")
        self.elem_edof = self.elem_edof.replace("'", "")
        self.elem_edof = self.elem_edof.replace(" ", "")
        self.elem_edof = self.elem_edof.replace("-", " ")
        # Supports
        supports = []
        for j in range(0, self.n_num):
            supports.append(f"Node-{j+1}:")
            for g in range(0, 3):
                if g == 0:
                    if self.__supports[j][g] == 1:
                        supports[-1] += "-blocked-X"
                    else:
                        supports[-1] += "---------------"
                if g == 1:
                    if self.__supports[j][g] == 1:
                        supports[-1] += "-blocked-Y"
                    else:
                        supports[-1] += "---------------"
                elif g == 2:
                    if self.__supports[j][g] == 1:
                        supports[-1] += "-blocked-Z"
        self.blocked_dir = str(np.array(supports).reshape(len(supports), 1))
        self.blocked_dir = self.blocked_dir.replace(",", "")
        self.blocked_dir = self.blocked_dir.replace("[", "")
        self.blocked_dir = self.blocked_dir.replace("]", "")
        self.blocked_dir = self.blocked_dir.replace("'", "")
        self.blocked_dir = self.blocked_dir.replace(" ", "")
        self.blocked_dir = self.blocked_dir.replace("-", " ")

        # Forces
        if self.ext == "Forces":
            forces = []
            for h in range(0, self.n_num):
                forces.append(
                    [f"Node_{h+1}:_", str(self.__forces[h]).replace(" ", "_")])
            self.show_external = str(np.array(forces).reshape(self.n_num, 2))
            self.show_external = self.show_external.replace(",", "")
            self.show_external = self.show_external.replace("[", "")
            self.show_external = self.show_external.replace("]", "")
            self.show_external = self.show_external.replace("'", "")
            self.show_external = self.show_external.replace(" ", "")
            self.show_external = self.show_external.replace("_", " ")

        if self.ext == "Displacements":
            displacements = []
            for h in range(0, self.n_num):
                displacements.append(
                    [f"Node_{h+1}:_", str(self.__displacements[h]).replace(" ", "_")])
            self.show_external = str(
                np.array(displacements).reshape(self.n_num, 2))
            self.show_external = self.show_external.replace(",", "")
            self.show_external = self.show_external.replace("[", "")
            self.show_external = self.show_external.replace("]", "")
            self.show_external = self.show_external.replace("'", "")
            self.show_external = self.show_external.replace(" ", "")
            self.show_external = self.show_external.replace("_", " ")

        E = []
        A = []
        for e in range(0, self.e_num):
            E.append([f"Element-{e+1}:-", self._E[e]])
            A.append([f"Element-{e+1}:-", self._A[e]])
        self.show_E = str(np.array(E).reshape(self.e_num, 2))
        self.show_A = str(np.array(A).reshape(self.e_num, 2))
        self.show_E = self.show_E.replace(",", "")
        self.show_E = self.show_E.replace("[", "")
        self.show_E = self.show_E.replace("]", "")
        self.show_E = self.show_E.replace("'", "")
        self.show_E = self.show_E.replace(" ", "")
        self.show_E = self.show_E.replace("-", " ")
        self.show_A = self.show_A.replace(",", "")
        self.show_A = self.show_A.replace("[", "")
        self.show_A = self.show_A.replace("]", "")
        self.show_A = self.show_A.replace("'", "")
        self.show_A = self.show_A.replace(" ", "")
        self.show_A = self.show_A.replace("-", " ")

    def print_model(self):
        TrussPlot3D(self.__coords, self.__elems, self.n_num, self.e_num, self.start_points,
                    self.end_points, self.bars_center, self.axis)
