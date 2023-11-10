import numpy as np
import pandas as pd
import seaborn as sns
from named_variables import *
import helpers
import matplotlib.pyplot as plt


def plot_fname(figures_dir, experiment_name, name_after_experiment):
    return figures_dir + experiment_name + '_' + name_after_experiment + '.pdf'


def plot_limited_regimes(paper_figures_dir, tdfs, sdfs, fname_next, colors, fontsize, linewidth=2):

    helpers.check_sizes_are_consistent([tdfs, sdfs, colors])

    plot_identifiers = [['(a)','(b)'],['(c)','(d)'],['(e)','(f)'],['(g)','(h)']]

    ships_updraft_ctrc = [None]*len(tdfs)
    track_updraft_ctrc = [None]*len(tdfs)
    ships_updraft_kohler = [None]*len(tdfs)
    track_updraft_kohler = [None]*len(tdfs)


    for idf in range(len(tdfs)):

        sdfs[idf]['N_tot_ctrc'] = sdfs[idf]['n_cn_bgd_ctrc']
        tdfs[idf]['N_tot_ctrc'] = tdfs[idf]['n_cn_bgd_ctrc']

        sdfs[idf]['N_tot_koh'] = sdfs[idf]['n_cn_bgd']
        tdfs[idf]['N_tot_koh'] = tdfs[idf]['n_cn_bgd']

        ships_updraft_ctrc[idf] = sdfs[idf][['updraft_ctrc', 'N_tot_ctrc', "N_base_analytical"]].dropna()
        track_updraft_ctrc[idf] = tdfs[idf][['updraft_ctrc', 'N_tot_ctrc', "N_base_analytical"]].dropna()

        ships_updraft_kohler[idf] = sdfs[idf][['updraft', 'N_tot_koh', "N_base_analytical"]].dropna()
        track_updraft_kohler[idf] = tdfs[idf][['updraft', 'N_tot_koh', "N_base_analytical"]].dropna()

    xmin = 1
    xmax = 10000

    ymin = 0
    ymax = 0.7


    helpers.plot_hybrid_plots(np.array([col['N_tot_ctrc'] for col in ships_updraft_ctrc]),
                              np.array([col['updraft_ctrc'] for col in ships_updraft_ctrc]),
                              np.array([col['N_tot_ctrc'] for col in track_updraft_ctrc]),
                              np.array([col['updraft_ctrc'] for col in track_updraft_ctrc]),
                              np.array([col['N_base_analytical']  for col in ships_updraft_ctrc]),
                              np.array([col['updraft_ctrc'] for col in ships_updraft_ctrc]),
                              np.array([col['N_base_analytical']for col in track_updraft_ctrc]),
                              np.array([col['updraft_ctrc'] for col in track_updraft_ctrc]),
                              xmin,
                              xmax,
                              ymin,
                              ymax,
                              True,
                              False,
                              "No tracks",
                              "Tracks",
                              "-",
                              plot_identifiers,
                              r"$N_{\textnormal{a0}}$ [$cm^{-3}$]",
                              w[longname] + " [" + w[units] + "]",
                              r"$N_{\textnormal{as}}$ [$cm^{-3}$]",
                              w[longname] + " [" + w[units] + "]",
                              paper_figures_dir,
                              f"ctrc_{fname_next}",
                              bins=20,
                              fontsize=fontsize)

    helpers.plot_hybrid_plots(np.array([col['N_tot_koh'] for col in ships_updraft_kohler]),
                              np.array([col['updraft'] for col in ships_updraft_kohler]),
                              np.array([col['N_tot_koh'] for col in track_updraft_kohler]),
                              np.array([col['updraft'] for col in track_updraft_kohler]),
                              np.array([col['N_base_analytical'] for col in ships_updraft_kohler]),
                              np.array([col['updraft'] for col in ships_updraft_kohler]),
                              np.array([col['N_base_analytical'] for col in track_updraft_kohler]),
                              np.array([col['updraft'] for col in track_updraft_kohler]),
                              xmin,
                              xmax,
                              ymin,
                              ymax,
                              True,
                              False,
                              "No tracks",
                              "Tracks",
                              "-",
                              plot_identifiers,
                              r"$N_{\textnormal{a0}}$ [$cm^{-3}$]",
                              w[longname] + " [" + w[units] + "]",
                              r"$N_{\textnormal{as}}$ [$cm^{-3}$]",
                              w[longname] + " [" + w[units] + "]",
                              paper_figures_dir,
                              f"kohler_{fname_next}",
                              bins=20,
                              fontsize=fontsize)