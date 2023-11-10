import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import helpers
from named_variables import *


def plot_fname(figures_dir, name_after_experiment):
    return figures_dir +'all_correlations_coupled'+ name_after_experiment + '.pdf'

def plot_coupled_correlations(paper_figures_dir, dfs, legend_labels, colors, plot_title, fontsize, set_logscale=False):

    helpers.check_sizes_are_consistent([dfs, legend_labels, colors])

    labels_subplots = [['(a)', '(b)', '(c)'], ['(d)', '(e)', '(f)'], ['(g)', '(h)', '(i)']]
    label_position = [0.15, 1.12]
    scattersize = 15.0
    fig1, axs = plt.subplots(3, 3, figsize=(8.9, 8.9))
    ks = len(dfs)
    for k, df, lb, color in zip(range(ks), dfs, legend_labels, colors):
        axs[k, 0].scatter(df["epsilon_param"], df["epsilon_obs"], s=scattersize, color='k', alpha=0.7,
                        label=rf"all ($r^2 ={df['epsilon_param'].corr(df['epsilon_obs']) ** 2:.2f})$")
        axs[k, 0].scatter(df.loc[df['is_coupled']]["epsilon_param"], df.loc[df['is_coupled']]["epsilon_obs"], s=scattersize, color=color, alpha=0.7,
                        label=rf"coupled ($r^2 ={df.loc[df['is_coupled']]['epsilon_param'].corr(df.loc[df['is_coupled']]['epsilon_obs']) ** 2:.2f})$")
        
        axs[k, 0].plot(np.linspace(0, 10, 100), np.linspace(0, 10, 100) , color='r', linewidth=2)
        axs[k, 0].plot(np.linspace(-2, 8, 100), np.linspace(0, 10, 100) , color='grey', linewidth=2)
        axs[k, 0].plot(np.linspace(2, 12, 100), np.linspace(0, 10, 100) , color='grey', linewidth=2)

        axs[k, 0].text(label_position[0], label_position[1], labels_subplots[k][0], transform=axs[k, 0].transAxes, fontsize=fontsize, fontweight='bold', va='top', ha='right')
        axs[k, 0].axis(xmin=0, xmax=12, ymin=0, ymax=12)
        axs[k, 0].tick_params(axis='both', labelsize=fontsize)
        axs[k, 0].set_aspect('equal', 'box')
        axs[k, 0].set_xticks([])
        axs[k, 0].set_yticks([])
        axs[k, 0].legend(loc='upper center', handletextpad=0.1)

    for k, df, lb, color in zip(range(ks), dfs, legend_labels, colors):
        axs[k, 1].scatter(df["epsilon_param_ctrc"], df["epsilon_obs"], s=scattersize, color='k', alpha=0.7,
                        label=rf"all ($r^2 ={df['epsilon_param_ctrc'].corr(df['epsilon_obs']) ** 2:.2f})$")
        axs[k, 1].scatter(df.loc[df['is_coupled']]["epsilon_param_ctrc"], df.loc[df['is_coupled']]["epsilon_obs"], s=scattersize, color=color, alpha=0.7,
                        label=rf"coupled ($r^2 ={df.loc[df['is_coupled']]['epsilon_param_ctrc'].corr(df.loc[df['is_coupled']]['epsilon_obs']) ** 2:.2f})$")
        
        axs[k, 1].plot(np.linspace(0, 10, 100), np.linspace(0, 10, 100) , color='r', linewidth=2)
        axs[k, 1].plot(np.linspace(-2, 8, 100), np.linspace(0, 10, 100) , color='grey', linewidth=2)
        axs[k, 1].plot(np.linspace(2, 12, 100), np.linspace(0, 10, 100) , color='grey', linewidth=2)

        axs[k, 1].text(label_position[0], label_position[1], labels_subplots[k][1], transform=axs[k, 1].transAxes, fontsize=fontsize, fontweight='bold', va='top', ha='right')
        axs[k, 1].axis(xmin=0, xmax=12, ymin=0, ymax=12)
        axs[k, 1].tick_params(axis='both', labelsize=fontsize)
        axs[k, 1].set_aspect('equal', 'box')
        axs[k, 1].set_xticks([])
        axs[k, 1].set_yticks([])
        axs[k, 1].legend(loc='upper center', handletextpad=0.1)

    for k, df, lb, color in zip(range(ks), dfs, legend_labels, colors):
        axs[k, 2].scatter(df["epsilon_param_fit"], df["epsilon_obs"], s=scattersize, color='k', alpha=0.7,
                        label=rf"all ($r^2 ={df['epsilon_param_fit'].corr(df['epsilon_obs']) ** 2:.2f})$")
        axs[k, 2].scatter(df.loc[df['is_coupled']]["epsilon_param_fit"], df.loc[df['is_coupled']]["epsilon_obs"], s=scattersize, color=color, alpha=0.7,
                        label=rf"coupled ($r^2 ={df.loc[df['is_coupled']]['epsilon_param_fit'].corr(df.loc[df['is_coupled']]['epsilon_obs']) ** 2:.2f})$")
        
        axs[k, 2].plot(np.linspace(0, 10, 100), np.linspace(0, 10, 100) , color='r', linewidth=2)
        axs[k, 2].plot(np.linspace(-2, 8, 100), np.linspace(0, 10, 100) , color='grey', linewidth=2)
        axs[k, 2].plot(np.linspace(2, 12, 100), np.linspace(0, 10, 100) , color='grey', linewidth=2)

        axs[k, 2].text(label_position[0], label_position[1], labels_subplots[k][2], transform=axs[k, 2].transAxes, fontsize=fontsize, fontweight='bold', va='top', ha='right')
        axs[k, 2].axis(xmin=0, xmax=12, ymin=0, ymax=12)
        axs[k, 2].tick_params(axis='both', labelsize=fontsize)
        axs[k, 2].set_aspect('equal', 'box')
        axs[k, 2].set_xticks([])
        axs[k, 2].set_yticks([])
        axs[k, 2].legend(loc='upper center', handletextpad=0.1)

    js = 3
    for j in range(js):
        axs[2, j].set_xlabel(r'$\epsilon$ (parameterised)[-]',fontsize=fontsize)
        axs[2, j].set_xticks([0, 5, 10])
    
    for k in range(ks):
        axs[k, 0].set_ylabel(r'$\epsilon$ (observed)[-]',fontsize=fontsize)
        axs[k, 0].set_yticks([0, 5, 10])



    # for df, lb, color in zip(dfs, legend_labels, colors):

    #     axs[0].scatter(df["epsilon_param"], df["epsilon_obs"], s=scattersize, color=color, alpha=0.7,
    #                     label=rf"{lb} ($r^2 ={df['epsilon_obs'].corr(df['epsilon_param']) ** 2:.2f})$")
    #     print(f"r2{lb}", df['epsilon_obs'].corr(df['epsilon_param'])**2)


    # axs[0].plot(np.linspace(0, 10, 100), np.linspace(0, 10, 100) , color='r', linewidth=2)
    # axs[0].plot(np.linspace(-2, 8, 100), np.linspace(0, 10, 100) , color='grey', linewidth=2)
    # axs[0].plot(np.linspace(2, 12, 100), np.linspace(0, 10, 100) , color='grey', linewidth=2)

    # axs[0].text(0.11, 1.08, labels_subplots[0], transform=axs[0].transAxes, fontsize=fontsize, fontweight='bold', va='top', ha='right')
    # axs[0].axis(xmin=0, xmax=12, ymin=0, ymax=12)
    # # axs[0].set_xlabel(r'$\epsilon$ (parameterised)[-]',fontsize=fontsize)
    # axs[0].set_ylabel(r'$\epsilon$ (observed)[-]',fontsize=fontsize)
    # axs[0].tick_params(axis='both', labelsize=fontsize)
    # axs[0].set_aspect('equal', 'box')
    # axs[0].set_xticks([])
    # axs[0].legend()
    

    # for df, lb, color in zip(dfs, legend_labels, colors):
    #     axs[1].scatter(df["epsilon_param_ctrc"], df["epsilon_obs"], s= scattersize, color=color, alpha=0.7,
    #                 label=rf"{lb} ($r^2 ={df['epsilon_obs'].corr(df['epsilon_param_ctrc'])**2:.2f})$")

    #     print(f"r2{lb}", df['epsilon_obs'].corr(df['epsilon_param_ctrc'])**2)

    # axs[1].plot(np.linspace(0, 10, 100), np.linspace(0, 10, 100) , color='r', linewidth=2)
    # axs[1].plot(np.linspace(-2, 8, 100), np.linspace(0, 10, 100) , color='grey', linewidth=2)
    # axs[1].plot(np.linspace(2, 12, 100), np.linspace(0, 10, 100) , color='grey', linewidth=2)

    # axs[1].text(0.11, 1.08, labels_subplots[1], transform=axs[1].transAxes, fontsize=fontsize, fontweight='bold', va='top', ha='right')
    # axs[1].axis(xmin=0, xmax=12, ymin=0, ymax=12)
    # # axs[1].set_xlabel(r'$\epsilon$ (parameterised)[-]',fontsize=fontsize)
    # axs[1].set_ylabel(r'$\epsilon$ (observed)[-]',fontsize=fontsize)
    # axs[1].tick_params(axis='both', labelsize=fontsize)
    # axs[1].set_aspect('equal', 'box')
    # axs[1].set_xticks([])
    # axs[1].legend()


    # for df, lb, color in zip(dfs, legend_labels, colors):
    #     axs[2].scatter(df["epsilon_param_fit"], df["epsilon_obs"], s= scattersize, color=color, alpha=0.7,
    #                 label=rf"{lb} ($r^2 ={df['epsilon_obs'].corr(df['epsilon_param_fit'])**2:.2f})$")

    #     print(f"r2{lb}", df['epsilon_obs'].corr(df['epsilon_param_fit'])**2)

    # axs[2].plot(np.linspace(0, 10, 100), np.linspace(0, 10, 100) , color='r', linewidth=2)
    # axs[2].plot(np.linspace(-2, 8, 100), np.linspace(0, 10, 100) , color='grey', linewidth=2)
    # axs[2].plot(np.linspace(2, 12, 100), np.linspace(0, 10, 100) , color='grey', linewidth=2)

    # axs[2].text(0.11, 1.08, labels_subplots[2], transform=axs[2].transAxes, fontsize=fontsize, fontweight='bold', va='top', ha='right')
    # axs[2].axis(xmin=0, xmax=12, ymin=0, ymax=12)
    # axs[2].set_xlabel(r'$\epsilon$ (parameterised)[-]',fontsize=fontsize)
    # axs[2].set_ylabel(r'$\epsilon$ (observed)[-]',fontsize=fontsize)
    # axs[2].tick_params(axis='both', labelsize=fontsize)
    # axs[2].set_aspect('equal', 'box')
    # axs[2].legend()



    plt.subplots_adjust(wspace=0.6)

    plt.savefig(plot_fname(paper_figures_dir, plot_title), dpi=300)



