import pandas as pd
import matplotlib.pyplot as plt
from named_variables import *
import numpy as np

def bar_color(df,color1,color2):
    return np.where(df.values>0,color1,color2).T


def plot_fname(figures_dir, name_after_experiment):
   return figures_dir + 'sensitivity_study' + name_after_experiment + '.pdf'

def plot_sensitivitystudy(paper_figures_dir, sens_df, plot_title, fontsize, linewidth = 2):

    plt.rcParams['text.usetex'] = True

    fig, ax = plt.subplots(1, 1, figsize=(8.9,6))

    rows = [sox, spd_res, cbh, nd_cln, w, d_pol,d_bgd_ais, d_bgd_acs, d_bgd_cos, k_bgd, k_pol, sigma_pol, sigma_bgd]


    longnames = [r[longname] for r in rows]

    ind = np.arange(len(rows))

    ax.bar(ind -0.3, sens_df['sens_arg'][:-2].to_list(), color=(196/255, 121/255, 0/255), width = 0.2, label = 'ARG')
    ax.bar(ind -0.1, sens_df['sens_mbn'][:-2].to_list(), color=(112 / 255, 160 / 255, 205 / 255), width = 0.2, label = 'MBN')
    ax.bar(ind + 0.1 , sens_df['sens_lkup'][:-2].to_list(), color=(0 / 255, 79 / 255, 0 / 255), width = 0.2, label = 'RW')

    ax.set_xticks(ind, tuple(longnames))
    ax.set_ylabel(r"$\frac{\partial \epsilon}{\partial p_i} \Delta p_i$", fontsize=fontsize)
    ax.tick_params(axis='x', labelsize=fontsize)
    ax.tick_params(axis='y', labelsize=fontsize)
    ax.set_xticklabels(tuple(longnames), rotation = 0)
    ax.set_ylim([-0.3, 1.6])
    ax.legend(fontsize=fontsize)
    plt.tight_layout()

    plt.axhline(0, color="k")

    plt.savefig(plot_fname(paper_figures_dir, f"_{plot_title}"), dpi=300)

    # Plots scatter plot of sensitivities for all parameters vs uncertainties with labelling point with parameter name
    fig, ax = plt.subplots(1, 1, figsize=(8.9,6))
    
    ax.scatter(sens_df['Deltap_perc'][:-2].to_list(), sens_df['sens_arg'][:-2].to_list(), color=(196/255, 121/255, 0/255), label = 'ARG')
    ax.scatter(sens_df['Deltap_perc'][:-2].to_list(), sens_df['sens_mbn'][:-2].to_list(), color=(112 / 255, 160 / 255, 205 / 255), label = 'MBN')
    ax.scatter(sens_df['Deltap_perc'][:-2].to_list(), sens_df['sens_lkup'][:-2].to_list(), color=(0 / 255, 79 / 255, 0 / 255), label = 'RW')

    for i, txt in enumerate(longnames):
        ax.annotate(txt, (sens_df['Deltap_perc'][:-2].to_list()[i], sens_df['sens_arg'][:-2].to_list()[i]), fontsize=fontsize)
        ax.annotate(txt, (sens_df['Deltap_perc'][:-2].to_list()[i], sens_df['sens_mbn'][:-2].to_list()[i]), fontsize=fontsize)
        ax.annotate(txt, (sens_df['Deltap_perc'][:-2].to_list()[i], sens_df['sens_lkup'][:-2].to_list()[i]), fontsize=fontsize)

    
    
    ax.set_xlabel(r"$\Delta p_i$ [$\%$]", fontsize=fontsize)
    ax.set_ylabel(r"$\frac{\partial \epsilon}{\partial p_i} $", fontsize=fontsize)
    ax.tick_params(axis='x', labelsize=fontsize)
    ax.tick_params(axis='y', labelsize=fontsize)
    ax.legend(fontsize=fontsize)

    # Plots bar plots of the breakdown of sensitivities
    labels_subplots = ['(a)', '(b)', '(c)']
    scattersize = 15.0
    fig1, axs = plt.subplots(3, 1, figsize=(9, 11))
    
    # Plots the uncertainties for all parameters
    axs[0].bar(ind , sens_df['Deltap_perc'][:-2].to_list(), color='k', width = 0.2)

    axs[0].set_xticks(ind, tuple(longnames))
    axs[0].set_ylabel(r"$\Delta p_i$ [$\%$]", fontsize=fontsize)
    axs[0].tick_params(axis='x', labelsize=fontsize)
    axs[0].tick_params(axis='y', labelsize=fontsize)
    axs[0].set_xticklabels([], rotation = 0)
    axs[0].text(0., 1.1, labels_subplots[0], transform=axs[0].transAxes, fontsize=fontsize, fontweight='bold', va='top', ha='right')

    # Plots bar plots of the sensitivities divided by the uncertainties for all parameters
    axs[1].bar(ind -0.3, (sens_df['nominal'][:-2]*sens_df['depsilon_dp_arg'][:-2]).to_list(), color=(196/255, 121/255, 0/255), width = 0.2, label = 'ARG')
    axs[1].bar(ind -0.1, (sens_df['nominal'][:-2]*sens_df['depsilon_dp_mbn'][:-2]).to_list(), color=(112 / 255, 160 / 255, 205 / 255), width = 0.2, label = 'MBN')
    axs[1].bar(ind + 0.1 , (sens_df['nominal'][:-2]*sens_df['depsilon_dp_lkup'][:-2]).to_list(), color=(0 / 255, 79 / 255, 0 / 255), width = 0.2, label = 'RW')
    axs[1].axhline(0, color="k")

    axs[1].set_xticks(ind, tuple(longnames))
    axs[1].set_ylabel(r"$\frac{\partial \epsilon}{\partial p_i} p_i$", fontsize=fontsize)
    axs[1].tick_params(axis='x', labelsize=fontsize)
    axs[1].tick_params(axis='y', labelsize=fontsize)
    axs[1].set_xticklabels([], rotation = 0)
    axs[1].text(0., 1.1, labels_subplots[1], transform=axs[1].transAxes, fontsize=fontsize, fontweight='bold', va='top', ha='right')


    # Plots bar plots of the sensitivities of all parameters again

    axs[2].bar(ind -0.3, sens_df['sens_arg'][:-2].to_list(), color=(196/255, 121/255, 0/255), width = 0.2, label = 'ARG')
    axs[2].bar(ind -0.1, sens_df['sens_mbn'][:-2].to_list(), color=(112 / 255, 160 / 255, 205 / 255), width = 0.2, label = 'MBN')
    axs[2].bar(ind + 0.1 , sens_df['sens_lkup'][:-2].to_list(), color=(0 / 255, 79 / 255, 0 / 255), width = 0.2, label = 'RW')

    axs[2].axhline(0, color="k")
    axs[2].set_xticks(ind, tuple(longnames))
    axs[2].set_ylabel(r"$\frac{\partial \epsilon}{\partial p_i} \Delta p_i$", fontsize=fontsize)
    axs[2].tick_params(axis='x', labelsize=fontsize)
    axs[2].tick_params(axis='y', labelsize=fontsize)
    axs[2].set_xticklabels(tuple(longnames), rotation = 0)
    axs[2].legend(fontsize=fontsize)
    axs[2].text(0.0, 1.1, labels_subplots[2], transform=axs[2].transAxes, fontsize=fontsize, fontweight='bold', va='top', ha='right')


    plt.savefig(plot_fname(paper_figures_dir, f"breakdown_{plot_title}"), dpi=300)


    plt.show()


