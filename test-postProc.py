import numpy as np

x = np.array([[0, 1]])
para = x[0, :]
print(para)
omega = para[0]
print(omega)

data = np.genfromtxt('cases/ics_2D_cylinder_r2/ics_temporals.txt', skip_header=1)
# # collect data after 8 seconds
# noffset = 8 * data.shape[0] // 10
# # extract P_OVER_RHO_INTGRL_(1) and TAU_INTGRL_(1)
# p_over_rho_intgrl_1 = data[noffset:, 4]
# tau_intgrl_1 = data[noffset:, 6]

p_over_rho_intgrl_1 = data[:, 4]
tau_intgrl_1 = data[:, 6]

print(p_over_rho_intgrl_1)


