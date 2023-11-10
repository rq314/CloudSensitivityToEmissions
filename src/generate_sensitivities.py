from parcel_models import arg, mbn, pyrcel_lookup
from plume_models import briggs_approx
import numpy as np
import pandas as pd
from aerosols import size_distribution


def generate_sensitivities(ship_df=None):
    if ship_df is None:
        ship_df = pd.read_csv("../data/processed/all_ships/ships_dataframe_processed_bri_arg.csv")

    T0 = ship_df['t1000'].mean()
    P0 = 101300
    updraft_in = 0.3
    U_rel = ship_df['spd_res'].mean()
    M_dot = ship_df['sox'].mean()
    beta = 0.6
    nd_cln = ship_df['nd_cln'].mean()

    h_cbh = ship_df['cbh'].mean()

    h_blh = ship_df['blh'].mean()


    invigoration_factor = 1.0

    print(f"Nominal value: {M_dot,U_rel, h_cbh, nd_cln}")
    print(f"Uncertainty: {ship_df['sox'].std(), ship_df['spd_res'].std(), ship_df['cbh'].loc[ship_df['cbh']>0].std(), ship_df['nd_cln'].std()}")

    h = h_cbh
    T = T0 - 0.0098 * h
    P = P0 - 1.226 * 9.81 * h

    exp = 'acruise'
    print("distribution: " + exp)

    d_pol_ais = size_distribution["pol"]['ds'][0]

    d_bgd_ais = size_distribution["bgd"]['ds'][0]
    d_bgd_acs = size_distribution["bgd"]['ds'][1]
    d_bgd_cos = size_distribution["bgd"]['ds'][2]

    k_pol = size_distribution["pol"]['ks'][0]
    k_bgd = size_distribution["bgd"]['ks'][0]

    sigma_pol = size_distribution["pol"]['sigmas'][0]
    sigma_bgd = size_distribution["bgd"]['sigmas'][0]

    gamma_pol_ais = size_distribution["pol"]['gammas'][0]

    gamma_bgd_ais = size_distribution["bgd"]['gammas'][0]
    gamma_bgd_acs = size_distribution["bgd"]['gammas'][1]
    gamma_bgd_cos = size_distribution["bgd"]['gammas'][2]

    imdot = 0
    iurel = 1
    ihcbh = 2
    indcln = 3
    iw = 4
    idpolais = 5
    idbgdais = 6
    idbgdacs = 7
    idbgdcos = 8
    ikpol = 9
    ikbgd = 10
    isigpol = 11
    isigbgd = 12
    ibeta = 13
    ihblh = 14


    sens_vars = [M_dot,
                 U_rel,
                 h_cbh,
                 nd_cln,
                 updraft_in,
                 d_pol_ais,
                 d_bgd_ais,
                 d_bgd_acs,
                 d_bgd_cos,
                 k_pol,
                 k_bgd,
                 sigma_pol,
                 sigma_bgd,
                 beta,
                 h_blh]

    uncertainties_absolute = [None, ship_df['spd_res'].std(), ship_df['cbh'].std(), ship_df['nd_cln'].std(), None, 0.02e-3, 0.02, 0.02e-3, 0.02, None, 0.19, 0.21, 0.02, 0.02, None]
    uncertainties_perc = [0.14, 0.2, 0.1, 0.1, 1.9, 0.08, 2.0, 2.0, 2.0, 0.5, 0.5, 0.09, 2.0, 0.83, 0.2]

    # We choose to favour the absolute uncertainties for the parameters that we do not have a good estimate for
    uncertainties = []
    uncertainties_perc_corrected = []
    for ae, pe, n in zip(uncertainties_absolute, uncertainties_perc, sens_vars):
        print(ae, pe)
        if pe is not None:
            uncertainties.append(pe * n)
            uncertainties_perc_corrected.append(100*pe)
        else:
            uncertainties.append(ae)
            uncertainties_perc_corrected.append(100*ae / n)

    sensitivities_arg = np.zeros(len(sens_vars))
    sensitivities_mbn = np.zeros(len(sens_vars))
    sensitivities_pyr = np.zeros(len(sens_vars))
    sensitivities_lkup = np.zeros(len(sens_vars))

    depsilon_dp_arg = np.zeros(len(sens_vars))
    depsilon_dp_mbn = np.zeros(len(sens_vars))
    depsilon_dp_pyr = np.zeros(len(sens_vars))
    depsilon_dp_lkup = np.zeros(len(sens_vars))

    for i in range(len(sens_vars)):

        d_pols = [sens_vars[idpolais]]
        d_bgds = [sens_vars[idbgdais], sens_vars[idbgdacs], sens_vars[idbgdcos]]
        k_pols = [sens_vars[ikpol]]
        k_bgds = [sens_vars[ikbgd], sens_vars[ikbgd], sens_vars[ikbgd]]
        sigma_pols = [sens_vars[isigpol]]
        sigma_bgds = [sens_vars[isigbgd], sens_vars[isigbgd], sens_vars[isigbgd]]
        gamma_pols = [gamma_pol_ais]
        gamma_bgds = [gamma_bgd_ais, gamma_bgd_acs, gamma_bgd_cos]

        n_base_pol_in = briggs_approx(sens_vars[ihcbh], sens_vars[iurel], sens_vars[imdot], beta=beta,
                                      d_s=sens_vars[idpolais], sigma=sens_vars[isigpol])

        Nd_pol_arg = arg(1e6 * n_base_pol_in, 1e6 * sens_vars[indcln], T, P0=P, W=sens_vars[iw], invigoration_factor=invigoration_factor,
                                distribution=size_distribution, d_pol=d_pols, d_bgd=d_bgds, sigma_pol=sigma_pols,
                                sigma_bgd=sigma_bgds, k_pol=k_pols, k_bgd=k_bgds, gamma_pol=gamma_pols,
                                gamma_bgd=gamma_bgds)
        Nd_pol_mbn = mbn(1e6 * n_base_pol_in, 1e6 * sens_vars[indcln], T, P0=P, W=sens_vars[iw], invigoration_factor=invigoration_factor,
                                distribution=size_distribution, d_pol=d_pols, d_bgd=d_bgds, sigma_pol=sigma_pols,
                                sigma_bgd=sigma_bgds, k_pol=k_pols, k_bgd=k_bgds, gamma_pol=gamma_pols,
                                gamma_bgd=gamma_bgds)
        Nd_pol_lkup = pyrcel_lookup(1e6 * n_base_pol_in, 1e6 * sens_vars[indcln], T, P0=P, W=sens_vars[iw], invigoration_factor=invigoration_factor,
                                           distribution=size_distribution, d_pol=d_pols, d_bgd=d_bgds, sigma_pol=sigma_pols,
                                           sigma_bgd=sigma_bgds, k_pol=k_pols, k_bgd=k_bgds, gamma_pol=gamma_pols,
                                           gamma_bgd=gamma_bgds)

        enhancement_arg = Nd_pol_arg / sens_vars[indcln]
        enhancement_mbn = Nd_pol_mbn / sens_vars[indcln]
        enhancement_lkup = Nd_pol_lkup / sens_vars[indcln]

        # Change to parameter

        sens_vars[i] *= 1.05

        # Repopulate distribution arrays in case they changed
        d_pols = [sens_vars[idpolais]]
        d_bgds = [sens_vars[idbgdais], sens_vars[idbgdacs], sens_vars[idbgdcos]]
        k_pols = [sens_vars[ikpol]]
        k_bgds = [sens_vars[ikbgd], sens_vars[ikbgd], sens_vars[ikbgd]]
        sigma_pols = [sens_vars[isigpol]]
        sigma_bgds = [sens_vars[isigbgd], sens_vars[isigbgd], sens_vars[isigbgd]]
        gamma_pols = [gamma_pol_ais]
        gamma_bgds = [gamma_bgd_ais, gamma_bgd_acs, gamma_bgd_cos]

        n_base_pol_in_new = briggs_approx(sens_vars[ihcbh], sens_vars[iurel], sens_vars[imdot], beta=beta,
                                          d_s=sens_vars[idpolais], sigma=sens_vars[isigpol])

        Nd_pol_arg_new = arg(1e6 * n_base_pol_in_new, 1e6 * sens_vars[indcln], T, P0=P, W=sens_vars[iw], invigoration_factor=invigoration_factor,
                                    distribution=size_distribution, d_pol=d_pols, d_bgd=d_bgds, sigma_pol=sigma_pols,
                                    sigma_bgd=sigma_bgds, k_pol=k_pols, k_bgd=k_bgds, gamma_pol=gamma_pols,
                                    gamma_bgd=gamma_bgds)
        Nd_pol_mbn_new = mbn(1e6 * n_base_pol_in_new, 1e6 * sens_vars[indcln], T, P0=P, W=sens_vars[iw], invigoration_factor=invigoration_factor,
                                    distribution=size_distribution, d_pol=d_pols, d_bgd=d_bgds, sigma_pol=sigma_pols,
                                    sigma_bgd=sigma_bgds, k_pol=k_pols, k_bgd=k_bgds, gamma_pol=gamma_pols,
                                    gamma_bgd=gamma_bgds)
        Nd_pol_lkup_new = pyrcel_lookup(1e6 * n_base_pol_in_new, 1e6 * sens_vars[indcln], T, P0=P,
                                               W=sens_vars[iw],  invigoration_factor=invigoration_factor, distribution=size_distribution, d_pol=d_pols, d_bgd=d_bgds,
                                               sigma_pol=sigma_pols, sigma_bgd=sigma_bgds, k_pol=k_pols, k_bgd=k_bgds,
                                               gamma_pol=gamma_pols, gamma_bgd=gamma_bgds)

        enhancement_arg_new = Nd_pol_arg_new / sens_vars[indcln]
        enhancement_mbn_new = Nd_pol_mbn_new / sens_vars[indcln]
        enhancement_lkup_new = Nd_pol_lkup_new / sens_vars[indcln]

        depsilon_dp_arg[i] = (enhancement_arg_new - enhancement_arg) / ((sens_vars[i] - (sens_vars[i] / 1.05)))
        depsilon_dp_mbn[i] = (enhancement_mbn_new - enhancement_mbn) / ((sens_vars[i] - (sens_vars[i] / 1.05)))
        depsilon_dp_lkup[i] = (enhancement_lkup_new - enhancement_lkup) / ((sens_vars[i] - (sens_vars[i] / 1.05)))

        sensitivities_arg[i] = uncertainties[i] * depsilon_dp_arg[i]
        sensitivities_mbn[i] = uncertainties[i] * depsilon_dp_mbn[i]
        sensitivities_lkup[i] = uncertainties[i] * depsilon_dp_lkup[i]

        print(sensitivities_arg[i], sensitivities_mbn[i], sensitivities_pyr[i])
        sens_vars[i] /= 1.05

    sensitivities = np.array(
        [sens_vars,
         list(sensitivities_arg),
         list(sensitivities_mbn), 
         list(sensitivities_lkup), 
         list(depsilon_dp_arg),
         list(depsilon_dp_mbn),
         list(depsilon_dp_lkup),
         list(uncertainties), 
         list(uncertainties_perc_corrected)]).T

    out_df = pd.DataFrame(sensitivities, columns=['nominal','sens_arg', 'sens_mbn', 'sens_lkup','depsilon_dp_arg','depsilon_dp_mbn','depsilon_dp_lkup','Deltap', 'Deltap_perc'])

    datadir = '../data/'

    out_df.to_csv(datadir + "sensitivity_" + exp + ".csv")

if __name__ == '__main__':
    generate_sensitivities()
