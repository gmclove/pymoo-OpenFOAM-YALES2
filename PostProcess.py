# from paraview.simple import *
import matplotlib

# This is required to 'plot' inside the CLI
matplotlib.use('AGG')

import numpy as np
import matplotlib.pyplot as plt
from parse import *
import os
import sys


class PostProcess:
    def __init__(self, x, gen):
        self.x = x
        self.gen = gen
        self.obj = []
        # self.case

    def main(self, case):
        for ind in range(len(self.x)):
            if case == 'cylinder':
                obj_i = self.cylinder(ind)
            elif case == 'diffuser':
                obj_i = self.diffuser(ind)
            elif case == 'airfoil':
                obj_i = self.airfoil(ind)
            else:
                print('Post-Process: case not found!')

            self.saveText(ind, obj_i)
            self.obj.append(obj_i)

        return self.obj

    ################################################################################
    ######################## MAIN FUNCTIONS ########################################
    ################## Customized for each case ####################################
    ################################################################################

    ################################################################################
    #                   Post-Process Universal Functions                           #
    ################################################################################

    #### Potential Functions in Development ####

    # def readFile(self, path):
    # return data # numpy array
    # def getTimePeriod(self, timeRange):
    # return data # numpy array
    # def applyFunction(fun, data):
    # return obj1, obj2
    # def saveData(self, ind, obj_i):
    # def saveFig():
    # Save figure
    #                 fig, (ax1) = plt.subplots(1, figsize=(10,8))

    #                 ax1.plot(forces[timestp40+fx:,0],forces[timestp40+fx:,1]+forces[timestp40+fx:,4],'b',linewidth=2,label='Pressure Force X')             # ax1.plot(forces[timestp40+fx:,0],np.mean(forces[timestp40+fx:,1])*np.ones(len(forces[timestp40+fx:,0])),':b',linewidth=1)
    #                 ax1.plot(forces[timestp40+fy:,0],forces[timestp40+fy:,2]+forces[timestp40+fy:,5],'g',linewidth=2,label='Pressure Force Y')
    #                 # ax1.plot(forces[timestp40+fy:,0],np.mean(forces[timestp40+fy:,2])*np.ones(len(forces[timestp40+fy:,0])),':g',linewidth=1)
    #                 ax1.set_xlabel('Time (s)', fontsize=16)
    #                 ax1.set_ylabel(r'Force ($N$)', fontsize=16)
    #                 ax1.legend(loc='lower left', fontsize=16)
    #                 ax1.tick_params(labelsize=14)
    #                 ax1.set_ylim([-0.3,0.3])
    #                 ax1.set_xlim([0,150])
    #                 # Save figure
    #                 fig, (ax1) = plt.subplots(1, figsize=(10,8))
    #                 plt.savefig('./cases/gen%i/data/OSCg%ii%i.png' %(self.gen, self.gen, ind), bbox_inches='tight', dpi=100)
    def saveText(self, ind, obj_i):
        #         try:
        #             os.mkdir('./cases/gen%i/data'%self.gen)
        #         except OSError as error:
        #             print(error)
        # Save fitness to text file
        np.savetxt('./cases/gen%i/data/FITg%ii%i.txt' % (self.gen, self.gen, ind),
                   np.array(obj_i))

    def paraview(self):
        # OpenFOAM file generation
        os.system('touch cases/gen%i/ind%i/g%ii%i.OpenFOAM'
                  % (self.gen, ind, self.gen, ind))
        ### paraview batch mode ###
        L = self.x[ind, 0]
        theta = self.x[ind, 1]
        L_diff = 4 + L * np.cos(np.deg2rad(theta))
        print('L_diff: %f' % L_diff)
        os.system('pvbatch paraviewPostProcess.py %i %i %.8f'
                  % (self.gen, ind, L_diff))

    def airfoil(self, ind):
        # Package importation
        from scipy import integrate

        # MAIN FUNCTION
        def main():
            # print('AIRFOIL')
            lift, drag = forcePlotAnalysis(ind)
            # area = areaCalc(ind)

            obj_i = [-lift, drag]
            return obj_i

        ######################################################################
        ################### Airfoil Case Function ############################
        def forcePlotAnalysis(ind):
            def main():
                # print('FORCE PLOT ANALYSIS')
                ################################################################################
                #                                    INPUTS                                    #
                ################################################################################
                # Define the expected header of the forces.dat file
                header = ["time",
                          "pressureF_x", "pressureF_y", "pressureF_z",
                          "viscousF_x", "viscousF_y", "viscousF_z",
                          "porousF_x", "porousF_y", "porousF_z",
                          "pressureM_x", "pressureM_y", "pressureM_z",
                          "viscousM_x", "viscousM_y", "viscousM_z",
                          "porousM_x", "porousM_y", "porousM_z"]

                # Give a example line to parse
                exampleLine = "{}\t(({} {} {}) ({} {} {}) ({} {} {})) (({} {} {}) ({} {} {}) ({} {} {}))\n"

                # Read the file and store it in "lines"
                lines = []
                with open('./cases/gen%i/ind%i/postProcessing/forces/0/forces.dat' % (self.gen, ind), 'rt') as in_file:
                    for line in in_file:
                        lines.append(line)  # Appends current line into lines
                # forces matrix will have len(lines) rows and 19 columns:
                # time-Fxp-Fyp-Fzp-Fxv-Fyv-Fzv-Fxp-Fyp-Fzp-Mxp-Myp-Mzp-Mxv-Myv-Mzv-Mxp-Myp-Mzp
                forces = np.zeros((len(lines), 19))

                # Iterate along the number of rows (timesteps)
                for i in range(len(lines)):
                    # Check if there is ocurrences in the line
                    if parse(exampleLine, lines[i]) != None:
                        # If there are ocurrences, copy them into the array
                        for j in range(19):
                            forces[i, j] = float(parse(exampleLine, lines[i])[j])

                # Remove the zeros in the matrix that may exist due to preallocation
                forces = forces[forces[:, 0] != 0]

                D = forces[-1, 1] + forces[-1, 4]
                L = forces[-1, 2] + forces[-1, 5]

                # Boundary conditions
                U = 30  # m/s
                rho = 1.225  # kg/m^3
                # area of airfoil
                A = areaCalc(ind)  # m^3
                CL = (L * 2) / (rho * U ** 2 * A)  # [N]/([kg/m^3][m/s]^2[m^2])=unitless
                CD = (D * 2) / (rho * U ** 2 * A)

                #             print('D: ')
                #             print(D)
                #             print('L: ')
                #             print(L)
                #             print('lift:')
                #             print(lift)
                #             print('drag:')
                #             print(drag)
                ###### PLOTTING OPTION ######
                # plotting(forces)

                return L, D

                ################################################################################
                #                                FITNESS DATA                                  #
                ################################################################################

            #             np.savetxt('./cases/gen%i/data/FITg%ii%i.txt' %(self.gen, self.gen, ind),
            #                       np.array((D,L)))

            def plotting(forces):
                ################################################################################
                #                                   PLOTTING                                   #
                ################################################################################
                # Fancy plot settings
                #             plt.style.use('seaborn-deep')
                #             plt.style.use('classic')
                #             matplotlib.rcParams['axes.linewidth'] = 1.3
                #             matplotlib.rcParams['lines.linewidth'] = 1.3
                #             matplotlib.rc('text', usetex=True)
                #             matplotlib.rcParams['text.latex.preamble'] = [r"\usepackage{amsmath}"]
                #             matplotlib.rcParams.update({'font.size': 8})

                # Figure definition
                fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 15))
                fig.subplots_adjust(wspace=0.3, hspace=0.25)

                # Upper left subplot
                ax1.plot(forces[:, 0], forces[:, 1], 'b', linewidth=3, label='Pressure Force X')
                ax1.plot(forces[:, 0], forces[:, 2], 'g', linewidth=3, label='Pressure Force Y')
                ax1.set_ylim(-1 * np.max(np.abs([forces[-1, 1:3]])), 2 * np.max(np.abs([forces[-1, 1:3]])))
                ax1.set_xlabel(r'Iteration Number', fontsize=24)
                ax1.set_ylabel(r'Force (N)', fontsize=24)
                ax1.legend(loc='upper right', fontsize=20)
                ax1.tick_params(labelsize=26)

                # Upper right subplot
                ax2.plot(forces[:, 0], forces[:, 4], 'r', linewidth=3, label='Viscous Force X')
                ax2.set_ylim(0, 2 * np.abs([forces[-1, 4]]))
                ax2.set_xlabel(r'Iteration Number', fontsize=24)
                ax2.set_ylabel(r'Force (N)', fontsize=24)
                ax2.legend(loc='upper right', fontsize=20)
                ax2.tick_params(labelsize=26)

                # Lower left subplot
                ax3.plot(forces[:, 0], forces[:, 12], 'm', linewidth=3, label='Pressure Moment Z')
                ax3.set_ylim(-2 * np.abs([forces[-1, 12]]), 2 * np.abs([forces[-1, 12]]))
                ax3.set_xlabel(r'Iteration Number', fontsize=24)
                ax3.set_ylabel(r'Moment (N m)', fontsize=24)
                ax3.legend(loc='lower right', fontsize=20)
                ax3.tick_params(labelsize=26)

                # Lower right subplot
                ax4.plot(forces[:, 0], forces[:, 15], 'k', linewidth=3, label='Viscous Moment Z')
                ax4.set_ylim(-2 * np.abs([forces[-1, 15]]), 2 * np.abs([forces[-1, 15]]))
                ax4.set_xlabel(r'Iteration Number', fontsize=24)
                ax4.set_ylabel(r'Moment (N$\cdot$m)', fontsize=24)
                ax4.legend(loc='upper right', fontsize=20)
                ax4.tick_params(labelsize=26)

                # General figure title
                fig.suptitle('Generation %i Individual %i' % (self.gen, ind), fontsize=30)

                # Figure saving
                plt.savefig('./cases/gen%i/data/CONg%ii%i.png' % (self.gen, self.gen, ind), bbox_inches='tight',
                            dpi=100)

            lift, drag = main()
            return lift, drag

        def areaCalc(ind):
            def main():
                ################################################################################
                #                                    INPUTS                                    #
                ################################################################################
                # Get the inputs from the terminal line
                x_cent = self.x[ind, 0]
                y_cent = self.x[ind, 1]

                ################################################################################
                #                            PARAMETER DECLARATION                             #
                ################################################################################
                # Reference percentage of the chord
                pc = 0.25;

                # Airfoil coordinate set of points
                xTemp, yTemp = joukowsky(x_cent, y_cent)
                x, y = airfoil_correction(xTemp, yTemp)

                # Location of the two pc-intercepts for the airfoil
                firstPC = np.argwhere(x - pc < 0)[0]
                lastPC = np.argwhere(x - pc < 0)[-1]

                # Get the position of the y-intercept point
                if np.any(y == 0):
                    zeroLoc = np.argwhere(y == 0)[1]
                else:
                    zeroLoc = np.argwhere(y < 0)[0]

                # Depending on the sign of y at pc, get the y-components for the x_pc
                if y[lastPC] < 0:
                    ypcPos = y[firstPC]
                    ypcNeg = y[lastPC]
                else:
                    ypcPos = y[lastPC]
                    ypcNeg = y[firstPC]

                # Avoid excessive refinement in the leading edge
                y = np.delete(y, np.argwhere(x < 0.0005))
                x = np.delete(x, np.argwhere(x < 0.0005))
                points = np.vstack((x, y)).T

                # Separate between the upper and lower airfoil surfaces
                upper = points[:np.argwhere(y < 0)[0][0], :]
                lower = points[np.argwhere(y < 0)[0][0]:, :]

                # Separate between the 4 quadrants specified with the y = 0 line and the specified pc
                UL = upper[upper[:, 0] < pc, :]
                UR = upper[upper[:, 0] > pc, :]
                LL = lower[lower[:, 0] < pc, :]
                LR = lower[lower[:, 0] > pc, :]

                # Sort the 4 quadrants with increasing x-component
                UL = UL[np.argsort(UL[:, 0]), :]
                UR = UR[np.argsort(UR[:, 0]), :]
                LL = LL[np.argsort(LL[:, 0]), :]
                LR = LR[np.argsort(LR[:, 0]), :]

                # Fix the first and last points of every quadrant
                UL[0, :] = np.array([0, 0])
                UL[-1, :] = np.array([pc, ypcPos])
                UR[0, :] = np.array([pc, ypcPos])
                UR[-1, :] = np.array([1, 0])
                LL[0, :] = np.array([0, 0])
                LL[-1, :] = np.array([pc, ypcNeg])
                LR[0, :] = np.array([pc, ypcNeg])
                LR[-1, :] = np.array([1, 0])

                ################################################################################
                #                               AREA CALCULATION                               #
                ################################################################################
                # Once the different lines are computed, the area will be computed as the integral of those lines

                # In case the lower surface of the airfoil interceps the y = 0 axis, it must be divided so all areas
                # are computed independently
                lowerNeg = lower[lower[:, 1] < 0, :]
                lowerPos = lower[lower[:, 1] > 0, :]

                # Upper surface area
                A1 = integrate.simps(upper[np.argsort(upper[:, 0]), 1], upper[np.argsort(upper[:, 0]), 0])
                # Lower surface area for points with negative y
                A2 = -integrate.simps(lowerNeg[np.argsort(lowerNeg[:, 0]), 1], lowerNeg[np.argsort(lowerNeg[:, 0]), 0])
                # Possible lower surface area for points with positive y
                A3 = integrate.simps(lowerPos[np.argsort(lowerPos[:, 0]), 1], lowerPos[np.argsort(lowerPos[:, 0]), 0])

                # The area will be the sum of the areas and substracting the possible intercept of both
                area = A1 + A2 - A3

                # Append the area into the FIT file for the generation and individual
                with open('./cases/gen%i/data/FITg%ii%i.txt' % (self.gen, self.gen, ind), "a") as file:
                    file.write(str(area))

                return area

            ################################################################################
            #                              FUNCTION DEFINITION                             #
            ################################################################################
            def joukowsky(x_cent, y_cent):
                '''Joukowsky airfoil components calculation (fixed radius)

                INPUTS:
                x_cent: float with the x-position of the center
                y_cent: float with the y-position of the center

                OUTPUT:
                x1:     cartesian coordinates for horizontal axis
                y1:     cartesian coordinates for vertical axis

                This function computes the cartesian coordinates of a Joukowsky
                airfoil from the position of the center, having always the radius
                fixed so it can go through the points |0,1|
                '''

                # Circle parameters definition
                center = np.array([x_cent, y_cent])
                radius1 = np.sqrt((center[0] - 1) ** 2 + (center[1] - 0) ** 2)
                # Second circle will be neglected

                # Circle coordinates calculations
                angle = np.linspace(0, 2 * np.pi, 500)
                chi1 = center[0] + radius1 * np.cos(angle)
                eta1 = center[1] + radius1 * np.sin(angle)

                # Cartesian components of the Joukowsky transform
                x1 = ((chi1) * (chi1 ** 2 + eta1 ** 2 + 1)) / (chi1 ** 2 + eta1 ** 2)
                y1 = ((eta1) * (chi1 ** 2 + eta1 ** 2 - 1)) / (chi1 ** 2 + eta1 ** 2)

                return x1, y1

            def airfoil_correction(x, y):
                '''Set the airfoil chord to 1 and the leading edge to (0,0)

                INPUT:
                x:     cartesian coordinates for horizontal axis
                y:     cartesian coordinates for vertical axis

                OUTPUT:
                xCorr: corrected cartesian coordinates for horizontal axis
                yCorr: corrected cartesian coordinates for vertical axis

                The function scales the airfoil to match the chord dimension to
                a value of 1 (proportionally scaling the vertical dimension). The
                leading edge of the airfoil is moved after to a position in (0,0)
                '''
                # Compute the scale factor (actual chord length)
                c = np.max(x) - np.min(x)

                # Leading edge current position
                LE = np.min(x / c)

                # Corrected position of the coordinates
                xCorr = x / c - LE
                yCorr = y / c

                return xCorr, yCorr

            area = main()
            return area

        obj_i = main()
        return obj_i

