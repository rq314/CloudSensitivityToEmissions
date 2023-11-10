import pandas as pd
import numpy as np
from plume_models import briggs_approx
from parcel_models import find_updraft, find_CN_arg, find_CN_mbn
from cloud_relationships import thickness, updraft
from pysolar.solar import *
from tqdm import tqdm


def pre_process_database(trackno,
                         soxs,
                         blhs,
                         cths,
                         spd_res,
                         nd_clns,
                         nd_pols,
                         cf_liqs,
                         lwps,
                         t1000s,
                         ltss,
                         ctts,
                         ctrcs,
                         is_coupled,
                         is_all_ships_data=True):
    data = {}
    
    data['trackno'] = trackno.reset_index(drop=True)
    data['sox'] = soxs.reset_index(drop=True)
    data['blh'] = blhs.reset_index(drop=True)
    data['cth'] = cths.reset_index(drop=True)
    data['LTS']=ltss.reset_index(drop=True)
    data['spd_res'] = spd_res.reset_index(drop=True)
    data['nd_cln'] = nd_clns.reset_index(drop=True)
    data['nd_pol'] = nd_pols.reset_index(drop=True) if (nd_pols is not None) else nd_clns.reset_index(drop=True)
    data['cf_liq'] = cf_liqs.reset_index(drop=True)
    data['lwp'] = lwps.reset_index(drop=True)
    data['t1000'] = t1000s.reset_index(drop=True)
    data['ctt'] = ctts.reset_index(drop=True)
    data['ctrc'] = ctrcs.reset_index(drop=True)
    data["thickness"] = [thickness(lwp) for lwp in data['lwp']]
    data["cbh"] = data["cth"] - data["thickness"]
    data['is_coupled'] = is_coupled.reset_index(drop=True)

    df = pd.DataFrame(data)

    return df

def post_process_database(dataframe,
                          get_aerosol_conc_func,
                          get_nd_track_func,
                          expected_obs_mask,
                          distribution,
                          expname,
                          is_all_ships_data=False
                          ):
    tqdm.pandas()

    df = dataframe

    df['updraft_ctrc'] = df.apply(
        lambda x: updraft(x['ctrc'], x['cbh'], x['LTS'], x['is_coupled'])
        , axis=1)

    print('Starting N_base_analytical...')

    if expname == "bri_arg" or expname == "bri_mbn" or expname == "bri_lkup":
        df['N_base_analytical'] = df.apply(
            lambda x: briggs_approx(H=x["cbh"],
                                    U_rel=x["spd_res"],
                                    M_dot=x["sox"],
                                    d_s=distribution['pol']['ds'][0],
                                    sigma=distribution['pol']['sigmas'][0]), axis=1)

    else:
        raise Exception(f"{expname} is not one of the accepted options for expname.")

    invigoration_factor = 1.0
    if is_all_ships_data is False:

        df['optimised'] = df.progress_apply(
            lambda x: find_updraft(
                1E6 * x["nd_pol"],
                1E6 * x["nd_cln"],
                1E6 * x["N_base_analytical"],
                x["t1000"] - 0.0098 * x["cbh"],
                P0=101300 - 1.226 * 9.81 * x["cbh"],
                distribution=distribution,
                invigoration_factor=invigoration_factor,
                expname=expname)
            , axis=1)

        df[['updraft', 'n_cn_bgd']] = pd.DataFrame(df['optimised'].tolist(),
                                                   index=df.index)

        df['nd_pol_param_fit'] = df.apply(
            lambda x: get_nd_track_func(
                1E6 * x['N_base_analytical'],
                1E6 * x["nd_cln"],
                x["t1000"] - 0.0098 * x["cbh"],
                P0=101300 - 1.226 * 9.81 * x["cbh"],
                W=x['updraft'],
                invigoration_factor=invigoration_factor,
                distribution=distribution,
                N_cn_bgd=1E6 * x['n_cn_bgd'])
            , axis=1)

        df['epsilon_param_fit'] = df.apply(
            lambda x: (x["nd_pol_param_fit"]) / x["nd_cln"] if x["nd_cln"] > 0 else np.nan, axis=1)

    else:
        df['optimised'] = df.progress_apply(
            lambda x: find_updraft(
                1E6 * 1.2 * x["nd_cln"],
                1E6 * x["nd_cln"],
                1E6 * x["N_base_analytical"],
                x["t1000"] - 0.0098 * x["cbh"],
                P0=101300 - 1.226 * 9.81 * x["cbh"],
                distribution=distribution,
                invigoration_factor=invigoration_factor,
                expname=expname)
            , axis=1)

        df[['updraft', 'n_cn_bgd']] = pd.DataFrame(df['optimised'].tolist(),
                                                           index=df.index)

        df['nd_pol_param_fit'] = df.apply(
            lambda x: get_nd_track_func(
                1E6 * x['N_base_analytical'],
                1E6 * x["nd_cln"],
                x["t1000"] - 0.0098 * x["cbh"],
                P0=101300 - 1.226 * 9.81 * x["cbh"],
                W=x['updraft'],
                invigoration_factor=invigoration_factor,
                distribution=distribution,
                N_cn_bgd=1E6 * x['n_cn_bgd'])
            , axis=1)

        df['epsilon_param_fit'] = df.apply(
            lambda x: (x["nd_pol_param_fit"]) / x["nd_cln"] if x["nd_cln"] > 0 else np.nan, axis=1)

    print('Starting nd_pol_param...')

    df['nd_pol_param'] = df.apply(
        lambda x: get_nd_track_func(
            1E6 * x['N_base_analytical'],
            1E6 * x["nd_cln"],
            x["t1000"] - 0.0098 * x["cbh"],
            P0=101300 - 1.226 * 9.81 * x["cbh"],
            W=0.3,
            invigoration_factor=invigoration_factor,
            distribution=distribution)
        , axis=1)

    df['nd_pol_param_ctrc'] = df.apply(
    lambda x: get_nd_track_func(
        1E6 * x['N_base_analytical'],
        1E6 * x["nd_cln"],
        x["t1000"] - 0.0098 * x["cbh"],
        P0=101300 - 1.226 * 9.81 * x["cbh"],
        W=x['updraft_ctrc'],
        invigoration_factor=invigoration_factor,
        distribution=distribution)
    , axis=1)
    
    print("Starting updraft-limited classification:")

    if expname == "bri_arg":
        df['n_cn_bgd_ctrc'] = df.apply(
            lambda x: 1e-6 * find_CN_arg(1E6 * x["nd_cln"],
                                  x["t1000"] - 0.0098 * x["cbh"],
                                  101300 - 1.226 * 9.81 * x["cbh"],
                                  x['updraft_ctrc'],
                                  distribution,
                                  n_iter=100), axis=1)

    elif expname == "bri_mbn":
        df['n_cn_bgd_ctrc'] = df.apply(
            lambda x: 1e-6 * find_CN_mbn(1E6 * x["nd_cln"],
                                  x["t1000"] - 0.0098 * x["cbh"],
                                  101300 - 1.226 * 9.81 * x["cbh"],
                                  x['updraft_ctrc'],
                                  distribution,
                                  n_iter=100), axis=1)

    elif expname == "bri_lkup":
        df['n_cn_bgd_ctrc'] = df.apply(
            lambda x: 1e-6 * find_CN_arg(1E6 * x["nd_cln"],
                                  x["t1000"] - 0.0098 * x["cbh"],
                                  101300 - 1.226 * 9.81 * x["cbh"],
                                  x['updraft_ctrc'],
                                  distribution,
                                  n_iter=100), axis=1)

    print('Starting diffs...')

    df['diff_nd_param'] = df.apply(
        lambda x: (x["nd_pol_param"] - x["nd_cln"]) / x["nd_cln"] if x["nd_cln"] > 0 else np.nan, axis=1)

    df['diff_nd_obs'] = df.apply(
        lambda x: (x["nd_pol"] - x["nd_cln"]) / x["nd_cln"] if x["nd_cln"] > 0 else np.nan, axis=1)

    df['epsilon_param'] = df.apply(
        lambda x: (x["nd_pol_param"]) / x["nd_cln"] if x["nd_cln"] > 0 else np.nan, axis=1)
    
    df['epsilon_param_ctrc'] = df.apply(
        lambda x: (x["nd_pol_param_ctrc"]) / x["nd_cln"] if x["nd_cln"] > 0 else np.nan, axis=1)

    df['epsilon_obs'] = df.apply(
        lambda x: (x["nd_pol"]) / x["nd_cln"] if x["nd_cln"] > 0 else np.nan, axis=1)

    shiptrack_df = df

    falsenegative_df = df.loc[(df["epsilon_param"] > expected_obs_mask)]

    return df, \
        shiptrack_df, \
        falsenegative_df

