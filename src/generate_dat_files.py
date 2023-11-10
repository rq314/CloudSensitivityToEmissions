import argparse
import numpy as np
from process_database import pre_process_database, post_process_database
from parcel_models import arg, pyrcel, mbn, pyrcel_lookup
from plume_models import briggs_approx
import pandas as pd
from aerosols import size_distribution
import multiprocessing as mp
import cloud_relationships
import generate_sensitivities


def parse_args():
    parser = argparse.ArgumentParser(description="Command line arguments to generate datafiles",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-e", "--exp", help="Experiment name")
    parser.add_argument("--dist", help="Aerosol distribution type")
    parser.add_argument("--procs", action='store_true', help="Flag to process ship database")
    parser.add_argument("--proct", action='store_true', help="Flag to process track database")
    parser.add_argument("--figdir", help="Figures output location")
    parser.add_argument("--datadir", help="Data directory location")

    parser.add_argument("--ncores", type=int, help="Number of cores")

    parser.add_argument("--track_dist", type=float, help="Distance from track")
    parser.add_argument("--blh", type=float, help="Cloud height mask")
    parser.add_argument("--ures", type=float, help="Relative velocity mask")
    parser.add_argument("--ndcln", type=float, help="Background droplet concentration mask")
    parser.add_argument("--cf", type=float, help="Cloud fraction mask")
    parser.add_argument("--reff", type=float, help="Effective radius mask")
    parser.add_argument("--detect", type=float, help="Dectection limit")

    args = parser.parse_args()
    config = vars(args)
    return config


def process_all_ships(queue,
                      ship_raw_dataframe,
                      exp,
                      distribution,
                      get_aerosol_conc_func,
                      get_nd_track_func,
                      expected_obs_mask,
                      process_id):
    pre_processed_dataframe = pre_process_database(ship_raw_dataframe['trackno'],
                                                   ship_raw_dataframe['sox'],
                                                   ship_raw_dataframe['blh'],
                                                   ship_raw_dataframe['cth'],
                                                   ship_raw_dataframe['spd_res'],
                                                   ship_raw_dataframe['nd_cln'],
                                                   None,
                                                   ship_raw_dataframe['cf_liq'],
                                                   ship_raw_dataframe['lwp'],
                                                   ship_raw_dataframe['t1000'],
                                                   ship_raw_dataframe['LTS'],
                                                   ship_raw_dataframe['ctt'],
                                                   ship_raw_dataframe['ctrc'],
                                                   ship_raw_dataframe['is_coupled'],
                                                   is_all_ships_data=True
                                                   )

    ships_dataframe_processed, tracks_dataframe_processed, falsenegative_dataframe_processed = post_process_database(
        pre_processed_dataframe,
        get_aerosol_conc_func,
        get_nd_track_func,
        expected_obs_mask,
        distribution=distribution,
        expname=exp,
        is_all_ships_data=True)

    print(f"Data files generated for 'all-ships' dir{process_id}")

    return queue.put([ships_dataframe_processed, tracks_dataframe_processed, falsenegative_dataframe_processed])


def process_only_track_properties(queue,
                                  merged,
                                  exp,
                                  distribution,
                                  get_aerosol_conc_func,
                                  get_nd_track_func,
                                  process_id):

    pre_processed_dataframe = pre_process_database(merged['trackno'],
                                                   merged['sox'],
                                                   merged['blh'],
                                                   merged["cth"],
                                                   merged['spd_res'],
                                                   merged['nd_cln'],
                                                   merged['nd_pol'],
                                                   merged['cf_liq'],
                                                   merged['lwp'],
                                                   merged['t1000'],
                                                   merged['LTS'],
                                                   merged['ctt'],
                                                   merged['ctrc'],
                                                   merged['is_coupled'],
                                                   is_all_ships_data=False
                                                   )
    ships_dataframe_processed, \
        tracks_dataframe_processed, \
        _, = post_process_database(pre_processed_dataframe,
                                   get_aerosol_conc_func,
                                   get_nd_track_func,
                                   0,
                                   distribution=distribution,
                                   expname=exp,
                                   is_all_ships_data=False)

    queue.put([tracks_dataframe_processed])
                                                            

def generate_dat_files():
    config = parse_args()

    expected_obs_mask = 1.2 if config['detect'] == None else config['detect']
    n_cores = 1 if config['ncores'] == None else config['ncores']
    process_ship = False if config['procs'] == None else config['procs']
    process_track = False if config['proct'] == None else config['proct']

    exp_key = 'bri_arg' if config['exp'] == None else config['exp']
    dist_key = "acruise" if config['dist'] == None else config['dist']
    raw_dir = '../data/raw/' if config['datadir'] == None else config['datadir']
    proc_dir = '../data/processed'

    fname_ships_raw_data = raw_dir + 'all_ships_data_ctrc_anonymous.csv'
    fname_track_raw_data = raw_dir + 'only_track_data_ctrc_anonymous.csv'

    exp = {
        'bri_arg': [briggs_approx, arg],
        'bri_mbn': [briggs_approx, mbn],
        'bri_lkup': [briggs_approx, pyrcel_lookup],
    }

    aero_dist = {
        'acruise': size_distribution
    }
    print('Running the following case: ' + exp_key + " distribution: " + dist_key)


    processes = []
    rets = []

    if process_ship is True:
        anonymous_ships = pd.read_csv(fname_ships_raw_data, index_col=0)
        merged_ships_filtered_split = np.array_split(anonymous_ships, n_cores)

        queue = mp.Queue()
        for p_index, sdf in enumerate(merged_ships_filtered_split):
            processes.append(mp.Process(target=process_all_ships, args=(queue,
                                                                        sdf,
                                                                        exp_key,
                                                                        aero_dist[dist_key],
                                                                        exp[exp_key][0],
                                                                        exp[exp_key][1],
                                                                        expected_obs_mask,
                                                                        p_index)))
        for p in processes:
            p.start()
            print(f'Starting process: {p}')
        for p in processes:
            ret = queue.get()  # will block
            rets.append(ret)
        for p in processes:
            p.join()
        print("processes finished")
        print(rets)

        resultant_dfs = pd.DataFrame()
        corrs_dfs = pd.DataFrame()
        tpos_dfs = pd.DataFrame()
        fnegs_dfs = pd.DataFrame()

        for index, r in enumerate(rets):
            resultant_dfs = pd.concat([resultant_dfs, r[0]])
            tpos_dfs = pd.concat([tpos_dfs, r[1]])
            fnegs_dfs = pd.concat([fnegs_dfs, r[2]])

        print(f'Ship data length: {len(resultant_dfs)}')

        resultant_dfs.to_csv(f'{proc_dir}/all_ships/ships_dataframe_processed_{exp_key}.csv')
        generate_sensitivities.generate_sensitivities(resultant_dfs)

    if process_track is True:

        anonymous_tracks = pd.read_csv(fname_track_raw_data, index_col=0)
        merged_tracks_filtered_split = np.array_split(anonymous_tracks, n_cores)
        
        queue = mp.Queue()
        for p_index, tdf in enumerate(merged_tracks_filtered_split):
            processes.append(mp.Process(target=process_only_track_properties, args=(queue,
                                                                                    tdf,
                                                                                    exp_key,
                                                                                    aero_dist[dist_key],
                                                                                    exp[exp_key][0],
                                                                                    exp[exp_key][1],
                                                                                    p_index)))
        for p in processes:
            results = p.start()
            print(f'Starting process: {p}')
        for p in processes:
            ret = queue.get()  # will block
            rets.append(ret)
        for p in processes:
            p.join()
        print("processes finished")
        print(rets)
        resultant_dfs = pd.DataFrame()
        corrs_dfs = pd.DataFrame()

        for index, r in enumerate(rets):
            resultant_dfs = pd.concat([resultant_dfs, r[0]])

        print(f'Track data length: {len(resultant_dfs)}')
        resultant_dfs.to_csv(f'{proc_dir}/only_tracks/only_tracks_dataframe_processed_{exp_key}.csv')
        corrs_dfs.to_csv(f'{proc_dir}/only_tracks/correlations_{exp_key}.csv')

if __name__ == '__main__':
    generate_dat_files()
