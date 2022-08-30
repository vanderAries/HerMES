import numpy as np
import scipy.interpolate as inter
import matplotlib.pyplot as plt
from structure.truss_classes import Stiffness2D, Stiffness3D, Forces2D, Forces3D


def solveq(K, f, bcPrescr, bcVal=None):

    nDofs = K.shape[0]
    nPdofs = bcPrescr.shape[0]

    if bcVal is None:
        bcVal = np.zeros([nPdofs], 'd')

    bc = np.ones(nDofs, 'bool')
    bcDofs = np.arange(nDofs)

    bc[np.ix_(bcPrescr-1)] = False
    bcDofs = bcDofs[bc]

    fsys = f[bcDofs]-K[np.ix_((bcDofs), (bcPrescr-1))] * \
        np.asmatrix(bcVal).reshape(nPdofs, 1)
    asys = np.linalg.solve(K[np.ix_((bcDofs), (bcDofs))], fsys)

    a = np.zeros([nDofs, 1])
    a[np.ix_(bcPrescr-1)] = np.asmatrix(bcVal).reshape(nPdofs, 1)
    a[np.ix_(bcDofs)] = asys

    R = K*np.asmatrix(a)-f

    return (np.asmatrix(a), R)


def extractElext(edof, a):

    ed = None

    if edof.ndim == 1:
        nDofs = len(edof)
        ed = np.zeros([nDofs])
        idx = edof-1
        ed[:] = a[np.ix_(idx)].T
    else:
        nElements = edof.shape[0]
        nDofs = edof.shape[1]
        ed = np.zeros([nElements, nDofs])
        i = 0
        for row in edof:
            idx = row-1
            ed[i, :] = a[np.ix_(idx)].T
            i += 1

    return ed


class LinearVonMises(object):
    def __init__(self, edof, max_edof, ex, ey, ep, e_num, supports, forces, H):
        self.q = np.asmatrix(np.zeros((max_edof, 1)))
        self.Ne = np.zeros((e_num, 1))

        self.Q = forces
        qe = extractElext(edof, self.q)
        K = Stiffness2D(edof, e_num, ex, ey, ep, qe, self.Ne)
        K0 = K.compute_ke_0()
        self.q, self.R = solveq(K0, self.Q, supports)
        qe = extractElext(edof, self.q)
        Fc = Forces2D(edof, e_num, ex, ey, ep, qe)
        self.Ne = Fc.compute_Ne_lin()
        self.sigma = np.divide(self.Ne.reshape(
            e_num, 1), ep[1].reshape(e_num, 1))
        self.eta = self.q[3]/H
        self.q = np.around(self.q, 4)
        self.R = np.around(self.R, 4)
        self.Ne = np.around(self.Ne, 4)
        self.sigma = np.around(self.sigma, 4)

        print('--------------------------------------')
        print(f'Displacements\n {self.q}')
        print(f'Eta\n {self.eta}')
        print('--------------------------------------')

        self.nodal_R = self.R.reshape(int(max_edof/2), 2)
        self.nodal_q = self.q.reshape(int(max_edof/2), 2)
        self.nodal_Ne = np.repeat(self.Ne, 2).reshape(e_num, 2)


class NonlinearForceVonMises(object):
    def __init__(self, edof, max_edof, ex, ey, ep, e_num, supports, forces, H):
        self.Q = np.zeros((max_edof, 1))
        self.deltaQ = [0.1, 0.1, 0.1, 0.08]
        self.sumdQ = 0

        chart_X = [0]
        chart_Y = [0]
        interp_X = [0]
        interp_Y = [0]
        eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                           linewidth=0.7, label='Equlibrium path')
        plt.style.use('seaborn-ticks')
        plt.title('Equlibrium path')
        plt.xlabel('Displacements [m]')
        plt.ylabel('Forces [N]')
        plt.grid()
        plt.pause(0.001)

        self.q = np.asmatrix(np.zeros((max_edof, 1)))
        self.Ne = np.zeros((e_num, 1))
        self.R = np.asmatrix(np.zeros((max_edof, 1)))

        for self.m in range(0, len(self.deltaQ)):
            self.itr = 0
            self.sumdQ += self.deltaQ[self.m]
            dQ = self.deltaQ[self.m]*forces
            self.Q += dQ
            qe = extractElext(edof, self.q)
            K = Stiffness2D(edof, e_num, ex, ey, ep, qe, self.Ne)
            KT = K.compute_ke_T()
            dq, dR = solveq(KT, dQ, supports)
            self.R += dR
            self.q += dq
            qe = extractElext(edof, self.q)

            chart_X.append(abs(float(self.q[3])))
            chart_Y.append(abs(float(self.Q[3])))
            eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                               linewidth=0.7, label='Equlibrium path')
            plt.pause(0.01)

            while True:
                self.itr += 1
                Fc = Forces2D(edof, e_num, ex, ey, ep, qe)
                self.Ne = Fc.compute_Ne()

                K = Stiffness2D(edof, e_num, ex, ey, ep, qe, self.Ne)
                KT = K.compute_ke_T()
                Res = Fc.compute_Res(self.Q, self.R)

                chart_X.append(abs(float(self.q[3])))
                chart_Y.append(abs(float(self.Q[3])-float(Res[3])))
                interp_X.append(abs(float(self.q[3])))
                interp_Y.append(abs(float(self.Q[3])-float(Res[3])))
                eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                                   linewidth=0.7, label='Equlibrium path')
                plt.pause(0.01)

                Res_norm = np.linalg.norm(Res)

                dq, dR = solveq(KT, Res, supports)
                self.R += dR
                self.q += dq
                dq_norm = np.linalg.norm(dq)
                qe = extractElext(edof, self.q)
                self.eta = self.q[3]/H

                chart_X.append(abs(float(self.q[3])))
                chart_Y.append(abs(float(self.Q[3])))
                eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                                   linewidth=0.7, label='Equlibrium path')
                plt.pause(0.01)

                if (Res_norm < 1e-04 and dq_norm < 1e-04) or self.itr == 40:

                    interp_X.append(abs(float(self.q[3])))
                    interp_Y.append(abs(float(self.Q[3])))

                    inc_range = plt.plot([0, abs(float(self.q[3]))], [abs(float(self.Q[3])), abs(
                        float(self.Q[3]))], linestyle='--', color='#000000', label='Force increment range')
                    inc_range = plt.plot([abs(float(self.q[3])), abs(float(self.q[3]))], [0, abs(
                        float(self.Q[3]))], linestyle='--', color='#000000', label='Force increment range')
                    plt.pause(0.01)

                    self.q = np.around(self.q, 5)
                    self.eta = np.around(self.eta, 5)
                    self.sumdQ = np.around(self.sumdQ, 3)
                    print('--------------------------------------')
                    print(
                        f'Step {self.m}\nForce value: [{self.sumdQ}]\nVertical displacement of center node: {self.q[3]}\nEta: {self.eta} \nIterations: [{self.itr}]')
                    print('--------------------------------------')
                    break

        x = np.linspace(0, interp_X[-1])
        f = inter.interp1d(interp_X, interp_Y, kind='cubic')
        y = f(x)
        interp = plt.plot(x, y, color='#000000', linewidth=0.7,
                          label='Equlibrium path interpoaltion')
        plt.pause(0.01)
        plt.legend(handles=[eq_path[0], inc_range[0], interp[0]],
                   loc='lower right')
        plt.show()

        self.sigma = np.divide(self.Ne.reshape(
            e_num, 1), ep[1].reshape(e_num, 1))
        self.R = np.around(self.R, 4)
        self.Ne = np.around(self.Ne, 4)
        self.sigma = np.around(self.sigma, 4)

        self.nodal_R = self.R.reshape(int(max_edof/2), 2)
        self.nodal_q = self.q.reshape(int(max_edof/2), 2)
        self.nodal_Ne = np.repeat(self.Ne, 2).reshape(e_num, 2)


class NonlinearDisVonMises(object):
    def __init__(self, edof, max_edof, ex, ey, ep, e_num, supports, forces, H):

        self.Q = np.zeros((max_edof, 1))
        self.q = np.asmatrix(np.zeros((max_edof, 1)))
        self.Ne = np.zeros((e_num, 1))
        self.R = np.asmatrix(np.zeros((max_edof, 1)))
        self.Q_ref = forces
        steps = 90
        stepVal = -0.005

        self.bcDis = supports
        self.bcVal = np.zeros((len(self.bcDis), 1))

        for i in range(0, len(forces)):
            if forces[i] != 0:
                self.bcDis = np.append(self.bcDis, [i+1])
                self.bcVal = np.append(self.bcVal, [[stepVal]], axis=0)

        chart_X = [0]
        chart_Y = [0]
        eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                           linewidth=0.7, label='Equlibrium path')
        plt.style.use('seaborn-ticks')
        plt.title('Equlibrium path')
        plt.xlabel('Displacements [m]')
        plt.ylabel('Forces [N]')
        plt.grid()
        plt.pause(0.01)

        for self.m in range(0, steps):
            self.itr = 0
            qe = extractElext(edof, self.q)
            K = Stiffness2D(edof, e_num, ex, ey, ep, qe, self.Ne)
            KT = K.compute_ke_T()
            dq, dR = solveq(KT, self.Q, self.bcDis, self.bcVal)
            self.R += dR
            self.q += dq
            qe = extractElext(edof, self.q)

            chart_X.append(-float(self.q[3]))
            chart_Y.append(-float(self.R[3]))
            eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                               linewidth=0.7, label='Equlibrium path')
            plt.pause(0.01)

            while True:
                self.itr += 1
                Fc = Forces2D(edof, e_num, ex, ey, ep, qe)
                self.Ne = Fc.compute_Ne()

                K = Stiffness2D(edof, e_num, ex, ey, ep, qe, self.Ne)
                KT = K.compute_ke_T()
                Res = Fc.compute_Res(self.Q, self.R)

                chart_X.append(-float(self.q[3]))
                chart_Y.append(-float(self.R[3])-float(Res[3]))
                eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                                   linewidth=0.7, label='Equlibrium path')
                plt.pause(0.01)

                Res_norm = np.linalg.norm(Res)

                dq, dR = solveq(KT, Res, supports)
                self.R += dR
                self.q += dq
                dq_norm = np.linalg.norm(dq)
                qe = extractElext(edof, self.q)
                self.eta = self.q[3]/H

                chart_X.append(-float(self.q[3]))
                chart_Y.append(-float(self.R[3]))
                eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                                   linewidth=0.7, label='Equlibrium path')
                plt.pause(0.01)

                if (Res_norm < 1e-04 and dq_norm < 1e-04) or self.itr == 40:

                    inc_range = plt.plot([0, -(float(self.q[3]))], [-(float(self.R[3])), -(
                        float(self.R[3]))], linestyle='--', color='#000000', label='Force increment range')
                    inc_range = plt.plot([-(float(self.q[3])), -(float(self.q[3]))], [0, -(
                        float(self.R[3]))], linestyle='--', color='#000000', label='Force increment range')
                    plt.pause(0.01)

                    self.q = np.around(self.q, 5)
                    self.eta = np.around(self.eta, 5)
                    print('--------------------------------------')
                    print(
                        f'Step {self.m}\nVertical displacement of center node: {self.q[3]}\nEta: {self.eta} \nIterations: [{self.itr}]')
                    print('--------------------------------------')
                    break

        plt.pause(0.01)
        plt.legend(handles=[eq_path[0], inc_range[0]],
                   loc='lower right')
        plt.show()

        self.sigma = np.divide(self.Ne.reshape(
            e_num, 1), ep[1].reshape(e_num, 1))
        self.R = np.around(self.R, 4)
        self.Ne = np.around(self.Ne, 4)
        self.sigma = np.around(self.sigma, 4)

        self.nodal_R = self.R.reshape(int(max_edof/2), 2)
        self.nodal_q = self.q.reshape(int(max_edof/2), 2)
        self.nodal_Ne = np.repeat(self.Ne, 2).reshape(e_num, 2)


class LinearDome(object):
    def __init__(self, edof, max_edof, ex, ey, ez, ep, e_num, supports, forces):
        self.q = np.asmatrix(np.zeros((max_edof, 1)))
        self.Ne = np.zeros((e_num, 1))

        self.Q = forces
        qe = extractElext(edof, self.q)
        K = Stiffness3D(edof, e_num, ex, ey, ez, ep, qe, self.Ne)
        K0 = K.compute_ke_0()
        self.q, self.R = solveq(K0, self.Q, supports)
        qe = extractElext(edof, self.q)
        Fc = Forces3D(edof, e_num, ex, ey, ez, ep, qe)
        self.Ne = Fc.compute_Ne_lin()
        self.sigma = np.divide(self.Ne.reshape(
            e_num, 1), ep[1].reshape(e_num, 1))
        self.q = np.around(self.q, 4)
        self.R = np.around(self.R, 4)
        self.Ne = np.around(self.Ne, 4)
        self.sigma = np.around(self.sigma, 4)

        print('--------------------------------------')
        print(f'Displacements\n {self.q}')
        print('--------------------------------------')

        self.nodal_R = self.R.reshape(int(max_edof/3), 3)
        self.nodal_q = self.q.reshape(int(max_edof/3), 3)
        self.nodal_Ne = np.repeat(self.Ne, 2).reshape(e_num, 2)


class NonlinearForceDome(object):
    def __init__(self, edof, max_edof, ex, ey, ez, ep, e_num, supports, forces):
        self.Q = np.zeros((max_edof, 1))
        self.deltaQ = [0.1, 0.1, 0.1, 0.08]
        self.sumdQ = 0

        chart_X = [0]
        chart_Y = [0]
        eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                           linewidth=0.7, label='Equlibrium path')
        plt.style.use('seaborn-ticks')
        plt.title('Equlibrium path')
        plt.xlabel('Displacements [m]')
        plt.ylabel('Forces [N]')
        plt.grid()
        plt.pause(0.01)

        self.q = np.asmatrix(np.zeros((max_edof, 1)))
        self.Ne = np.zeros((e_num, 1))
        self.R = np.asmatrix(np.zeros((max_edof, 1)))

        for self.m in range(0, len(self.deltaQ)):
            self.itr = 0
            self.sumdQ += self.deltaQ[self.m]
            dQ = self.deltaQ[self.m]*forces
            self.Q += dQ
            qe = extractElext(edof, self.q)
            K = Stiffness3D(edof, e_num, ex, ey, ez, ep, qe, self.Ne)
            KT = K.compute_ke_T()
            dq, dR = solveq(KT, dQ, supports)
            self.R += dR
            self.q += dq
            qe = extractElext(edof, self.q)

            chart_X.append(abs(float(self.q[2])))
            chart_Y.append(abs(float(self.Q[2])))
            eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                               linewidth=0.7, label='Equlibrium path')
            plt.pause(0.01)

            while True:
                self.itr += 1
                Fc = Forces3D(edof, e_num, ex, ey, ez, ep, qe)
                self.Ne = Fc.compute_Ne()

                K = Stiffness3D(edof, e_num, ex, ey, ez, ep, qe, self.Ne)
                KT = K.compute_ke_T()
                Res = Fc.compute_Res(self.Q, self.R)

                chart_X.append(abs(float(self.q[2])))
                chart_Y.append(abs(float(self.Q[2])-float(Res[2])))
                eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                                   linewidth=0.7, label='Equlibrium path')
                plt.pause(0.01)

                Res_norm = np.linalg.norm(Res)

                dq, dR = solveq(KT, Res, supports)
                self.R += dR
                self.q += dq
                dq_norm = np.linalg.norm(dq)
                qe = extractElext(edof, self.q)

                chart_X.append(abs(float(self.q[2])))
                chart_Y.append(abs(float(self.Q[2])))
                eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                                   linewidth=0.7, label='Equlibrium path')
                plt.pause(0.01)

                if (Res_norm < 1e-04 and dq_norm < 1e-04) or self.itr == 40:

                    inc_range = plt.plot([0, abs(float(self.q[2]))], [abs(float(self.Q[2])), abs(
                        float(self.Q[2]))], linestyle='--', color='#000000', label='Force increment range')
                    inc_range = plt.plot([abs(float(self.q[2])), abs(float(self.q[2]))], [0, abs(
                        float(self.Q[2]))], linestyle='--', color='#000000', label='Force increment range')
                    plt.pause(0.01)

                    self.q = np.around(self.q, 5)
                    self.sumdQ = np.around(self.sumdQ, 3)
                    print('--------------------------------------')
                    print(
                        f'Step {self.m}\nForce value: [{self.sumdQ}]\nVertical displacement of center node: {self.q[2]}\nIterations: [{self.itr}]')
                    print('--------------------------------------')
                    break

        plt.pause(0.01)
        plt.legend(handles=[eq_path[0], inc_range[0]],
                   loc='lower right')
        plt.show()

        self.sigma = np.divide(self.Ne.reshape(
            e_num, 1), ep[1].reshape(e_num, 1))
        self.R = np.around(self.R, 4)
        self.Ne = np.around(self.Ne, 4)
        self.sigma = np.around(self.sigma, 4)

        self.nodal_R = self.R.reshape(int(max_edof/3), 3)
        self.nodal_q = self.q.reshape(int(max_edof/3), 3)
        self.nodal_Ne = np.repeat(self.Ne, 2).reshape(e_num, 2)


class NonlinearDisDome(object):
    def __init__(self, edof, max_edof, ex, ey, ez, ep, e_num, supports, forces):

        self.Q = np.zeros((max_edof, 1))
        self.q = np.asmatrix(np.zeros((max_edof, 1)))
        self.Ne = np.zeros((e_num, 1))
        self.R = np.asmatrix(np.zeros((max_edof, 1)))
        self.Q_ref = forces
        steps = 50
        stepVal = -0.05

        self.bcDis = supports
        self.bcVal = np.zeros((len(self.bcDis), 1))

        for i in range(0, len(forces)):
            if forces[i] != 0:
                self.bcDis = np.append(self.bcDis, [i+1])
                self.bcVal = np.append(self.bcVal, [[stepVal]], axis=0)

        chart_X = [0]
        chart_Y = [0]
        eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                           linewidth=0.7, label='Equlibrium path')
        plt.style.use('seaborn-ticks')
        plt.title('Equlibrium path')
        plt.xlabel('Displacements [m]')
        plt.ylabel('Forces [N]')
        plt.grid()
        plt.pause(0.01)

        for self.m in range(0, steps):
            self.itr = 0
            qe = extractElext(edof, self.q)
            K = Stiffness3D(edof, e_num, ex, ey, ez, ep, qe, self.Ne)
            KT = K.compute_ke_T()
            dq, dR = solveq(KT, self.Q, self.bcDis, self.bcVal)
            self.R += dR
            self.q += dq
            qe = extractElext(edof, self.q)

            chart_X.append(-float(self.q[2]))
            chart_Y.append(-float(self.R[2]))
            eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                               linewidth=0.7, label='Equlibrium path')
            plt.pause(0.01)

            while True:
                self.itr += 1
                Fc = Forces3D(edof, e_num, ex, ey, ez, ep, qe)
                self.Ne = Fc.compute_Ne()

                K = Stiffness3D(edof, e_num, ex, ey, ez, ep, qe, self.Ne)
                KT = K.compute_ke_T()
                Res = Fc.compute_Res(self.Q, self.R)

                chart_X.append(-float(self.q[2]))
                chart_Y.append(-float(self.R[2])-float(Res[2]))
                eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                                   linewidth=0.7, label='Equlibrium path')
                plt.pause(0.01)

                Res_norm = np.linalg.norm(Res)

                dq, dR = solveq(KT, Res, supports)
                self.R += dR
                self.q += dq
                dq_norm = np.linalg.norm(dq)
                qe = extractElext(edof, self.q)

                chart_X.append(-float(self.q[2]))
                chart_Y.append(-float(self.R[2]))
                eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                                   linewidth=0.7, label='Equlibrium path')
                plt.pause(0.01)

                if (Res_norm < 1e-04 and dq_norm < 1e-04) or self.itr == 40:

                    inc_range = plt.plot([0, -(float(self.q[2]))], [-(float(self.R[2])), -(
                        float(self.R[2]))], linestyle='--', color='#000000', label='Force increment range')
                    inc_range = plt.plot([-(float(self.q[2])), -(float(self.q[2]))], [0, -(
                        float(self.R[2]))], linestyle='--', color='#000000', label='Force increment range')
                    plt.pause(0.01)

                    self.q = np.around(self.q, 5)
                    print('--------------------------------------')
                    print(
                        f'Step {self.m}\nVertical displacement of center node: {self.q[2]}\nIterations: [{self.itr}]')
                    print('--------------------------------------')
                    break

        plt.pause(0.01)
        plt.legend(handles=[eq_path[0], inc_range[0]],
                   loc='lower right')
        plt.show()

        self.sigma = np.divide(self.Ne.reshape(
            e_num, 1), ep[1].reshape(e_num, 1))
        self.R = np.around(self.R, 4)
        self.Ne = np.around(self.Ne, 4)
        self.sigma = np.around(self.sigma, 4)

        self.nodal_R = self.R.reshape(int(max_edof/3), 3)
        self.nodal_q = self.q.reshape(int(max_edof/3), 3)
        self.nodal_Ne = np.repeat(self.Ne, 2).reshape(e_num, 2)
