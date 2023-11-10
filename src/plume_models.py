import numpy as np

def briggs_approx(H, U_rel, M_dot, d_s, sigma, r_0=10., beta=0.6):
    H = H

    s4frac = 0.04
    gamma = 3 * s4frac / (2 - 2 * s4frac)

    rho_s = 1841
    d_s = d_s * 1e-6

    N_dot = conversion_factor(M_dot, gamma, d_s, corr=1.0, rho_s=rho_s, sigma=sigma)

    Q = U_rel * np.pi * (r_0 + beta * H) ** 2

    N = (N_dot * 1E-6 / Q)

    return N

def conversion_factor(M_dot, gamma, d_s, corr=1.0, rho_s=1841, sigma=1.6):
    # ds in m
    return 6 * corr * gamma * M_dot / (np.pi * rho_s * (d_s ** 3) * np.exp(4.5 * (np.log(sigma) ** 2)))
