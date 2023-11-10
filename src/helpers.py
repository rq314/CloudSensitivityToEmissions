from matplotlib.transforms import Bbox
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_fname(figures_dir, experiment_name, name_after_experiment):
    return f"{figures_dir}{experiment_name}_{name_after_experiment}.pdf"


def check_sizes_are_consistent(elements):
    sizes = []

    for elem in elements:
        sizes.append(len(elem))

    if sizes.count(sizes[0]) != len(sizes):
        raise ValueError(f"{sizes} for dfs, legend_labels and colors should match")

def plot_hybrid_plots(X1, Y1, X2, Y2, X3, Y3, X4, Y4, XMIN, XMAX, YMIN, YMAX, log_scale_x, log_scale_y, title1, title2, extratitle, identifiers ,xlabel1, ylabel1, xlabel2, ylabel2, figdir,
                          fnamext, bins=25, fontsize=16):
    length = 3



    fig = plt.figure(figsize=(12, 16))
    grid = plt.GridSpec(12, 12, figure=fig, hspace=1.5, wspace=0.0)

    grid_left = grid[0:11,0:6].subgridspec(3, 1)
    grid_right = grid[0:11,6:].subgridspec(3, 1)

    grid_lefts = [None]*length
    grid_rights = [None]*length

    grid_lefts[0] = grid_left[0].subgridspec(4, 4)
    grid_lefts[1] = grid_left[1].subgridspec(4, 4)
    grid_lefts[2] = grid_left[2].subgridspec(4, 4)
    grid_rights[0] = grid_right[0].subgridspec(4, 4)
    grid_rights[1] = grid_right[1].subgridspec(4, 4)
    grid_rights[2] = grid_right[2].subgridspec(4, 4)

    grid_cbar = grid[-1,:-1].subgridspec(1, 1)


    main_ax_left = [None]*length
    y_hist_left = [None]*length
    x_hist_left = [None]*length

    main_ax_right = [None]*length
    y_hist_right = [None]*length
    x_hist_right = [None]*length

    hist_left = [None]*length
    hist_right = [None]*length

    cmap = plt.get_cmap('coolwarm', 25)
    cmap.set_bad('white', 1.0)

    x_hist_shift_vert = 0.0585
    y_hist_shift_hor = 0.009

    for i_df in range(length):
        if log_scale_x:
            x1 = [np.log10(x) for x in X1[i_df]]
            x2 = [np.log10(x) for x in X2[i_df]]
            x3 = [np.log10(x) for x in X3[i_df]]
            x4 = [np.log10(x) for x in X4[i_df]]
            xmin = np.log10(XMIN)
            xmax = np.log10(XMAX)
        else:
            x1 = X1[i_df]
            x2 = X2[i_df]
            x3 = X3[i_df]
            x4 = X4[i_df]
            xmin = XMIN
            xmax = XMAX

        if log_scale_y:
            y1 = [np.log10(y) for y in Y1[i_df]]
            y2 = [np.log10(y) for y in Y2[i_df]]
            y3 = [np.log10(y) for y in Y3[i_df]]
            y4 = [np.log10(y) for y in Y4[i_df]]
            ymin = np.log10(YMIN)
            ymax = np.log10(YMAX)
        else:
            y1 = Y1[i_df]
            y2 = Y2[i_df]
            y3 = Y3[i_df]
            y4 = Y4[i_df]
            ymin = YMIN
            ymax = YMAX

        ext = (xmin, xmax, ymin, ymax)

        main_ax_left[i_df] = fig.add_subplot(grid_lefts[i_df][1:4, 0:3])
        y_hist_left[i_df] = fig.add_subplot(grid_lefts[i_df][1:4, -1], xticklabels=[], sharey=main_ax_left[i_df])
        x_hist_left[i_df] = fig.add_subplot(grid_lefts[i_df][0, 0:3], yticklabels=[], sharex=main_ax_left[i_df])

        main_ax_right[i_df] = fig.add_subplot(grid_rights[i_df][1:4, 0:3])
        y_hist_right[i_df] = fig.add_subplot(grid_rights[i_df][1:4, -1], xticklabels=[], sharey=main_ax_right[i_df])
        x_hist_right[i_df] = fig.add_subplot(grid_rights[i_df][0, 0:3], yticklabels=[], sharex=main_ax_right[i_df])

        counts1, xedges1, yedges1 = np.histogram2d(x1, y1, bins=bins, range=[[xmin, xmax], [ymin, ymax]], normed=False)
        counts2, xedges2, yedges2 = np.histogram2d(x2, y2, bins=bins, range=[[xmin, xmax], [ymin, ymax]], normed=False)
        # difference in probability of occurence
        counts_first_plot = (counts2 / counts2.sum()) - (counts1 / counts1.sum())

        for i in range(bins):
            for j in range(bins):
                if counts1[i][j] == 0 and counts2[i][j] == 0:
                    counts_first_plot[i][j] = np.nan

        YEDGES1, XEDGES1 = np.meshgrid(yedges1, xedges1)

        vmaxabs = 0.05

        hist_left[i_df] = main_ax_left[i_df].pcolormesh(XEDGES1, YEDGES1, counts_first_plot, cmap=cmap, vmin=-vmaxabs, vmax=vmaxabs)

        if log_scale_x:
            main_ax_left[i_df].plot(np.log10(np.logspace(xmin, xmax, 100)), 10 ** (-4) * np.logspace(xmin, xmax, 100), 'k--',
                         label='Updraft-lim')
            main_ax_left[i_df].plot(np.log10(np.logspace(xmin, xmax, 100)), 10 ** (-3) * np.logspace(xmin, xmax, 100), 'k:',
                         label='Aerosol-lim')
        else:
            main_ax_left[i_df].plot(np.linspace(xmin, xmax, 100), 10 ** (-4) * np.linspace(xmin, xmax, 100), 'k--', label='Updraft-lim')
            main_ax_left[i_df].plot(np.linspace(xmin, xmax, 100), 10 ** (-3) * np.linspace(xmin, xmax, 100), 'k:', label='Aerosol-lim')

        main_ax_left[i_df].set_xlim([xmin, xmax])
        main_ax_left[i_df].set_ylim([ymin, ymax])

        x_hist_left[i_df].text(0, 1.08, identifiers[i_df][0], transform=x_hist_left[i_df].transAxes, fontsize=fontsize, fontweight='bold', va='top',
                     ha='right')

        main_ax_left[i_df].set_box_aspect(1)
        main_ax_left[i_df].set_xlabel(xlabel1, fontsize=fontsize)
        main_ax_left[i_df].set_ylabel(ylabel1, fontsize=fontsize)
        main_ax_left[i_df].set_xticks(np.arange(5), labels=[r"$10^0$", r"$10^1$", r"$10^2$", r"$10^3$", r"$10^4$"])
        main_ax_left[i_df].tick_params(axis='x', labelsize=fontsize)
        main_ax_left[i_df].tick_params(axis='y', labelsize=fontsize)

        main_ax_left[i_df].text(0.3, 0.45, r"Aerosol-lim",fontsize=12, rotation = 90, bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 2})
        main_ax_left[i_df].arrow(0.65, 0.6, 2, 0,
                       head_width=0.03,
                       width=0.005,
                       ec='black',
                       fc='black')

        main_ax_left[i_df].text(3.6, 0.03, r"Updraft-lim",fontsize=12,rotation = 90, bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 2})
        main_ax_left[i_df].arrow(3.5, 0.03, -0.7, 0,
                  head_width=0.03,
                  width=0.005,
                  ec='black',
                  fc='black')

        counts3, xedges3, yedges3 = np.histogram2d(x3, y3, bins=bins, range=[[xmin, xmax], [ymin, ymax]], normed=False)
        counts4, xedges4, yedges4 = np.histogram2d(x4, y4, bins=bins, range=[[xmin, xmax], [ymin, ymax]], normed=False)
        # difference in probability of occurence
        counts_second_plot = (counts4 / counts4.sum()) - (counts3 / counts3.sum())

        for i in range(bins):
            for j in range(bins):
                if counts3[i][j] == 0 and counts4[i][j] == 0:
                    counts_second_plot[i][j] = np.nan

        YEDGES3, XEDGES3 = np.meshgrid(yedges3, xedges3)

        vmaxabs = 0.05
        hist_right = main_ax_right[i_df].pcolormesh(XEDGES3, YEDGES3, counts_second_plot, cmap=cmap, vmin=-vmaxabs, vmax=vmaxabs)

        x_hist_right[i_df].text(0, 1.08, identifiers[i_df][1], transform=x_hist_right[i_df].transAxes, fontsize=fontsize, fontweight='bold', va='top',
                     ha='right')

        main_ax_right[i_df].set_xlim([xmin, xmax])
        main_ax_right[i_df].set_ylim([ymin, ymax])
        main_ax_right[i_df].set_box_aspect(1)
        main_ax_right[i_df].set_xlabel(xlabel2, fontsize=fontsize)
        main_ax_right[i_df].set_xticks(np.arange(5), labels=[r"$10^0$", r"$10^1$", r"$10^2$", r"$10^3$", r"$10^4$"])

        main_ax_right[i_df].tick_params(axis='x', labelsize=fontsize)
        main_ax_right[i_df].tick_params(axis='y', labelsize=fontsize)

        # histogram on the attached axes
        x_hist_left[i_df].hist(x1, bins, histtype='stepfilled', orientation='vertical',color="lightgrey", range=(xmin, xmax), density=True, alpha=0.7,
                     label=title1)
        x_hist_left[i_df].hist(x2, bins, histtype='step', orientation='vertical',color="k", range=(xmin, xmax), density=True, alpha=0.7,
                     label=title2)
        x_hist_left[i_df].legend(loc='upper left', fontsize=10)
        x_hist_left[i_df].get_xaxis().set_visible(False)
        x_hist_left[i_df].set_yticks([])
        x_hist_left[i_df].spines['left'].set_visible(False)
        x_hist_left[i_df].spines['right'].set_visible(False)
        x_hist_left[i_df].spines['top'].set_visible(False)

        y_hist_left[i_df].get_yaxis().set_visible(False)
        y_hist_left[i_df].set_xticks([])
        y_hist_left[i_df].spines['right'].set_visible(False)
        y_hist_left[i_df].spines['top'].set_visible(False)
        y_hist_left[i_df].spines['bottom'].set_visible(False)
        y_hist_left[i_df].spines['left'].set_visible(False)


        (x0m, y0m), (x1m, y1m) = main_ax_left[i_df].get_position().get_points()  # main heatmap
        (x0h, y0h), (x1h, y1h) = x_hist_left[i_df].get_position().get_points()  # horizontal histogram
        x_hist_left[i_df].set_position(Bbox([[x0m, y0h-y_hist_shift_hor], [x1m, y1h-y_hist_shift_hor]]))
        (x0v, y0v), (x1v, y1v) = y_hist_left[i_df].get_position().get_points()  # vertical histogram
        height_delta = (y1h - y0h) - (x1v - x0v)
        y_hist_left[i_df].set_position(Bbox([[x0v, y0m], [x1v, y1m]]))

        #
        # histogram on the attached axes
        x_hist_right[i_df].hist(x3, bins, histtype='stepfilled', orientation='vertical',color="lightgrey", range=(xmin, xmax), density=True, alpha=0.7)
        x_hist_right[i_df].hist(x4, bins, histtype='step', orientation='vertical',color="k", range=(xmin, xmax), density=True, alpha=0.7)
        x_hist_right[i_df].get_xaxis().set_visible(False)

        x_hist_right[i_df].set_yticks([])
        x_hist_right[i_df].spines['left'].set_visible(False)
        x_hist_right[i_df].spines['right'].set_visible(False)
        x_hist_right[i_df].spines['top'].set_visible(False)

        y_hist_right[i_df].hist(y3, bins, histtype='stepfilled', orientation='horizontal',color="lightgrey", range=(ymin, ymax), density=True, alpha=0.7)
        y_hist_right[i_df].hist(y4, bins, histtype='step', orientation='horizontal',color="k", range=(ymin, ymax), density=True, alpha=0.7)
        y_hist_right[i_df].get_yaxis().set_visible(False)
        y_hist_right[i_df].set_xticks([])
        y_hist_right[i_df].spines['right'].set_visible(False)
        y_hist_right[i_df].spines['top'].set_visible(False)
        y_hist_right[i_df].spines['bottom'].set_visible(False)

        (x0m, y0m), (x1m, y1m) = main_ax_right[i_df].get_position().get_points()  # main heatmap
        (x0h, y0h), (x1h, y1h) = x_hist_right[i_df].get_position().get_points()  # horizontal histogram
        x_hist_right[i_df].set_position(Bbox([[x0m, y0h-y_hist_shift_hor], [x1m, y1h-y_hist_shift_hor]]))
        (x0v, y0v), (x1v, y1v) = y_hist_right[i_df].get_position().get_points()  # vertical histogram
        height_delta = (y1h - y0h) - (x1v - x0v)
        y_hist_right[i_df].set_position(Bbox([[x0v-x_hist_shift_vert, y0m], [x1v-x_hist_shift_vert, y1m]]))

    cax = fig.add_subplot(grid_cbar[0])
    cax.get_yaxis().set_visible(False)
    cax.set_xticks([])
    cax.spines['right'].set_visible(False)
    cax.spines['top'].set_visible(False)
    cax.spines['bottom'].set_visible(False)
    cax.spines['left'].set_visible(False)

    cbar = fig.colorbar(hist_right, orientation='horizontal', ax=cax, fraction=0.5, pad=0.1 )
    cbar.ax.tick_params(labelsize=fontsize)
    cbar.ax.set_xlabel('P(Track) - P(noTrack)', rotation=0, fontsize=fontsize)
    print(fnamext)
    plt.savefig(plot_fname(figdir, fnamext, 'hybrid'), pad_inches=0.1, bbox_inches="tight", dpi=300)

