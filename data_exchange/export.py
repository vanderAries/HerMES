import numpy as np
import json


class GeometryExporter(object):
    def __init__(self, data, path):
        self.data = data
        self.path = path

    def to2D(self):
        if self.data.structure_type == "2D":
            print("File is already 2D")
        else:
            self.coords = np.delete(self.data.coords, 2, 1)
            self.supports = np.delete(self.data.supports, 2, 1)
            self.forces = np.delete(self.data.forces, 2, 1)
            self.structure_type = "2D"

            self.coords = self.coords.tolist()
            self.elems = self.data.elems.tolist()
            self.supports = self.supports.tolist()
            self.forces = self.forces.tolist()

            data = {}
            data["example"] = self.data.example
            data["structure_type"] = self.structure_type
            data["E"] = self.data.E
            data["A"] = self.data.A
            data["coords"] = self.coords
            data["elems"] = self.elems
            data["supports"] = self.supports
            data["forces"] = self.forces

            file = open(self.path, "w")
            json.dump(data, file, indent=4)
            file.close()

    def to3D(self):
        if self.data.structure_type == "3D":
            print("File is already 3D")
        else:
            self.coords = np.append(self.data.coords, np.zeros(
                (self.data.coords.shape[0], 1)), axis=1)
            self.supports = np.append(self.data.supports, np.ones(
                (self.data.supports.shape[0], 1)), axis=1)
            self.forces = np.append(self.data.forces, np.zeros(
                (self.data.forces.shape[0], 1)), axis=1)
            self.structure_type = "3D"

            self.coords = self.coords.tolist()
            self.elems = self.data.elems.tolist()
            self.supports = self.supports.tolist()
            self.forces = self.forces.tolist()

            data = {}
            data["example"] = self.data.example
            data["structure_type"] = self.structure_type
            data["E"] = self.data.E
            data["A"] = self.data.A
            data["coords"] = self.coords
            data["elems"] = self.elems
            data["supports"] = self.supports
            data["forces"] = self.forces

            file = open(self.path, "w")
            json.dump(data, file, indent=4)
            file.close()


class ResultsExporter(object):
    def __init__(self, data, results, path):
        self.data = data
        self.path = path
        self.results = results

        self.coords = self.data.coords.tolist()
        self.elems = self.data.elems.tolist()
        self.supports = self.data.supports.tolist()
        self.forces = self.data.forces.tolist()

        self.nodal_R = self.results.nodal_R.tolist()
        self.nodal_q = self.results.nodal_q.tolist()
        self.nodal_Ne = self.results.nodal_Ne.tolist()
        self.element_Ne = self.results.Ne.tolist()

        self.dis_coords = self.data.coords + self.results.nodal_q
        self.dis_coords = self.dis_coords.tolist()

        data = {}
        data["E"] = self.data.E
        data["A"] = self.data.A
        data["coords"] = self.coords
        data["elems"] = self.elems
        data["supports"] = self.supports
        data["forces"] = self.forces

        data["nodal_R"] = self.nodal_R
        data["nodal_q"] = self.nodal_q
        data["nodal_Ne"] = self.nodal_Ne
        data["element_Ne"] = self.element_Ne
        data["coords_dis"] = self.dis_coords

        file = open(self.path, "w")
        json.dump(data, file, indent=4)
        file.close()
