import numpy as np
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


class LinearSolver2D:
    def __init__(self, edof, max_edof, ex, ey, ep, e_num, supports, forces):
        self.q = np.asmatrix(np.zeros((max_edof, 1)))
        self.Ne = np.zeros((e_num, 1))

        Q = forces
        qe = extractElext(edof, self.q)
        K = Stiffness2D(edof, e_num, ex, ey, ep, qe, self.Ne)
        K0 = K.compute_ke_0()
        self.q, self.R = solveq(K0, Q, supports)
        qe = extractElext(edof, self.q)
        Fe = Forces2D(edof, e_num, ex, ey, ep, qe)
        self.Ne = Fe.compute_Ne_lin()

        self.sigma = np.divide(self.Ne.reshape(
            e_num, 1), ep[1].reshape(e_num, 1))

        print('--------------------------------------')
        print(f'displacements\n {self.q}')
        print('--------------------------------------')

        # Print results

        self.nodal_R = self.R.reshape(int(max_edof/2), 2)
        self.nodal_q = self.q.reshape(int(max_edof/2), 2)
        self.nodal_Ne = np.repeat(self.Ne, 2).reshape(e_num, 2)

        self.q = np.around(self.q, 5)
        self.nodal_q = np.around(self.nodal_q, 5)
        self.nodal_R = np.around(self.nodal_R, 5)
        self.Ne = np.around(self.Ne, 5)
        self.nodal_Ne = np.around(self.nodal_Ne, 5)
        self.sigma = np.around(self.sigma, 5)

        dis = []
        for h in range(0, int(max_edof/2)):
            dis.append(
                [f"Node_{h+1}: " + str(self.nodal_q[h])])
        self.show_q = str(np.array(dis).reshape(int(max_edof/2), 1))
        self.show_q = self.show_q.replace(",", "")
        self.show_q = self.show_q.replace("[", "")
        self.show_q = self.show_q.replace("]", "")
        self.show_q = self.show_q.replace("'", "")


class LinearSolver3D:
    def __init__(self, edof, max_edof, ex, ey, ez, ep, e_num, supports, forces):
        self.q = np.asmatrix(np.zeros((max_edof, 1)))
        Ne = np.zeros((e_num, 1))

        Q = forces
        qe = extractElext(edof, self.q)
        K = Stiffness3D(edof, e_num, ex, ey, ez, ep, qe, Ne)
        K0 = K.compute_ke_0()
        self.q, self.R = solveq(K0, Q, supports)
        qe = extractElext(edof, self.q)
        Fe = Forces3D(edof, e_num, ex, ey, ez, ep, qe)
        self.Ne = Fe.compute_Ne_lin()
        self.sigma = np.divide(self.Ne.reshape(
            e_num, 1), ep[1].reshape(e_num, 1))

        print('--------------------------------------')
        print(f'displacements\n {self.q}')
        print('--------------------------------------')

        # Print results

        self.nodal_R = self.R.reshape(int(max_edof/3), 3)
        self.nodal_q = self.q.reshape(int(max_edof/3), 3)
        self.nodal_Ne = np.repeat(self.Ne, 2).reshape(e_num, 2)

        self.q = np.around(self.q, 5)
        self.nodal_q = np.around(self.nodal_q, 5)
        self.nodal_R = np.around(self.nodal_R, 5)
        self.Ne = np.around(self.Ne, 5)
        self.nodal_Ne = np.around(self.nodal_Ne, 5)
        self.sigma = np.around(self.sigma, 5)

        dis = []
        for h in range(0, int(max_edof/3)):
            dis.append(
                [f"Node_{h+1}: " + str(self.nodal_q[h])])
        self.show_q = str(np.array(dis).reshape(int(max_edof/3), 1))
        self.show_q = self.show_q.replace(",", "")
        self.show_q = self.show_q.replace("[", "")
        self.show_q = self.show_q.replace("]", "")
        self.show_q = self.show_q.replace("'", "")


class NonlinearForceSolver2D:
    def __init__(self, edof, max_edof, ex, ey, ep, e_num, supports, forces, incermentsNum, maxIter, resNorm, disNorm, dofTrack):
        self.Q = np.zeros((max_edof, 1))
        deltaQ = 1/incermentsNum

        self.q = np.asmatrix(np.zeros((max_edof, 1)))
        self.Ne = np.zeros((e_num, 1))
        self.R = np.asmatrix(np.zeros((max_edof, 1)))

        chart_X = [0]
        chart_Y = [0]
        eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                           linewidth=0.7, label='Equlibrium path')
        plt.style.use('seaborn-ticks')
        plt.title('Equlibrium path')
        plt.xlabel('Displacements [m]')
        plt.ylabel('Forces [N]')
        plt.grid()
        plt.pause(0.0001)

        for m in range(0, incermentsNum):
            itr = 0
            dQ = deltaQ*forces
            self.Q += dQ
            qe = extractElext(edof, self.q)
            K = Stiffness2D(edof, e_num, ex, ey, ep, qe, self.Ne)
            KT = K.compute_ke_T()
            dq, dR = solveq(KT, dQ, supports)
            self.R += dR
            self.q += dq
            qe = extractElext(edof, self.q)

            chart_X.append(abs(float(self.q[dofTrack])))
            chart_Y.append(abs(float(self.Q[dofTrack])))
            eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                               linewidth=0.7, label='Equlibrium path')
            plt.pause(0.0001)

            while True:
                itr += 1
                Fc = Forces2D(edof, e_num, ex, ey, ep, qe)
                self.Ne = Fc.compute_Ne()

                K = Stiffness2D(edof, e_num, ex, ey, ep, qe, self.Ne)
                KT = K.compute_ke_T()
                Res = Fc.compute_Res(self.Q, self.R)

                chart_X.append(abs(float(self.q[dofTrack])))
                chart_Y.append(
                    abs(float(self.Q[dofTrack])-float(Res[dofTrack])))
                eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                                   linewidth=0.7, label='Equlibrium path')
                plt.pause(0.0001)

                Res_norm = np.linalg.norm(Res)

                dq, dR = solveq(KT, Res, supports)
                self.R += dR
                self.q += dq
                dq_norm = np.linalg.norm(dq)
                qe = extractElext(edof, self.q)

                chart_X.append(abs(float(self.q[dofTrack])))
                chart_Y.append(abs(float(self.Q[dofTrack])))
                eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                                   linewidth=0.7, label='Equlibrium path')
                plt.pause(0.0001)

                if (Res_norm < resNorm and dq_norm < disNorm) or itr == maxIter:

                    inc_range = plt.plot([0, abs(float(self.q[dofTrack]))], [abs(float(self.Q[dofTrack])), abs(
                        float(self.Q[dofTrack]))], linestyle='--', color='#000000', label='Force increment range')
                    inc_range = plt.plot([abs(float(self.q[dofTrack])), abs(float(self.q[dofTrack]))], [0, abs(
                        float(self.Q[dofTrack]))], linestyle='--', color='#000000', label='Force increment range')
                    plt.pause(0.01)

                    print('--------------------------------------')
                    print(
                        f'Step {m+1} \n\ndisplacements\n {self.q} \n\niter [{itr}]')
                    print('--------------------------------------')
                    break

        plt.pause(0.0001)
        plt.legend(handles=[eq_path[0], inc_range[0]],
                   loc='lower right')
        plt.show()

        self.sigma = np.divide(self.Ne.reshape(
            e_num, 1), ep[1].reshape(e_num, 1))

        self.nodal_R = self.R.reshape(int(max_edof/2), 2)
        self.nodal_q = self.q.reshape(int(max_edof/2), 2)
        self.nodal_Ne = np.repeat(self.Ne, 2).reshape(e_num, 2)

        self.q = np.around(self.q, 5)
        self.nodal_q = np.around(self.nodal_q, 5)
        self.nodal_R = np.around(self.nodal_R, 5)
        self.Ne = np.around(self.Ne, 5)
        self.nodal_Ne = np.around(self.nodal_Ne, 5)
        self.sigma = np.around(self.sigma, 5)

        dis = []
        for h in range(0, int(max_edof/2)):
            dis.append(
                [f"Node_{h+1}: " + str(self.nodal_q[h])])
        self.show_q = str(np.array(dis).reshape(int(max_edof/2), 1))
        self.show_q = self.show_q.replace(",", "")
        self.show_q = self.show_q.replace("[", "")
        self.show_q = self.show_q.replace("]", "")
        self.show_q = self.show_q.replace("'", "")


class NonlinearDisSolver2D:
    def __init__(self, edof, max_edof, ex, ey, ep, e_num, supports, forces, incermentsVal, maxIter, resNorm, disNorm, dofTrack, dofControl):

        m = 0

        self.Q = np.zeros((max_edof, 1))
        self.q = np.asmatrix(np.zeros((max_edof, 1)))
        self.Ne = np.zeros((e_num, 1))
        self.R = np.asmatrix(np.zeros((max_edof, 1)))
        self.Q_ref = forces

        self.bcDis = supports
        self.bcVal = np.zeros((len(self.bcDis), 1))

        if dofControl == -1:
            for i in range(0, len(forces)):
                if forces[i] != 0:
                    self.bcDis = np.append(self.bcDis, [i+1])
                    if forces[i] > 0:
                        self.bcVal = np.append(
                            self.bcVal, [[incermentsVal]], axis=0)
                    else:
                        self.bcVal = np.append(
                            self.bcVal, [[-incermentsVal]], axis=0)
        else:
            self.bcDis = np.append(self.bcDis, [dofControl+1])
            print(self.bcDis)
            self.Q = self.Q_ref
            self.Q[dofControl] = 0
            # tymczasowo dopoki ponizszy warunek nie zadziala
            self.bcVal = np.append(self.bcVal, [[-incermentsVal]], axis=0)

            # Z jakiegos powodu ten warunek nie dziala, nie dodaje nic do bcVal
            # if forces[dofControl] > 0:
            #     self.bcVal = np.append(self.bcVal, [[incermentsVal]], axis=0)
            # elif forces[dofControl] < 0:
            #     self.bcVal = np.append(self.bcVal, [[-incermentsVal]], axis=0)
            # else:
            #     print(
            #         f"There is no force in {dofControl+1} degree of freedom. Pick another dof.")
            print(self.bcVal)

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

        print("FIRST SEQUENCE - DONE")

        while True:
            m += 1
            itr = 0
            qe = extractElext(edof, self.q)
            K = Stiffness2D(edof, e_num, ex, ey, ep, qe, self.Ne)
            KT = K.compute_ke_T()
            dq, dR = solveq(KT, self.Q, self.bcDis, self.bcVal)
            self.R += dR
            self.q += dq
            qe = extractElext(edof, self.q)

            chart_X.append(-(float(self.q[dofTrack])))
            chart_Y.append(-(float(self.R[dofTrack])))
            eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                               linewidth=0.7, label='Equlibrium path')
            plt.pause(0.01)

            print("SECOND SEQUENCE - DONE")

            while True:
                itr += 1
                Fc = Forces2D(edof, e_num, ex, ey, ep, qe)
                self.Ne = Fc.compute_Ne()

                K = Stiffness2D(edof, e_num, ex, ey, ep, qe, self.Ne)
                KT = K.compute_ke_T()
                Res = Fc.compute_Res(self.Q, self.R)

                chart_X.append(-(float(self.q[dofTrack])))
                chart_Y.append(
                    -(float(self.R[dofTrack])-float(Res[dofTrack])))
                eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                                   linewidth=0.7, label='Equlibrium path')
                plt.pause(0.01)

                Res_norm = np.linalg.norm(Res)

                dq, dR = solveq(KT, Res, supports)
                self.R += dR
                self.q += dq
                dq_norm = np.linalg.norm(dq)
                qe = extractElext(edof, self.q)

                chart_X.append(-(float(self.q[dofTrack])))
                chart_Y.append(-(float(self.R[dofTrack])))
                eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                                   linewidth=0.7, label='Equlibrium path')
                plt.pause(0.01)

                print(f"THIRD SEQUENCE - DONE itr {itr}")
                print(f"MAX iter {maxIter}")

                if (Res_norm < resNorm and dq_norm < disNorm) or itr == maxIter:

                    inc_range = plt.plot([0, -(float(self.q[dofTrack]))], [-(float(self.R[dofTrack])), -(
                        float(self.R[dofTrack]))], linestyle='--', color='#000000', label='Force increment range')
                    inc_range = plt.plot([-(float(self.q[dofTrack])), -(float(self.q[dofTrack]))], [0, -(
                        float(self.R[dofTrack]))], linestyle='--', color='#000000', label='Force increment range')
                    plt.pause(0.01)

                    print('--------------------------------------')
                    print(
                        f'Step {m} \n\ndisplacements\n {self.q} \n\niter [{itr}]')
                    print('--------------------------------------')
                    break

            for i in range(0, len(self.Q_ref)):
                if self.Q_ref[i] != 0 and self.R[i] == self.Q_ref[i]:
                    self.bcVal[i] = 0
            print("FOURTH SEQUENCE - DONE")

            if np.linalg.norm(self.bcVal) == 0:
                print("FIFTH SEQUENCE - DONE")
                break

        plt.pause(0.01)
        plt.legend(handles=[eq_path[0], inc_range[0]],
                   loc='lower right')
        plt.show()

        self.sigma = np.divide(self.Ne.reshape(
            e_num, 1), ep[1].reshape(e_num, 1))

        self.nodal_R = self.R.reshape(int(max_edof/2), 2)
        self.nodal_q = self.q.reshape(int(max_edof/2), 2)
        self.nodal_Ne = np.repeat(self.Ne, 2).reshape(e_num, 2)

        self.q = np.around(self.q, 5)
        self.nodal_q = np.around(self.nodal_q, 5)
        self.nodal_R = np.around(self.nodal_R, 5)
        self.Ne = np.around(self.Ne, 5)
        self.nodal_Ne = np.around(self.nodal_Ne, 5)
        self.sigma = np.around(self.sigma, 5)


class NonlinearForceSolver3D:
    def __init__(self, edof, max_edof, ex, ey, ez, ep, e_num, supports, forces, incermentsNum, maxIter, resNorm, disNorm, dofTrack):
        self.Q = np.zeros((max_edof, 1))
        deltaQ = 1/incermentsNum

        self.q = np.asmatrix(np.zeros((max_edof, 1)))
        self.Ne = np.zeros((e_num, 1))
        self.R = np.asmatrix(np.zeros((max_edof, 1)))

        chart_X = [0]
        chart_Y = [0]
        eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                           linewidth=0.7, label='Equlibrium path')
        plt.style.use('seaborn-ticks')
        plt.title('Equlibrium path')
        plt.xlabel('Displacements [m]')
        plt.ylabel('Forces [N]')
        plt.grid()
        plt.pause(0.0001)

        for m in range(0,  incermentsNum):
            itr = 0
            dQ = deltaQ*forces
            self.Q += dQ
            qe = extractElext(edof, self.q)
            K = Stiffness3D(edof, e_num, ex, ey, ez, ep, qe, self.Ne)
            KT = K.compute_ke_T()
            dq, dR = solveq(KT, dQ, supports)
            self.R += dR
            self.q += dq
            qe = extractElext(edof, self.q)

            chart_X.append(abs(float(self.q[dofTrack])))
            chart_Y.append(abs(float(self.Q[dofTrack])))
            eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                               linewidth=0.7, label='Equlibrium path')
            plt.pause(0.0001)

            while True:
                itr += 1
                Fc = Forces3D(edof, e_num, ex, ey, ez, ep, qe)
                self.Ne = Fc.compute_Ne()

                K = Stiffness3D(edof, e_num, ex, ey, ez, ep, qe, self.Ne)
                KT = K.compute_ke_T()
                Res = Fc.compute_Res(self.Q, self.R)

                chart_X.append(abs(float(self.q[dofTrack])))
                chart_Y.append(
                    abs(float(self.Q[dofTrack])-float(Res[dofTrack])))
                eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                                   linewidth=0.7, label='Equlibrium path')
                plt.pause(0.0001)

                Res_norm = np.linalg.norm(Res)
                dq, dR = solveq(KT, Res, supports)
                self.R += dR
                self.q += dq
                dq_norm = np.linalg.norm(dq)
                qe = extractElext(edof, self.q)

                chart_X.append(abs(float(self.q[dofTrack])))
                chart_Y.append(abs(float(self.Q[dofTrack])))
                eq_path = plt.plot(chart_X, chart_Y, color='#f07200',
                                   linewidth=0.7, label='Equlibrium path')
                plt.pause(0.0001)

                if (Res_norm < resNorm and dq_norm < disNorm) or itr == maxIter:

                    inc_range = plt.plot([0, abs(float(self.q[dofTrack]))], [abs(float(self.Q[dofTrack])), abs(
                        float(self.Q[dofTrack]))], linestyle='--', color='#000000', label='Force increment range')
                    inc_range = plt.plot([abs(float(self.q[dofTrack])), abs(float(self.q[dofTrack]))], [0, abs(
                        float(self.Q[dofTrack]))], linestyle='--', color='#000000', label='Force increment range')
                    plt.pause(0.0001)

                    print('--------------------------------------')
                    print(
                        f'Step {m+1} \n\ndisplacements\n {self.q} \n\niter [{itr}]')
                    print('--------------------------------------')
                    break

        plt.pause(0.0001)
        plt.legend(handles=[eq_path[0], inc_range[0]],
                   loc='lower right')
        plt.show()

        self.sigma = np.divide(self.Ne.reshape(
            e_num, 1), ep[1].reshape(e_num, 1))

        self.nodal_R = self.R.reshape(int(max_edof/3), 3)
        self.nodal_q = self.q.reshape(int(max_edof/3), 3)
        self.nodal_Ne = np.repeat(self.Ne, 2).reshape(e_num, 2)

        self.q = np.around(self.q, 5)
        self.nodal_q = np.around(self.nodal_q, 5)
        self.nodal_R = np.around(self.nodal_R, 5)
        self.Ne = np.around(self.Ne, 5)
        self.nodal_Ne = np.around(self.nodal_Ne, 5)
        self.sigma = np.around(self.sigma, 5)

        dis = []
        for h in range(0, int(max_edof/3)):
            dis.append(
                [f"Node_{h+1}: " + str(self.nodal_q[h])])
        self.show_q = str(np.array(dis).reshape(int(max_edof/3), 1))
        self.show_q = self.show_q.replace(",", "")
        self.show_q = self.show_q.replace("[", "")
        self.show_q = self.show_q.replace("]", "")
        self.show_q = self.show_q.replace("'", "")


class NonlinearDisSolver3D:
    pass
