from pyrcel import binned_activation, arg2000, mbn2014, ParcelModel
from aerosols import aerosols, size_distribution
import numpy as np
from scipy.interpolate import RegularGridInterpolator

accom = 0.3

def calc_Nd(eq, pol, bgd, factor=1.0):
    # eq needs to be in the format [pol, bgd] not [bgd,pol]
    # Computes Nd as frac*Npol + frac*Nbgd
    Nd = 0.0
    for i in range(len(eq)):

        if pol is not None:
            if i < len(pol.ns):
                Nd += eq[i] * pol.ns[i]
            else:
                Nd += eq[i] * bgd.ns[i - len(pol.ns)]
        else:
            Nd += eq[i] * bgd.ns[i]

    return Nd * factor


def find_CN_arg(Nd_desired, T0, P0, W, distribution, n_iter, d_bgd=None, sigma_bgd=None, k_bgd=None, gamma_bgd=None):

    N_cn_bgd_tests = np.linspace(0.01, 2000, n_iter)
    rms_error_Nd_min = 1e32

    N_cn = 0
    for N_cn_bgd_test in N_cn_bgd_tests:

        bgd = aerosols(name='bgd',
                       ds=distribution['bgd']['ds'],
                       gammas=distribution['bgd']['gammas'],
                       n_total=N_cn_bgd_test,
                       ks=distribution['bgd']['ks'],
                       sigmas=distribution['bgd']['sigmas']) if d_bgd is None else aerosols(name='bgd',
                                                                                            ds=d_bgd,
                                                                                            gammas=gamma_bgd,
                                                                                            n_total=N_cn_bgd_test,
                                                                                            ks=k_bgd,
                                                                                            sigmas=sigma_bgd)

        _, _, eq_acs_log = arg2000(W, T0, P0, bgd.pyr_dist, accom=accom)

        Nd_estimate = calc_Nd(eq_acs_log, None, bgd, factor=1e6)

        rms_error_Nd = (Nd_desired - Nd_estimate) ** 2

        if rms_error_Nd < rms_error_Nd_min:
            N_cn = N_cn_bgd_test
            rms_error_Nd_min = rms_error_Nd

    return N_cn * 1e6


def find_CN_mbn(Nd_desired, T0, P0, W, distribution, n_iter, d_bgd=None, sigma_bgd=None, k_bgd=None, gamma_bgd=None):
    N_cn_bgd_tests = np.linspace(0.01, 2000, n_iter)
    rms_error_Nd_min = 1e32

    N_cn = 0
    for N_cn_bgd_test in N_cn_bgd_tests:

        bgd = aerosols(name='bgd',
                       ds=distribution['bgd']['ds'],
                       gammas=distribution['bgd']['gammas'],
                       n_total=N_cn_bgd_test,
                       ks=distribution['bgd']['ks'],
                       sigmas=distribution['bgd']['sigmas']) if d_bgd is None else aerosols(name='bgd',
                                                                                            ds=d_bgd,
                                                                                            gammas=gamma_bgd,
                                                                                            n_total=N_cn_bgd_test,
                                                                                            ks=k_bgd,
                                                                                            sigmas=sigma_bgd)

        _, _, eq_acs_log = mbn2014(W, T0, P0, bgd.pyr_dist, accom=accom, xmin=0.05, xmax=0.1, tol=1e-12, max_iters=1000)

        Nd_estimate = calc_Nd(eq_acs_log, None, bgd, factor=1e6)

        rms_error_Nd = (Nd_desired - Nd_estimate) ** 2

        if rms_error_Nd < rms_error_Nd_min:
            N_cn = N_cn_bgd_test
            rms_error_Nd_min = rms_error_Nd

    return N_cn * 1e6

def find_CN_pyrcel(Nd_desired, T0, P0, W, distribution, n_iter, d_bgd=None, sigma_bgd=None, k_bgd=None, gamma_bgd=None):
    N_cn_bgd_tests = np.linspace(0.01, 2000, n_iter)
    rms_error_Nd_min = 1e32
    N_cn = 0
    for N_cn_bgd_test in N_cn_bgd_tests:

        bgd = aerosols(name='bgd',
                       ds=distribution['bgd']['ds'],
                       gammas=distribution['bgd']['gammas'],
                       n_total=N_cn_bgd_test,
                       ks=distribution['bgd']['ks'],
                       sigmas=distribution['bgd']['sigmas'],
                       is_binned=True) if d_bgd is None else aerosols(name='bgd',
                                                                    ds=d_bgd,
                                                                    gammas=gamma_bgd,
                                                                    n_total=N_cn_bgd_test,
                                                                    ks=k_bgd,
                                                                    sigmas=sigma_bgd,
                                                                    is_binned=True)

        dt = 1.0
        t_end = 100. / W  # end time, seconds... 100 meter simulation
        S0 = -0.01
        model = ParcelModel(bgd.pyr_dist, W, T0, S0, P0, console=False, accom=accom)

        parcel_trace, aerosol_traces = model.run(t_end, dt, solver='cvode')

        Smax = parcel_trace['S'].max()

        ind_final = int(t_end / dt) - 1

        T = parcel_trace['T'].iloc[ind_final]

        eq = [None] * 3

        eq[0], _, _, _ = binned_activation(Smax, T, aerosol_traces['bgd0'].iloc[ind_final], bgd.pyr_dist[0])
        eq[1], _, _, _ = binned_activation(Smax, T, aerosol_traces['bgd1'].iloc[ind_final], bgd.pyr_dist[1])
        eq[2], _, _, _ = binned_activation(Smax, T, aerosol_traces['bgd2'].iloc[ind_final], bgd.pyr_dist[2])

        Nd_estimate = calc_Nd(eq, None, bgd, factor=1e6)

        rms_error_Nd = (Nd_desired - Nd_estimate) ** 2

        if rms_error_Nd < rms_error_Nd_min:
            N_cn = N_cn_bgd_test
            rms_error_Nd_min = rms_error_Nd

    return N_cn * 1e6


def arg(N_CN_pol, N_d_bgd, T0, P0, W, invigoration_factor, distribution, N_cn_bgd=None, d_pol=None, d_bgd=None, sigma_pol=None,
               sigma_bgd=None, k_pol=None, k_bgd=None, gamma_pol=None, gamma_bgd=None):

    n_iter = 50

    N_bgd = find_CN_arg(N_d_bgd, T0, P0, W, distribution, n_iter, d_bgd, sigma_bgd, k_bgd,
                        gamma_bgd) if N_cn_bgd is None else N_cn_bgd

    N_CN_total = N_bgd + N_CN_pol

    N_CN_bgd = 1e-6 * N_bgd
    N_CN_pol = 1e-6 * N_CN_pol

    bgd = aerosols(name='bgd',
                   ds=distribution['bgd']['ds'],
                   gammas=distribution['bgd']['gammas'],
                   n_total=N_CN_bgd,
                   ks=distribution['bgd']['ks'],
                   sigmas=distribution['bgd']['sigmas']) if d_bgd is None else aerosols(name='bgd',
                                                                                        ds=d_bgd,
                                                                                        gammas=gamma_bgd,
                                                                                        n_total=N_CN_bgd,
                                                                                        ks=k_bgd,
                                                                                        sigmas=sigma_bgd)

    pol = aerosols(name='pol',
                   ds=distribution['pol']['ds'],
                   gammas=distribution['pol']['gammas'],
                   n_total=N_CN_pol,
                   ks=distribution['pol']['ks'],
                   sigmas=distribution['pol']['sigmas']) if d_pol is None else aerosols(name='pol',
                                                                                        ds=d_pol,
                                                                                        gammas=gamma_pol,
                                                                                        n_total=N_CN_pol,
                                                                                        ks=k_pol,
                                                                                        sigmas=sigma_pol)

    _, _, eq = arg2000(invigoration_factor*W, T0, P0, pol.pyr_dist + bgd.pyr_dist, accom=accom)

    return calc_Nd(eq, pol, bgd, factor=1)


def mbn(N_CN_pol, N_d_bgd, T0, P0, W, invigoration_factor, distribution, N_cn_bgd=None, d_pol=None, d_bgd=None, sigma_pol=None,
               sigma_bgd=None, k_pol=None, k_bgd=None, gamma_pol=None, gamma_bgd=None):

    n_iter = 50
    N_bgd = find_CN_mbn(N_d_bgd, T0, P0, W, distribution, n_iter, d_bgd, sigma_bgd, k_bgd,
                        gamma_bgd) if N_cn_bgd is None else N_cn_bgd

    N_CN_bgd = 1e-6 * N_bgd
    N_CN_pol = 1e-6 * N_CN_pol

    bgd = aerosols(name='bgd',
                   ds=distribution['bgd']['ds'],
                   gammas=distribution['bgd']['gammas'],
                   n_total=N_CN_bgd,
                   ks=distribution['bgd']['ks'],
                   sigmas=distribution['bgd']['sigmas']) if d_bgd is None else aerosols(name='bgd',
                                                                                        ds=d_bgd,
                                                                                        gammas=gamma_bgd,
                                                                                        n_total=N_CN_bgd,
                                                                                        ks=k_bgd,
                                                                                        sigmas=sigma_bgd)

    pol = aerosols(name='pol',
                   ds=distribution['pol']['ds'],
                   gammas=distribution['pol']['gammas'],
                   n_total=N_CN_pol,
                   ks=distribution['pol']['ks'],
                   sigmas=distribution['pol']['sigmas']) if d_pol is None else aerosols(name='pol',
                                                                                        ds=d_pol,
                                                                                        gammas=gamma_pol,
                                                                                        n_total=N_CN_pol,
                                                                                        ks=k_pol,
                                                                                        sigmas=sigma_pol)

    _, _, eq = mbn2014(invigoration_factor*W, T0, P0, pol.pyr_dist + bgd.pyr_dist, accom=accom, xmin=1e-5, xmax=0.1, tol=1e-12, max_iters=10000)


    return calc_Nd(eq, pol, bgd, factor=1)


def pyrcel(N_CN_pol, N_d_bgd, T0, P0, W, invigoration_factor, distribution=size_distribution, S0=-0.01, N_cn_bgd=None, d_pol=None,
                  d_bgd=None, sigma_pol=None, sigma_bgd=None, k_pol=None, k_bgd=None, gamma_pol=None, gamma_bgd=None):
    N_bgd = find_CN_pyrcel(N_d_bgd, T0, P0, W, distribution, n_iter=20)

    N_CN_total = N_bgd + N_CN_pol

    N_CN_bgd = 1e-6 * N_bgd
    N_CN_pol = 1e-6 * N_CN_pol

    bgd = aerosols(name='bgd',
                   ds=distribution['bgd']['ds'],
                   gammas=distribution['bgd']['gammas'],
                   n_total=N_CN_bgd,
                   ks=distribution['bgd']['ks'],
                   sigmas=distribution['bgd']['sigmas'],
                   is_binned=True) if d_bgd is None else aerosols(name='bgd',
                                                                    ds=d_bgd,
                                                                    gammas=gamma_bgd,
                                                                    n_total=N_CN_bgd,
                                                                    ks=k_bgd,
                                                                    sigmas=sigma_bgd,
                                                                    is_binned=True)

    pol = aerosols(name='pol',
                   ds=distribution['pol']['ds'],
                   gammas=distribution['pol']['gammas'],
                   n_total=N_CN_pol,
                   ks=distribution['pol']['ks'],
                   sigmas=distribution['pol']['sigmas'],
                   is_binned=True) if d_pol is None else aerosols(name='pol',
                                                                    ds=d_pol,
                                                                    gammas=gamma_pol,
                                                                    n_total=N_CN_pol,
                                                                    ks=k_pol,
                                                                    sigmas=sigma_pol,
                                                                    is_binned=True)

    dt = 1.0
    t_end = 100. / (invigoration_factor*W)  # end time, seconds... 100 meter simulation

    model = ParcelModel(pol.pyr_dist + bgd.pyr_dist, invigoration_factor*W, T0, S0, P0, console= False, accom=accom)

    parcel_trace, aerosol_traces = model.run(t_end, dt, solver='cvode')

    Smax = parcel_trace['S'].max()
    # Smax = 0.004

    ind_final = int(t_end / dt) - 1

    T = parcel_trace['T'].iloc[ind_final]

    pol_size = len(pol.pyr_dist)
    bgd_size = len(bgd.pyr_dist)

    eq = [None] * (pol_size + bgd_size)

    for i in range(pol_size):
        eq[i], _, _, _ = binned_activation(Smax, T, aerosol_traces['pol' + str(i)].iloc[ind_final], pol.pyr_dist[i])

    for i in range(bgd_size):
        eq[i + pol_size], _, _, _ = binned_activation(Smax, T, aerosol_traces['bgd' + str(i)].iloc[ind_final],
                                                      bgd.pyr_dist[i])

    return calc_Nd(eq, pol, bgd, factor=1)


def pyrcel_lookup(N_CN_pol, N_d_bgd, T0, P0, W, invigoration_factor, distribution, S0=-0.01, N_cn_bgd=None, d_pol=None, d_bgd=None,
                         sigma_pol=None, sigma_bgd=None, k_pol=None, k_bgd=None, gamma_pol=None, gamma_bgd=None):
    # lookuptable = np.load('../data/lookuptable_pool.npy')
    lookuptable = np.load('../data/lookuptable_pool_invigorated.npy')

    nncn = 10
    nndbgd = 10
    nw = 20

    N_cn = np.linspace(0.01,5000e6, nncn)
    Nd_bgd = np.linspace(0.01,2000e6, nndbgd)
    w = np.linspace(0.01,3., nw)

    interp = RegularGridInterpolator((N_cn, Nd_bgd, w), lookuptable, bounds_error=False)
    Nd = interp([N_CN_pol, N_d_bgd, W])

    return Nd[0]


def find_updraft(nd_pol, nd_cln, n_base_pol, T0, P0, distribution, invigoration_factor, expname, get_plot=False):
    n_iter = 100
    w = np.nan
    N_bgd = np.nan
    updraft_temps = np.linspace(0.01, 3., n_iter)
    rms_error_Nd_min = 1e32
    rms_error_Nd_arr = []

    for k in range(n_iter):

        if expname == "bri_arg":
            N_bgd_temp = find_CN_arg(nd_cln, T0, P0, updraft_temps[k], distribution, n_iter=50)
        else:
            N_bgd_temp = find_CN_mbn(nd_cln, T0, P0, updraft_temps[k], distribution, n_iter=50)

        N_CN_bgd = 1e-6 * N_bgd_temp
        N_CN_pol = 1e-6 * n_base_pol

        bgd = aerosols(name='bgd',
                       ds=distribution['bgd']['ds'],
                       gammas=distribution['bgd']['gammas'],
                       n_total=N_CN_bgd,
                       ks=distribution['bgd']['ks'],
                       sigmas=distribution['bgd']['sigmas'])

        pol = aerosols(name='pol',
                       ds=distribution['pol']['ds'],
                       gammas=distribution['pol']['gammas'],
                       n_total=N_CN_pol,
                       ks=distribution['pol']['ks'],
                       sigmas=distribution['pol']['sigmas'])

        Nd_estimate = 0

        if expname == "bri_arg":
            _, _, eq = arg2000(invigoration_factor*updraft_temps[k], T0, P0, pol.pyr_dist + bgd.pyr_dist, accom=accom)

            Nd_estimate = calc_Nd(eq, pol, bgd, factor=1e6)


        elif expname == "bri_mbn":
            _, _, eq = mbn2014(invigoration_factor*updraft_temps[k], T0, P0, pol.pyr_dist + bgd.pyr_dist, accom=accom)

            Nd_estimate = calc_Nd(eq, pol, bgd, factor=1e6)


        elif expname == "bri_pyrcel":
            bgd = aerosols(name='bgd',
                ds=distribution['bgd']['ds'],
                gammas=distribution['bgd']['gammas'],
                n_total=N_CN_bgd,
                ks=distribution['bgd']['ks'],
                sigmas=distribution['bgd']['sigmas'],
                is_binned=True)

            pol = aerosols(name='pol',
                        ds=distribution['pol']['ds'],
                        gammas=distribution['pol']['gammas'],
                        n_total=N_CN_pol,
                        ks=distribution['pol']['ks'],
                        sigmas=distribution['pol']['sigmas'],
                        is_binned=True)
        
            dt = 1.0
            t_end = 100. / (invigoration_factor*updraft_temps[k]) # end time, seconds... 100 meter simulation
            model = ParcelModel(pol.pyr_dist + bgd.pyr_dist, invigoration_factor*updraft_temps[k], T0, -0.01, P0, console=False,
                                accom=accom)

            parcel_trace, aerosol_traces = model.run(t_end, dt, solver='cvode')

            Smax = parcel_trace['S'].max()

            ind_final = int(t_end / dt) - 1

            T = parcel_trace['T'].iloc[ind_final]

            pol_size = len(pol.pyr_dist)
            bgd_size = len(bgd.pyr_dist)

            eq = [None] * (pol_size + bgd_size)

            for i in range(pol_size):
                eq[i], _, _, _ = binned_activation(Smax, T, aerosol_traces['pol' + str(i)].iloc[ind_final],
                                                   pol.pyr_dist[i])

            for i in range(bgd_size):
                eq[i + pol_size], _, _, _ = binned_activation(Smax, T, aerosol_traces['bgd' + str(i)].iloc[ind_final],
                                                              bgd.pyr_dist[i])

            Nd_estimate = calc_Nd(eq, pol, bgd, factor=1)


        elif expname == "bri_lkup":
            Nd_estimate = 1e6 * pyrcel_lookup(1e6 * N_CN_pol, nd_cln, T0, P0, W=updraft_temps[k], invigoration_factor=invigoration_factor, distribution = pol.pyr_dist + bgd.pyr_dist, S0=-0.01)
        else:
            raise Exception(f"{expname} is not one of the accepted options for expname.")

        rms_error_Nd = (nd_pol - Nd_estimate) ** 2
        rms_error_Nd_arr.append(rms_error_Nd)


        if rms_error_Nd < rms_error_Nd_min:
            w = updraft_temps[k]
            N_bgd = N_bgd_temp
            rms_error_Nd_min = rms_error_Nd

    if get_plot == True:
        return w, 1e-6 * N_bgd, invigoration_factor*updraft_temps, rms_error_Nd_arr

    return w, 1e-6 * N_bgd
