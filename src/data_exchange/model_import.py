import json
import numpy as np


class ModelImport(object):
    def __init__(self, path):
        self.path = path
        json_file = open(self.path)
        json_data = json.load(json_file)
        json_file.close()

        self.example = json_data["example"]
        self.structure_type = json_data["structure_type"]

        self.E = json_data["E"]
        self.A = json_data["A"]
        self.ep = np.array([self.E, self.A])

        if self.example == "von Mises Truss":
            self.L = json_data["L"]
            self.H = json_data["H"]
            self.L0 = json_data["L0"]
            self.sb0 = json_data["sb0"]
            self.P = json_data["P"]

        self.coords = np.array(json_data["coords"])
        self.elems = np.array(json_data["elems"])
        self.supports = np.array(json_data["supports"])

        try:
            self.forces = np.array(json_data["forces"])
        except:
            print('')

        try:
            self.displacements = np.array(json_data["displacements"])
        except:
            print('')


