from plot_coupled_correlations import plot_coupled_correlations
from plot_updrafts_boxplot import plot_updrafts_boxplot
from plot_sensitivitystudy import plot_sensitivitystudy
from plot_limited_regimes import plot_limited_regimes

import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np

def generate_all_plots():
    paper_figures_dir = '../figs/'
    nbins = 20

    mpl.rcParams.update(mpl.rcParamsDefault)
    plt.rcParams['text.usetex'] = True

    datadir_only_tracks = '../data/processed/only_tracks/'
    datadir_all_ships = '../data/processed/all_ships/'
    datadir_sensitivity = '../data/'

    filename_arg_tracks = 'only_tracks_dataframe_processed_bri_arg.csv'
    filename_mbn_tracks = 'only_tracks_dataframe_processed_bri_mbn.csv'
    filename_lkup_tracks = 'only_tracks_dataframe_processed_bri_lkup.csv'

    # Commented out as we only include the track data. As we've purchased ship data from a commercial source, we are unable to provide the complete dataset.
    #  However, we've obtained permission to share emission rates for the analyzed tracks in this study.

    # filename_arg_ships = 'ships_dataframe_processed_bri_arg.csv'
    # filename_mbn_ships = 'ships_dataframe_processed_bri_mbn.csv'
    # filename_lkup_ships = 'ships_dataframe_processed_bri_lkup.csv'

    filename_sensitivity = "sensitivity_" + "acruise" + ".csv"

    track_arg_df = pd.read_csv(datadir_only_tracks + filename_arg_tracks)
    track_mbn_df = pd.read_csv(datadir_only_tracks + filename_mbn_tracks)
    track_lkup_df = pd.read_csv(datadir_only_tracks + filename_lkup_tracks)

    # Commented out as we only include the track data. As we've purchased ship data from a commercial source, we are unable to provide the complete dataset.
    #  However, we've obtained permission to share emission rates for the analyzed tracks in this study.

    # ships_arg_df = pd.read_csv(datadir_all_ships + filename_arg_ships)
    # ships_mbn_df = pd.read_csv(datadir_all_ships + filename_mbn_ships)
    # ships_lkup_df = pd.read_csv(datadir_all_ships + filename_lkup_ships)


    sens_df = pd.read_csv(datadir_sensitivity + filename_sensitivity)

    legend_labels = ['ARG', 'MBN', 'RW']
    colors = [(196 / 255, 121 / 255, 0 / 255), (112 / 255, 160 / 255, 205 / 255), (0/255, 79/255, 0/255)]

    plot_coupled_correlations(paper_figures_dir,
                        [track_arg_df,
                        track_mbn_df,
                        track_lkup_df],
                        legend_labels,
                        colors,
                        plot_title="",
                        fontsize=14)

    plot_updrafts_boxplot(paper_figures_dir,
                    [track_arg_df,
                    track_mbn_df,
                    track_lkup_df],
                    legend_labels,
                    colors,
                    nbins,
                    plot_title="",
                    fontsize=14,
                    linewidth=2)

    # Commented out as we only include the track data. As we've purchased ship data from a commercial source, we are unable to provide the complete dataset.
    #  However, we've obtained permission to share emission rates for the analyzed tracks in this study.

    # plot_limited_regimes(paper_figures_dir,
    #                              [track_arg_df,
    #                               track_mbn_df,
    #                               track_lkup_df],
    #                              [ships_arg_df.loc[ships_arg_df['trackno']<=0],
    #                               ships_mbn_df.loc[ships_mbn_df['trackno']<=0],
    #                               ships_lkup_df.loc[ships_lkup_df['trackno']<=0]],
    #                              "all",
    #                              colors,
    #                              fontsize=14,
    #                              linewidth=2)

    plot_sensitivitystudy(paper_figures_dir, sens_df, "invigorated", fontsize=14, linewidth=2)

if __name__ == '__main__':
    generate_all_plots()