import pandas as pd
import matplotlib.pyplot as plt
from named_variables import *
import helpers
def plot_fname(figures_dir, name_after_experiment):
    return figures_dir + 'fit' +'_'+ name_after_experiment + '.pdf'

def plot_updrafts_boxplot(paper_figures_dir, dfs, legend_labels, colors, nbins, plot_title, fontsize = 26, linewidth = 2):

    helpers.check_sizes_are_consistent([dfs, legend_labels, colors])

    mase2_arr = [0.26,0.68,0.44,0.91,2.21,0.3,0.11,0.32, 0.28]
    mase2_dataframe = pd.DataFrame(mase2_arr, columns = ["updraft"])

    cstripe_arr = [0.22,
                    0.28,
                    0.3,
                    0.27,
                    0.28,
                    0.2,
                    0.29,
                    0.24,
                    0.15,
                    0.14,
                    0.18,
                    0.22,
                    0.25,
                    0.2,
                    0.23,
                    0.19,
                    0.32,
                    0.24,
                    0.32,
                    0.17,
                    0.16,
                    0.21,
                    0.17,
                    0.27,
                    0.36,
                    0.54,
                    0.15,
                    0.2,
                    0.25,
                    0.21,
                    0.18,
                    0.15,
                    0.22,
                    0.31,
                    0.22,
                    0.26,
                    0.3,
                    0.2,
                    0.24,
                    0.26,
                    0.37,
                    0.37,
                    0.3,
                    0.28,
                    0.46,
                    0.29,
                    0.44,
                    0.29,
                    0.41,
                    0.48,
                    0.34,
                    0.36]

    cstripe_dataframe = pd.DataFrame(cstripe_arr, columns=["updraft"])

    _, ax3 = plt.subplots(1,1, figsize=(8.9,6))

    boxwidth = 0.15
    boxprops_exp = dict(color=(178/255, 178/255, 178/255))
    boxprops_zheng = dict(color='k')


    ax3 = mase2_dataframe.boxplot(column=['updraft'], positions=[0], widths=boxwidth, boxprops=boxprops_exp, medianprops = boxprops_exp, whiskerprops = boxprops_exp, capprops = boxprops_exp, flierprops = boxprops_exp)
    ax3 = cstripe_dataframe.boxplot(column=['updraft'], positions=[1], widths=boxwidth, boxprops=boxprops_exp, medianprops = boxprops_exp, whiskerprops = boxprops_exp, capprops = boxprops_exp, flierprops = boxprops_exp)
    ax3 = dfs[0].boxplot(column=['updraft_ctrc'], positions=[2], widths=boxwidth,
                                         boxprops=boxprops_zheng,
                                         medianprops=boxprops_zheng, whiskerprops=boxprops_zheng,
                                         capprops=boxprops_zheng,
                                         flierprops=boxprops_zheng)
    ax3 = dfs[0].loc[dfs[0]['is_coupled']].boxplot(column=['updraft_ctrc'], positions=[3], widths=boxwidth,
                                        boxprops=boxprops_zheng,
                                        medianprops=boxprops_zheng, whiskerprops=boxprops_zheng,
                                        capprops=boxprops_zheng,
                                        flierprops=boxprops_zheng)

    for index, iterators in enumerate(zip(dfs, legend_labels, colors)):

        df, lb, color = iterators

        Q1 = df['updraft'].quantile(0.25)
        Q3 = df['updraft'].quantile(0.75)
        IQR = Q3 - Q1

        outliers_not_in_axes_range = ((df['updraft'] < (Q1 - 1.5 * IQR)) | (df['updraft'] > (Q3 + 1.5 * IQR)) & (df['updraft'] > 1.0)).sum()

        print(f"{lb}: {df['updraft'].median()/df['updraft_ctrc'].median()}")

        boxprops = dict(color=color)
        ax3 = df.boxplot(column=['updraft'], positions=[4+2*index], widths=boxwidth, boxprops=boxprops,
                                             medianprops=boxprops, whiskerprops=boxprops, capprops=boxprops,
                                             flierprops=boxprops)
        if outliers_not_in_axes_range > 0:
            ax3.text(4+2*index-0.5, 0.8, f"{outliers_not_in_axes_range} outliers",fontsize=12, rotation = 60)

            ax3.arrow(4+2*index-0.16, 0.93, 0.1, 0.047,
                        head_width=0.015,
                        width=0.0025,
                        ec='black',
                        fc='black')

        Q1_c = df.loc[df['is_coupled']]['updraft'].quantile(0.25)
        Q3_c = df.loc[df['is_coupled']]['updraft'].quantile(0.75)
        IQR_c = Q3_c - Q1_c

        outliers_not_in_axes_range_c = ((df.loc[df['is_coupled']]['updraft'] < (Q1_c - 1.5 * IQR_c)) | (df.loc[df['is_coupled']]['updraft'] > (Q3_c + 1.5 * IQR_c)) & (df.loc[df['is_coupled']]['updraft'] > 1.0)).sum()
        ax3 = df.loc[df['is_coupled']].boxplot(column=['updraft'], positions=[5+2*index], widths=boxwidth, boxprops=boxprops,
                                             medianprops=boxprops, whiskerprops=boxprops, capprops=boxprops,
                                             flierprops=boxprops)
        
        if outliers_not_in_axes_range_c > 0:
            ax3.text(5+2*index-0.5, 0.8, f"{outliers_not_in_axes_range_c} outliers",fontsize=12, rotation = 60)

            ax3.arrow(5+2*index-0.16, 0.93, 0.1, 0.047,
                        head_width=0.015,
                        width=0.0025,
                        ec='black',
                        fc='black')



    ax3.axhline(0, color="k")
    fixed_labels = ['MASE2','CSTRIPE','CTRC',f"CTRC{r'$_{coup}$'}"]

    legend_labels_both = []

    for l in legend_labels:
        legend_labels_both.append(l)
        legend_labels_both.append(f"{l}{r'$_{coup}$'}")


    labels = fixed_labels + legend_labels_both
    print(labels, legend_labels_both)
    ax3.set_ylabel(w[longname] + " [" +w[units] +"]", fontsize=fontsize)
    ax3.tick_params(axis='x', labelsize=fontsize)
    ax3.tick_params(axis='y', labelsize=fontsize)
    ax3.set_ylim([0, 1.0])
    ax3.set_xticklabels(labels, rotation = 0)
    ax3.grid(False)


    plt.tight_layout()
    plt.savefig(plot_fname(paper_figures_dir, f'up_boxplot_{plot_title}'), dpi=300)

