import numpy as np

def effective_radius(thickness, Nd):
    rho_w = 1000
    f_ad = 1.
    k = 0.8
    Lambda_ad = 2.2e-6
    return 1e6 * ((3 / (4 * np.pi * rho_w)) ** (1 / 3)) * ((f_ad * Lambda_ad) ** (1 / 3)) * ((k * Nd) ** (-1 / 3)) * (
            (thickness) ** (1 / 3))


def thickness(lwp):
    f_ad = 1.
    Lambda_ad = 2.2e-6

    # lwp is in g/m3, so conversion to kg is necessary
    return np.sqrt((2e-3) * lwp / (f_ad * Lambda_ad))


def updraft(ctrc: float, cbh: float, LTS: float, is_coupled: bool):
    if is_coupled:
        return (-0.38 * ctrc + 8.4) / 100.

    if LTS >= 16:
        return (-0.37 * ctrc + 26.1) / 100.

    if LTS < 16:
        return cbh*1e-3*0.9

    return np.nan

def cloud_type (LTS):
    if LTS >=18:
        return "msc"
    elif LTS>14 and LTS <18:
        return "trans"
    elif LTS<=14:
        return "sc"
    else:
        return np.nan


def cloud_regime(updraft, N_cn):
    if N_cn == 0:
        return np.nan
    if (updraft/N_cn) >= 10**(-3):
        return "aerosol-limited"
    if (updraft / N_cn) <= 10 ** (-4):
        return "updraft-limited"
    if ((updraft / N_cn) >= 10 ** (-4)) and ((updraft / N_cn) <= 10 ** (-3)):
        return "transitional"

    return np.nan
