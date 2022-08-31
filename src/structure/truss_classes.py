import numpy as np


class Element_parameters2D:
    """Parent class that contains all element parameters needed to compute stiffness and forces"""

    def __init__(self, edof, e_num, ex_global, ey_global, ep, qe=None, Ne=None):
        """
        :param list ex: element x coordinates [x1, x2]
        :param list ey: element y coordinates [y1, y2]
        :param list ep: [E, A]: E - Young's modulus, A - Cross section area
        :param list qe: element global displacements [q1, q2, q3, q4]
        :param list Ne: element normal force [Ne]
        """
        self._edof = edof
        self._max_edof = np.amax(edof)
        self._e_num = e_num
        self._ex = ex_global
        self._ey = ey_global
        self._EA = ep[0]*ep[1]
        self._qe = qe
        self._Ne = Ne

    def length(self, ex, ey):
        """Element length"""

        b = np.mat([
            [ex[1]-ex[0]],
            [ey[1]-ey[0]]
        ])
        L = np.sqrt(b.T*b)
        return L.item()

    def transfromation_matrix(self, ex, ey):
        """Transformation matrix G that contains the direction cosines"""
        b = np.mat([
            [ex[1]-ex[0]],
            [ey[1]-ey[0]]
        ])
        L = np.sqrt(b.T*b).item()
        n = np.asarray(b.T/L).reshape(2,)
        G = np.mat([
            [n[0],  n[1],   0.,   0.],
            [-n[1], n[0],   0.,   0.],
            [0.,    0.,   n[0], n[1]],
            [0.,    0.,  -n[1], n[0]]
        ])
        return G


class Stiffness2D(Element_parameters2D):
    """Class that contains stifness matrices for each element"""

    def __init__(self, edof, e_num, ex_global, ey_global, ep, qe=None, Ne=None):
        """
        :param list ex: element x coordinates [x1, x2]
        :param list ey: element y coordinates [y1, y2]
        :param list ep: [E, A]: E - Young's modulus, A - Cross section area
        :param list qe: element global displacements [q1, q2, q3, q4]
        :param list Ne: element normal force [Ne]
        """
        Element_parameters2D.__init__(
            self, edof, e_num, ex_global, ey_global, ep, qe, Ne)

    def bar2d_ke_0(self, ex, ey, EA):
        """
        Compute the element stiffness matrix for two dimensional bar element in global coord. system. (10-36)
        Return mat Ke_0: stiffness matrix, [4 x 4]
        """
        L = self.length(ex, ey)
        G = self.transfromation_matrix(ex, ey)
        Ke_0 = (EA/L)*np.mat([[1., 0., -1., 0.],
                              [0., 0.,  0., 0.],
                              [-1., 0., 1., 0.],
                              [0.,  0.,  0., 0]
                              ])

        return G.T*Ke_0*G

    def bar2d_ke_u(self, ex, ey, EA, qe):
        """
        Compute the element displacement matrix for two dimensional bar element in global coord. system. (10-36)
        Return mat Ke_u: displacement matrix [4 x 4]
        """
        L = self.length(ex, ey)
        G = self.transfromation_matrix(ex, ey)
        qeloc = np.matmul(G, qe.reshape(4, 1))

        du = qeloc[2, 0] - qeloc[0, 0]
        dv = qeloc[3, 0] - qeloc[1, 0]

        Ke_1 = (3/2)*(EA/L**2)*np.mat([[2*du, dv, -2*du, -dv],
                                       [dv,    0,  -dv,    0],
                                       [-2*du, -dv, 2*du, dv],
                                       [-dv,   0,   dv,    0]
                                       ])

        Ke_2 = (3/2)*(EA/L**3)*np.mat([[du**2, du*dv, -du**2, -du*dv],
                                       [du*dv, dv**2, -du*dv, -dv**2],
                                       [-du**2, -du*dv, du**2, du*dv],
                                       [-du*dv, -dv**2, du*dv, dv**2]
                                       ])

        Ke_u = (2/3)*Ke_1 + (2/3)*Ke_2

        return G.T*Ke_u*G

    def bar2d_ke_sigma(self, ex, ey, Ne):
        """
        Compute element stress matrix for two dimensional bar element in global coord. system. (10-36)
        Return mat Ke_sigma: stress matrix [4 x 4]
        """
        L = self.length(ex, ey)
        G = self.transfromation_matrix(ex, ey)
        Ke_sigma = (Ne.item()/L)*np.mat([
            [1, 0, -1, 0],
            [0, 1, 0, -1],
            [-1, 0, 1, 0],
            [0, -1, 0, 1]])

        return G.T*Ke_sigma*G

    def assem_K(self, edof, K, Ke):
        """
        Assemble element matrices Ke into the global
        stiffness matrix K
        according to the topology matrix edof.

        Parameters:

            edof        dof topology array
            K           the global stiffness matrix
            Ke          element stiffness matrix

        Output parameters:

            K           the new global stiffness matrix
        """

        if edof.ndim == 1:
            idx = edof-1
            K[np.ix_(idx, idx)] = K[np.ix_(idx, idx)] + Ke

        else:
            for row in edof:
                idx = row-1
                K[np.ix_(idx, idx)] = K[np.ix_(idx, idx)] + Ke

        return K

    def compute_ke_0(self):
        """
        Compute global stiffnes matrix for two dimensional bar elements.
        Return mat K_0: tangent matrix [4 x 4]
        """
        Ke_0 = np.zeros((self._e_num, 4, 4))

        K_0 = np.zeros((self._max_edof, self._max_edof))

        for i in range(0, self._e_num):
            Ke_0[i] = self.bar2d_ke_0(self._ex[i], self._ey[i], self._EA[i])
            K_0 = self.assem_K(self._edof[i, :], K_0, Ke_0[i])

        return K_0

    def compute_ke_T(self):
        """
        Compute global tangent matrix for two dimensional bar elements.
        Return mat K_T: tangent matrix [4 x 4]
        """
        Ke_0 = np.zeros((self._e_num, 4, 4))
        Ke_u = np.zeros((self._e_num, 4, 4))
        Ke_sigma = np.zeros((self._e_num, 4, 4))

        K_T = np.zeros((self._max_edof, self._max_edof))

        for i in range(0, self._e_num):
            Ke_0[i] = self.bar2d_ke_0(self._ex[i], self._ey[i], self._EA[i])
            Ke_u[i] = self.bar2d_ke_u(
                self._ex[i], self._ey[i], self._EA[i], self._qe[i])
            Ke_sigma[i] = self.bar2d_ke_sigma(
                self._ex[i], self._ey[i], self._Ne[i])

        Ke_T = Ke_0+Ke_u+Ke_sigma

        for j in range(0, self._e_num):
            K_T = self.assem_K(self._edof[j, :], K_T, Ke_T[j])

        return K_T


class Forces2D(Element_parameters2D):
    """Class that computes internal forces in elements"""

    def __init__(self, edof, e_num, ex_global, ey_global, ep, qe=None):
        """
        :param list ex: element x coordinates [x1, x2]
        :param list ey: element y coordinates [y1, y2]
        :param list ep: [E, A]: E - Young's modulus, A - Cross section area
        :param list qe: element global displacements [q1, q2, q3, q4]
        :param list Ne: element normal force [Ne]
        """
        Element_parameters2D.__init__(
            self, edof, e_num, ex_global, ey_global, ep, qe)

    def bar2d_Ne(self, ex, ey, EA, qe):
        """
        Compute the normal force for two dimensional bar element. (10-33)

        :param list ex: element x coordinates [x1, x2]
        :param list ey: element y coordinates [y1, y2]
        :param list ep: [E, A]: E - Young's modulus, A - Cross section area
        :return normal force
        """
        L = self.length(ex, ey)
        G = self.transfromation_matrix(ex, ey)
        qeloc = np.matmul(G, qe.reshape(4, 1))

        B0 = np.array([-1, 0, 1, 0])/L

        M = np.array([[1, 0, -1, 0],
                      [0, 1, 0, -1],
                      [-1, 0, 1, 0],
                      [0, -1, 0, 1]
                      ])/L**2

        B1 = np.matmul(qeloc.T, M)
        B = B0+0.5*B1

        N = EA*np.matmul(B, qeloc)
        return N

    def bar2d_Ne_lin(self, ex, ey, EA, qe):
        """
        Compute the normal force for two dimensional bar element. (10-33)

        :param list ex: element x coordinates [x1, x2]
        :param list ey: element y coordinates [y1, y2]
        :param list ep: [E, A]: E - Young's modulus, A - Cross section area
        :return normal force
        """
        L = self.length(ex, ey)
        G = self.transfromation_matrix(ex, ey)
        qeloc = np.matmul(G, qe.reshape(4, 1))

        B = np.array([-1, 0, 1, 0])/L

        N = EA*np.matmul(B, qeloc)
        return N

    def bar2d_Fe(self, ex, ey, qe, Ne):
        """
        Compute the Fe matrix for two dimensional bar element. (10-43c)

        :param list ex: element x coordinates [x1, x2]
        :param list ey: element y coordinates [y1, y2]
        :param list qe: element global displacements [q1, q2, q3, q4]
        :param list Ne: element normal force [Ne]
        :return mat Fe: [4 x 1]
        """
        L = self.length(ex, ey)
        G = self.transfromation_matrix(ex, ey)
        qeloc = np.matmul(G, qe.reshape(4, 1))

        du = qeloc[2, 0] - qeloc[0, 0]
        dv = qeloc[3, 0] - qeloc[1, 0]

        Fe = np.array([
            [-1-du/L],
            [-dv/L],
            [1+du/L],
            [dv/L]
        ])

        return np.matmul(G.T, Ne.item()*Fe)

    def assem_F(self, edof, F, Fe):
        """
        Assemble element matrices and fe into the global force vector F
        according to the topology matrix edof.

        Parameters:
            edof        dof topology array
            F           the global force vector
            Fe          element force vector

        Output parameters:
            F           the new global force vector

        """

        if edof.ndim == 1:
            idx = edof-1

            F[np.ix_(idx)] = F[np.ix_(idx)] + Fe
        else:
            for row in edof:
                idx = row-1
                F[np.ix_(idx)] = F[np.ix_(idx)] + Fe

        return F

    def compute_Ne(self):
        """
        Compute global normal force for two dimensional bar elements.
        Return mat K_0: tangent matrix [4 x 4]
        """
        Ne = np.zeros((self._e_num, 1))

        for i in range(0, self._e_num):
            Ne[i] = self.bar2d_Ne(self._ex[i], self._ey[i],
                                  self._EA[i], self._qe[i])
        self.Ne = Ne

        return Ne

    def compute_Ne_lin(self):
        """
        Compute global normal force for two dimensional bar elements.
        Return mat K_0: tangent matrix [4 x 4]
        """
        Ne = np.zeros((self._e_num, 1))
        print("debug", self._ex, self._ey, self._EA, self._qe)
        for i in range(0, self._e_num):
            Ne[i] = self.bar2d_Ne_lin(
                self._ex[i], self._ey[i], self._EA[i], self._qe[i])
        self.Ne = Ne

        return Ne

    def compute_F(self):
        """
        Compute global internal forces for two dimensional bar elements.
        Return mat K_0: tangent matrix [4 x 4]
        """
        Fe = np.zeros((self._e_num, 4, 1))
        F = np.zeros((self._max_edof, 1))

        for i in range(0, self._e_num):
            Fe[i] = self.bar2d_Fe(
                self._ex[i], self._ey[i], self._qe[i], self.Ne[i])
            F = self.assem_F(self._edof[i, :], F, Fe[i])

        return F

    def compute_Res(self, Q, R):

        return Q+R-self.compute_F()


class Element_parameters3D:
    """Parent class that contains all element parameters needed to compute stiffness and forces"""

    def __init__(self, edof, e_num, ex_global, ey_global, ez_global, ep, qe=None, Ne=None):
        """
        :param list ex: element x coordinates [x1, x2]
        :param list ey: element y coordinates [y1, y2]
        :param list ep: [E, A]: E - Young's modulus, A - Cross section area
        :param list qe: element global displacements [q1, q2, q3, q4]
        :param list Ne: element normal force [Ne]
        """
        self._edof = edof
        self._max_edof = np.amax(edof)
        self._e_num = e_num
        self._ex = ex_global
        self._ey = ey_global
        self._ez = ez_global
        self._EA = ep[0]*ep[1]
        self._qe = qe
        self._Ne = Ne

    def length(self, ex, ey, ez):
        """Element length"""

        b = np.mat([
            [ex[1]-ex[0]],
            [ey[1]-ey[0]],
            [ez[1]-ez[0]]
        ])
        L = np.sqrt(b.T*b)
        return L.item()

    def transfromation_matrix(self, ex, ey, ez):
        """Transformation matrix G that contains the direction cosines"""
        b = np.mat([
            [ex[1]-ex[0]],
            [ey[1]-ey[0]],
            [ez[1]-ez[0]]
        ])
        L = np.sqrt(b.T*b).item()
        n = np.asarray(b.T/L).reshape(3,)
        G = np.mat([
            [n[0],  n[1], n[2],   0.,   0.,   0.],
            [-n[1], n[0], n[2],   0.,   0.,   0.],
            [n[2],  n[1], n[0],   0.,   0.,   0.],
            [0.,     0.,    0.,   n[0],  n[1], n[2]],
            [0.,     0.,    0.,  -n[1],  n[0], n[2]],
            [0.,     0.,    0.,   n[2],  n[1], n[0]]
        ])
        return G


class Stiffness3D(Element_parameters3D):
    """Class that contains stifness matrices for each element"""

    def __init__(self, edof, e_num, ex_global, ey_global, ez_global, ep, qe=None, Ne=None):
        """
        :param list ex: element x coordinates [x1, x2]
        :param list ey: element y coordinates [y1, y2]
        :param list ep: [E, A]: E - Young's modulus, A - Cross section area
        :param list qe: element global displacements [q1, q2, q3, q4]
        :param list Ne: element normal force [Ne]
        """
        Element_parameters3D.__init__(self, edof, e_num, ex_global, ey_global, ez_global, ep, qe, Ne)

    def bar3d_ke_0(self, ex, ey, ez, EA):
        """
        Compute the element stiffness matrix for two dimensional bar element in global coord. system. (10-36)
        Return mat Ke_0: stiffness matrix, [4 x 4]
        """
        L = self.length(ex, ey, ez)
        G = self.transfromation_matrix(ex, ey, ez)
        Ke_0 = (EA/L)*np.mat([[1., 0., 0., -1., 0., 0.],
                              [0., 0., 0.,  0., 0., 0.],
                              [0., 0., 0.,  0., 0., 0.],
                              [-1., 0., 0., 1., 0., 0.],
                              [0.,  0., 0.,  0., 0., 0.],
                              [0., 0., 0.,  0., 0., 0.]
                              ])

        return G.T*Ke_0*G

    def bar3d_ke_u(self, ex, ey, ez, EA, qe):
        """
        Compute the element displacement matrix for two dimensional bar element in global coord. system. (10-36)
        Return mat Ke_u: displacement matrix [4 x 4]
        """
        L = self.length(ex, ey, ez)
        G = self.transfromation_matrix(ex, ey, ez)
        qeloc = np.matmul(G, qe.reshape(6, 1))

        du = qeloc[3, 0] - qeloc[0, 0]
        dv = qeloc[4, 0] - qeloc[1, 0]
        dw = qeloc[5, 0] - qeloc[2, 0]

        Ke_1 = (3/2)*(EA/L**2)*np.mat([[2*du, dv, dw, -2*du, -dv, -dw],
                                       [dv,    0,  0,  -dv,    0,  0],
                                       [dw,    0,  0,  -dw,    0,  0],
                                       [-2*du, -dv, -dw, 2*du, dv, dw],
                                       [-dv,   0,  0,   dv,    0,  0],
                                       [-dw,   0,  0,   dw,    0,  0]
                                       ])

        Ke_2 = (3/2)*(EA/L**3)*np.mat([[du**2, du*dv, du*dw, -du**2, -du*dv, -du*dw],
                                       [du*dv, dv**2, dv*dw, -du*dv, -dv**2, -dv*dw],
                                       [dw*du, dw*dv, dw*2,  -dw*du, -dw*dv,  -dw*2],
                                       [-du**2, -du*dv, -du*dw, du**2, du*dv, du*dw],
                                       [-du*dv, -dv**2, -dv*dw, du*dv, dv**2, dv*dw],
                                       [-dw*du, -dw*dv, -dw*2,  dw*du, dw*dv,  dw*2]
                                       ])

        Ke_u = (2/3)*Ke_1 + (2/3)*Ke_2

        return G.T*Ke_u*G

    def bar3d_ke_sigma(self, ex, ey, ez, Ne):
        """
        Compute element stress matrix for two dimensional bar element in global coord. system. (10-36)
        Return mat Ke_sigma: stress matrix [4 x 4]
        """
        L = self.length(ex, ey, ez)
        G = self.transfromation_matrix(ex, ey, ez)
        Ke_sigma = (Ne.item()/L)*np.mat([
            [1, 0, 0, -1, 0, 0],
            [0, 1, 0, 0, -1, 0],
            [0, 0, 1, 0, 0, -1],
            [-1, 0, 0, 1, 0, 0],
            [0, -1, 0, 0, 1, 0],
            [0, 0, -1, 0, 0, 1]
        ])

        return G.T*Ke_sigma*G

    def assem_K(self, edof, K, Ke):
        """
        Assemble element matrices Ke into the global
        stiffness matrix K
        according to the topology matrix edof.

        Parameters:

            edof        dof topology array
            K           the global stiffness matrix
            Ke          element stiffness matrix

        Output parameters:

            K           the new global stiffness matrix
        """

        if edof.ndim == 1:
            idx = edof-1
            K[np.ix_(idx, idx)] = K[np.ix_(idx, idx)] + Ke

        else:
            for row in edof:
                idx = row-1
                K[np.ix_(idx, idx)] = K[np.ix_(idx, idx)] + Ke

        return K

    def compute_ke_0(self):
        """
        Compute global stiffnes matrix for two dimensional bar elements.
        Return mat K_0: tangent matrix [4 x 4]
        """
        Ke_0 = np.zeros((self._e_num, 6, 6))

        K_0 = np.zeros((self._max_edof, self._max_edof))

        for i in range(0, self._e_num):
            Ke_0[i] = self.bar3d_ke_0(
                self._ex[i], self._ey[i], self._ez[i], self._EA[i])
            K_0 = self.assem_K(self._edof[i, :], K_0, Ke_0[i])

        return K_0

    def compute_ke_T(self):
        """
        Compute global tangent matrix for two dimensional bar elements.
        Return mat K_T: tangent matrix [4 x 4]
        """
        Ke_0 = np.zeros((self._e_num, 6, 6))
        Ke_u = np.zeros((self._e_num, 6, 6))
        Ke_sigma = np.zeros((self._e_num, 6, 6))

        K_T = np.zeros((self._max_edof, self._max_edof))

        for i in range(0, self._e_num):
            Ke_0[i] = self.bar3d_ke_0(
                self._ex[i], self._ey[i], self._ez[i], self._EA[i])
            Ke_u[i] = self.bar3d_ke_u(
                self._ex[i], self._ey[i], self._ez[i], self._EA[i], self._qe[i])
            Ke_sigma[i] = self.bar3d_ke_sigma(
                self._ex[i], self._ey[i], self._ez[i], self._Ne[i])

        Ke_T = Ke_0+Ke_u+Ke_sigma

        for j in range(0, self._e_num):
            K_T = self.assem_K(self._edof[j, :], K_T, Ke_T[j])

        return K_T


class Forces3D(Element_parameters3D):
    """Class that computes internal forces in elements"""

    def __init__(self, edof, e_num, ex_global, ey_global, ez_global, ep, qe=None):
        """
        :param list ex: element x coordinates [x1, x2]
        :param list ey: element y coordinates [y1, y2]
        :param list ep: [E, A]: E - Young's modulus, A - Cross section area
        :param list qe: element global displacements [q1, q2, q3, q4]
        :param list Ne: element normal force [Ne]
        """
        Element_parameters3D.__init__(self, edof, e_num, ex_global, ey_global, ez_global, ep, qe)

    def bar3d_Ne(self, ex, ey, ez, EA, qe):
        """
        Compute the normal force for two dimensional bar element. (10-33)

        :param list ex: element x coordinates [x1, x2]
        :param list ey: element y coordinates [y1, y2]
        :param list ep: [E, A]: E - Young's modulus, A - Cross section area
        :return normal force
        """
        L = self.length(ex, ey, ez)
        G = self.transfromation_matrix(ex, ey, ez)
        qeloc = np.matmul(G, qe.reshape(6, 1))

        B0 = np.array([-1., 0., 0., 1., 0., 0.])/L

        M = np.array([[1, 0, 0, -1, 0, 0],
                      [0, 1, 0, 0, -1, 0],
                      [0, 0, 1, 0, 0, -1],
                      [-1, 0, 0, 1, 0, 0],
                      [0, -1, 0, 0, 1, 0],
                      [0, 0, -1, 0, 0, 1]
                      ])/L**2

        B1 = np.matmul(qeloc.T, M)
        B = B0+0.5*B1

        N = EA*np.matmul(B, qeloc)
        return N

    def bar3d_Ne_lin(self, ex, ey, ez, EA, qe):
        """
        Compute the normal force for two dimensional bar element. (10-33)

        :param list ex: element x coordinates [x1, x2]
        :param list ey: element y coordinates [y1, y2]
        :param list ep: [E, A]: E - Young's modulus, A - Cross section area
        :return normal force
        """
        L = self.length(ex, ey, ez)
        G = self.transfromation_matrix(ex, ey, ez)
        qeloc = np.matmul(G, qe.reshape(6, 1))

        B = np.array([-1., 0., 0., 1., 0., 0.])/L

        N = EA*np.matmul(B, qeloc)
        return N

    def bar3d_Fe(self, ex, ey, ez, qe, Ne):
        """
        Compute the Fe matrix for two dimensional bar element. (10-43c)

        :param list ex: element x coordinates [x1, x2]
        :param list ey: element y coordinates [y1, y2]
        :param list qe: element global displacements [q1, q2, q3, q4]
        :param list Ne: element normal force [Ne]
        :return mat Fe: [4 x 1]
        """
        L = self.length(ex, ey, ez)
        G = self.transfromation_matrix(ex, ey, ez)
        qeloc = np.matmul(G, qe.reshape(6, 1))

        du = qeloc[3, 0] - qeloc[0, 0]
        dv = qeloc[4, 0] - qeloc[1, 0]
        dw = qeloc[5, 0] - qeloc[2, 0]

        Fe = np.array([
            [-1-du/L],
            [-dv/L],
            [-dw/L],
            [1+du/L],
            [dv/L],
            [dw/L]
        ])

        return np.matmul(G.T, Ne.item()*Fe)

    def assem_F(self, edof, F, Fe):
        """
        Assemble element matrices and fe into the global force vector F
        according to the topology matrix edof.

        Parameters:
            edof        dof topology array
            F           the global force vector
            Fe          element force vector

        Output parameters:
            F           the new global force vector

        """

        if edof.ndim == 1:
            idx = edof-1

            F[np.ix_(idx)] = F[np.ix_(idx)] + Fe
        else:
            for row in edof:
                idx = row-1
                F[np.ix_(idx)] = F[np.ix_(idx)] + Fe

        return F

    def compute_Ne(self):
        """
        Compute global normal force for two dimensional bar elements.
        Return mat K_0: tangent matrix [4 x 4]
        """
        Ne = np.zeros((self._e_num, 1))

        for i in range(0, self._e_num):
            Ne[i] = self.bar3d_Ne(self._ex[i], self._ey[i],
                                  self._ez[i], self._EA[i], self._qe[i])
        self.Ne = Ne

        return Ne

    def compute_Ne_lin(self):
        """
        Compute global normal force for two dimensional bar elements.
        Return mat K_0: tangent matrix [4 x 4]
        """
        Ne = np.zeros((self._e_num, 1))

        for i in range(0, self._e_num):
            Ne[i] = self.bar3d_Ne_lin(self._ex[i], self._ey[i],
                                      self._ez[i], self._EA[i], self._qe[i])
        self.Ne = Ne

        return Ne

    def compute_F(self):
        """
        Compute global internal forces for two dimensional bar elements.
        Return mat K_0: tangent matrix [4 x 4]
        """
        Fe = np.zeros((self._e_num, 6, 1))
        F = np.zeros((self._max_edof, 1))

        for i in range(0, self._e_num):
            Fe[i] = self.bar3d_Fe(
                self._ex[i], self._ey[i], self._ez[i], self._qe[i], self.Ne[i])
            F = self.assem_F(self._edof[i, :], F, Fe[i])

        return F

    def compute_Res(self, Q, R):

        return Q+R-self.compute_F()
