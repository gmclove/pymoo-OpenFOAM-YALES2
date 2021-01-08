import os
import subprocess
import numpy as np


class PostProc:
    def __init__(self, x, gen):
        self.x = np.array([[0, 1]]) #[[0, 1]]  # x
        # create array for objectives
        self.obj = []
        dataFile = 'ics_temporals.txt'

        # Extract parameters for each individual
        for ind in range(len(self.x)):

            para = self.x[ind, :] #x[ind, :]
            omega = para[0]
            freq = para[1]

            print('Individual: '+str(ind))
            print('Parameters: '+str(para))
            print('Omega: '+str(omega))
            print('Freq: '+str(freq))

            ####### Extract data from case file ########
            data = np.genfromtxt('ics_temporals.txt', skip_header=1)
            # collect data after 8 seconds
            noffset = 8 * data.shape[0] // 10
            # extract P_OVER_RHO_INTGRL_(1) and TAU_INTGRL_(1)
            p_over_rho_intgrl_1 = data[noffset:, 4]
            tau_intgrl_1 = data[noffset:, 6]

            ######## Compute Lift and Drag ##########
            drag = np.mean(p_over_rho_intgrl_1 - tau_intgrl_1)
            # lift = np.mean()

            obj_i = [drag] #,lift]
            self.obj.append(obj_i)

localpath = os.getcwd()
a_Omega = np.array([50., 250., 500.] )
a_freq = np.array([5., 10., 20.])

drag = np.zeros((len(a_Omega),len(a_freq)))
iOmega = 0
for Omega in a_Omega:
    ifreq = 0
    for freq in a_freq:
        try:
            os.mkdir("dump")
        except OSError:
            print("dump already exists")
        modif_in(Omega, freq)
        sim = subprocess.run(["sh", "sim.sh"])
        data = np.genfromtxt('dump/ics_temporals.txt', skip_header = 1)
        noffset = 8*data.shape[0]//10
        plt.plot(data[noffset:,3], data[noffset:,4] - data[noffset:,6],'-',label=r"$\Omega = %.1f, f= %.1f$"%(Omega,freq))
        print("Omega = %.1f, f= %.1f, Drag= %.4e"%(Omega,freq,np.mean(data[noffset:,4] - data[noffset:,6])))
        os.replace("dump","run_O"+ "{0:.1f}".format(Omega) + "_f" +"{0:.1f}".format(freq))
        drag[iOmega,ifreq] = np.mean(data[noffset:,4] - data[noffset:,6])
        ifreq += 1
    iOmega +=1
plt.legend()
plt.show()