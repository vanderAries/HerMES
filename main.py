# This Python file uses the following encoding: utf-8
import sys
import os

from structure.build_model import Truss2D, Truss3D
from structure.solver import LinearSolver2D, LinearSolver3D, NonlinearForceSolver2D, NonlinearForceSolver3D, NonlinearDisSolver2D, NonlinearDisSolver3D
from data_exchange.export import GeometryExporter, ResultsExporter
from data_exchange.json_loader import Loader

from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QObject, Slot, Signal, QFileInfo


class Backend(QObject):
    def __init__(self):
        super().__init__()

    # Signals
    readPath = Signal(str)
    readModelInfo = Signal(str)
    readResults = Signal(str)
    is2D = Signal(bool)
    is3D = Signal(bool)
    isDataLoaded = Signal(str)
    isModelBuilt = Signal(str)
    isResultsReady = Signal(str)

    # Import File
    @Slot(str)
    def importFile(self, filePath):
        self.path = filePath[8:]
        self.name = QFileInfo(self.path).baseName()
        self.data = Loader(self.path)
        self.readPath.emit(self.path)
        self.isDataLoaded.emit("Data imported")

        if self.data.structure_type == "2D":
            self.is2D.emit(True)
        elif self.data.structure_type == "3D":
            self.is3D.emit(True)

    # Import File from Path

    @Slot(str)
    def importFileFromPath(self, filePath):
        self.path = filePath
        self.name = QFileInfo(self.path).baseName()
        self.data = Loader(self.path)
        self.isDataLoaded.emit("Data imported")

        if self.data.structure_type == "2D":
            self.is2D.emit(True)
        elif self.data.structure_type == "3D":
            self.is3D.emit(True)

    # Import Examples
    @Slot(None)
    def importVonMises(self):
        rel_path = "examples/von_mises_truss_data.json"
        self.path = os.path.abspath(rel_path)
        self.name = QFileInfo(self.path).baseName()
        self.data = Loader(self.path)
        self.readPath.emit(self.path)
        self.isDataLoaded.emit("Data imported")

        self.is2D.emit(True)

    @Slot(None)
    def importSpaceTruss(self):
        rel_path = "examples/space_truss_data.json"
        self.path = os.path.abspath(rel_path)
        self.name = QFileInfo(self.path).baseName()
        self.data = Loader(self.path)
        self.readPath.emit(self.path)
        self.isDataLoaded.emit("Data imported")

        self.is3D.emit(True)

    @Slot(None)
    def importDome(self):
        rel_path = "examples/dome_data.json"
        self.path = os.path.abspath(rel_path)
        self.name = QFileInfo(self.path).baseName()
        self.data = Loader(self.path)
        self.readPath.emit(self.path)
        self.isDataLoaded.emit("Data imported")

        self.is3D.emit(True)

    # 3D -> 2D

    @Slot(str)
    def exportTo2D(self, filePath):
        self.path = filePath[8:]
        self.geomExport = GeometryExporter(self.data, self.path)
        self.geomExport.to2D()

    # 2D -> 3D
    @Slot(str)
    def exportTo3D(self, filePath):
        self.path = filePath[8:]
        self.geomExport = GeometryExporter(self.data, self.path)
        self.geomExport.to3D()

    @Slot(str)
    def resultsExport(self, filePath):
        self.path = filePath[8:]
        self.resExport = ResultsExporter(self.data, self.solve, self.path)

    @Slot(None)
    def buildModel(self):
        if self.data.structure_type == "2D":
            self.truss = Truss2D(self.data)
            self.truss.build_model()

        elif self.data.structure_type == "3D":
            self.truss = Truss3D(self.data)
            self.truss.build_model()

        info = f"Number of nodes: {self.truss.n_num}\n\nNumber of elements: {self.truss.e_num}\n\nTotal degrees of freedom: {self.truss.max_edof}\n\nYoung module in elements [N/m^2]:\n{self.truss.show_E}\n\nSection area in elements [m^2]:\n{self.truss.show_A}\n\nDegrees of freedom in elements:\n{self.truss.elem_edof}\n\nSupports: \n{self.truss.blocked_dir}\n\n"

        if self.truss.ext == "Forces":
            info += f"Forces [N]:\n{self.truss.show_external}"

        elif self.truss.ext == "Displacements":
            info += f"Displacements [m]:\n{self.truss.show_external}"

        self.readModelInfo.emit(info)
        self.isModelBuilt.emit("Model built")

    # Print model in 2D or 3D
    @Slot(None)
    def printModel(self):
        self.truss.print_model()

    # Solvers
    @Slot(None)
    def solveModelLinear(self):
        if self.data.structure_type == "2D" and self.data.example == None:
            self.solve = LinearSolver2D(self.truss.edof, self.truss.max_edof,
                                        self.truss.ex, self.truss.ey, self.data.ep, self.truss.e_num, self.truss.supports, self.truss.forces)

        elif self.data.structure_type == "3D" and self.data.example == None or self.data.example == "Space Truss":
            self.solve = LinearSolver3D(self.truss.edof, self.truss.max_edof,
                                        self.truss.ex, self.truss.ey, self.truss.ez, self.data.ep, self.truss.e_num, self.truss.supports, self.truss.forces)

        elif self.data.example == "von Mises Truss":
            from structure.examples_solver import LinearVonMises
            self.solve = LinearVonMises(self.truss.edof, self.truss.max_edof,
                                        self.truss.ex, self.truss.ey, self.data.ep, self.truss.e_num, self.truss.supports, self.truss.forces, self.data.H)

        elif self.data.example == "Dome":
            from structure.examples_solver import LinearDome
            self.solve = LinearDome(self.truss.edof, self.truss.max_edof,
                                    self.truss.ex, self.truss.ey, self.truss.ez, self.data.ep, self.truss.e_num, self.truss.supports, self.truss.forces)

        if self.data.example == None or self.data.example == "Space Truss":
            self.readResults.emit(f"Displacements:\n{self.solve.show_q}")

        elif self.data.example == "von Mises Truss":
            self.readResults.emit(
                f"Displacements:\n{self.solve.q}\nEta:\n{self.solve.eta}")

        elif self.data.example == "Dome":
            self.readResults.emit(
                f"Displacements:\n{self.solve.q}")

        self.isResultsReady.emit("Linear results ready")

    @Slot(int, int, str, str, str)
    def solveModelForceNonlinear(self, incermentsNum, maxIter, resNorm, disNorm, dofTrack):
        if self.data.structure_type == "2D" and self.data.example == None:
            self.solve = NonlinearForceSolver2D(self.truss.edof, self.truss.max_edof,
                                                self.truss.ex, self.truss.ey, self.data.ep, self.truss.e_num, self.truss.supports, self.truss.forces, incermentsNum, maxIter, float(resNorm), float(disNorm), int(dofTrack)-1)

        elif self.data.structure_type == "3D" and self.data.example == None or self.data.example == "Space Truss":
            self.solve = NonlinearForceSolver3D(self.truss.edof, self.truss.max_edof,
                                                self.truss.ex, self.truss.ey, self.truss.ez, self.data.ep, self.truss.e_num, self.truss.supports, self.truss.forces, incermentsNum, maxIter, float(resNorm), float(disNorm), int(dofTrack)-1)

        elif self.data.example == "von Mises Truss":
            from structure.examples_solver import NonlinearForceVonMises
            self.solve = NonlinearForceVonMises(self.truss.edof, self.truss.max_edof,
                                                self.truss.ex, self.truss.ey, self.data.ep, self.truss.e_num, self.truss.supports, self.truss.forces, self.data.H)

        elif self.data.example == "Dome":
            from structure.examples_solver import NonlinearForceDome
            self.solve = NonlinearForceDome(self.truss.edof, self.truss.max_edof,
                                            self.truss.ex, self.truss.ey, self.truss.ez, self.data.ep, self.truss.e_num, self.truss.supports, self.truss.forces)

        if self.data.example == None or self.data.example == "Space Truss":
            self.readResults.emit(f"Displacements:\n{self.solve.show_q}")

        elif self.data.example == "von Mises Truss":
            self.readResults.emit(
                f"Step {self.solve.m}\nForce increment[{self.solve.deltaQ[self.solve.m]}]\nDisplacements\n{self.solve.q}\neta {self.solve.eta} \niter [{self.solve.itr}]")

        elif self.data.example == "Dome":
            self.readResults.emit(
                f"Step {self.solve.m}\nForce increment[{self.solve.deltaQ[self.solve.m]}]\nDisplacements\n{self.solve.q}\niter [{self.solve.itr}]")

        self.isResultsReady.emit("Nonlinear results ready")

    @Slot(str, str, int, str, str, str)
    def solveModelDisNonlinear(self, incermentsValue, maxIter, resNorm, disNorm, dofTrack, dofControl):
        if self.data.structure_type == "2D" and self.data.example == None:
            self.solve = NonlinearDisSolver2D(self.truss.edof, self.truss.max_edof,
                                              self.truss.ex, self.truss.ey, self.data.ep, self.truss.e_num, self.truss.supports, self.truss.forces, float(incermentsValue), maxIter, float(resNorm), float(disNorm), int(dofTrack)-1, int(dofControl)-1)

        elif self.data.structure_type == "3D" and self.data.example == None or self.data.example == "Space Truss":
            self.solve = NonlinearDisSolver3D(self.truss.edof, self.truss.max_edof,
                                              self.truss.ex, self.truss.ey, self.truss.ez, self.data.ep, self.truss.e_num, self.truss.supports, self.truss.forces, float(incermentsValue), maxIter, float(resNorm), float(disNorm), int(dofTrack)-1, int(dofControl)-1)

        elif self.data.example == "von Mises Truss":
            from structure.examples_solver import NonlinearDisVonMises
            self.solve = NonlinearDisVonMises(self.truss.edof, self.truss.max_edof,
                                              self.truss.ex, self.truss.ey, self.data.ep, self.truss.e_num, self.truss.supports, self.truss.forces, self.data.H)

        elif self.data.example == "Dome":
            from structure.examples_solver import NonlinearDisDome
            self.solve = NonlinearDisDome(self.truss.edof, self.truss.max_edof,
                                          self.truss.ex, self.truss.ey, self.truss.ez, self.data.ep, self.truss.e_num, self.truss.supports, self.truss.forces)

        if self.data.example == None or self.data.example == "Space Truss":
            self.readResults.emit(f"Displacements:\n{self.solve.show_q}")

        elif self.data.example == "von Mises Truss":
            self.readResults.emit(
                f"Step {self.solve.m}\nDisplacements\n{self.solve.q}\neta {self.solve.eta} \niter [{self.solve.itr}]")

        elif self.data.example == "Dome":
            self.readResults.emit(
                f"Step {self.solve.m}\nDisplacements\n{self.solve.q}\niter [{self.solve.itr}]")

        self.isResultsReady.emit("Nonlinear results ready")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOrganizationName("Stellaris Incorporated")
    app.setOrganizationDomain("stellarisinc.com")
    app.setApplicationName("HerMES")
    engine = QQmlApplicationEngine()

    # Get Context
    backend = Backend()
    engine.rootContext().setContextProperty("backend", backend)

    # Load QML File
    engine.load(os.path.join(os.path.dirname(__file__), "qml/main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
