import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import shapiro, ttest_ind
import statsmodels.api as sm

from sklearn.cluster import KMeans
from sklearn.feature_selection import f_regression
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


plt.style.use("ggplot")


def clean_df(data, new_names):
    rename_col = dict(zip(data.columns, new_names))
    data_cardio = data.rename(mapper=rename_col, axis=1)
    return data_cardio


def hist_all(data, num_var, n_col, n_row, title=None, treatment=False, treatment_col_name = 'treatment'):
    """
    treatment = specify treatment column name otherwise default = False
    num_var = list of numerical features
    """
    data_tmp = data.copy()

    fig, axes = plt.subplots(ncols=n_col, nrows=n_row,
                             figsize=(n_col * 3, n_row * 3))
    fig.suptitle(title, fontsize=15)
    if treatment:
        for k, ax in zip(num_var, np.ravel(axes)):
            sns.kdeplot(ax=ax, x=data_tmp[k], hue=data_tmp[treatment_col_name])
            ax.set_title(f"{k} Histogram")
        plt.tight_layout()
        return fig
    else:
        for k, ax in zip(num_var, np.ravel(axes)):
            sns.kdeplot(ax=ax, x=data_tmp[k])
            ax.set_title(f"{k} Histogram")
        plt.tight_layout()
        return fig


def test_all(data, num_var, n_col, n_row, title=None, show_outliers=True, treatment_col_name = 'treatment'):
    '''
    function to visualize groups against each other into one plot
    '''
    df = data.copy()

    fig, ax = plt.subplots(ncols=n_col, nrows=n_row,
                           figsize=(n_col*3, n_row*3))
    if show_outliers:
        for col, ax in zip(num_var, np.ravel(ax)):
            sns.boxplot(ax=ax, data=df, x=treatment_col_name, y=col, showfliers=True)
            ax.set(title=col)
    else:
        for col, ax in zip(num_var, np.ravel(ax)):
            sns.boxplot(ax=ax, data=df, x=treatment_col_name, y=col, showfliers=False)
            ax.set(title=col)
    fig.suptitle(title, fontsize=15)
    plt.tight_layout()


def get_readout_plot(
    data, num_var, n_col, n_row, readout_col, hue, hue_order=None, title=None
):
    """
    num_var = list of numerical features
    readout_col = column to test against
    """
    data_tmp = data.copy()

    fig, axes = plt.subplots(
        ncols=n_col, nrows=n_row, figsize=(n_col * 3, n_row * 3), sharex=True
    )
    fig.suptitle(title, fontsize=15)
    for col, ax in zip(num_var, np.ravel(axes)):
        if hue_order is not None:
            sns.scatterplot(
                ax=ax, data=data_tmp, x=readout_col, y=col, hue=hue, hue_order=hue_order
            )
            ax.set(ylabel=None, title=col)
            ax.legend([])
        else:
            sns.scatterplot(ax=ax, data=data_tmp,
                            x=readout_col, y=col, hue=hue)
            ax.set(ylabel=None, title=col)
            ax.legend([])
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper right")
    return fig


def normal_all(data, n_col, n_row, num_var, treatment_col_name='treatment'):
    """
    getting the normality plot output for all the columns
    """
    # cleaning the data
    data_tmp = data.copy()
    data_tmp.drop(treatment_col_name, axis=1, inplace=True)
    data_tmp.drop("ID", axis=1, inplace=True)

    # creating a dict of Shapiro
    p_values = []

    for i in range(len(data_tmp.columns)):
        pval = shapiro(data_tmp[data_tmp.columns[i]])[1]
        p_values.append(pval)

    data_norm = dict(zip(data_tmp.columns, p_values))

    fig, axes = plt.subplots(ncols=n_col, nrows=n_row,
                             figsize=(n_col * 3, n_row * 3))
    for k, ax in zip(num_var, np.ravel(axes)):
        if data_norm[k] > 0.05:
            sm.qqplot(data_tmp[k], line="s", ax=ax)
            ax.set_title(f"{k} QQ Plot NORMAL", fontweight="bold")
        else:
            sm.qqplot(data_tmp[k], line="s", ax=ax)
            ax.set_title(f"{k} QQ Plot")
    plt.tight_layout()
    return fig


def normal_table(data, treatment_col_name = 'treatment'):
    """
    gets the pvalue output for the Shapiro-normality test
    """
    data_d = data.drop("ID", axis=1)
    data_tmp = data_d.drop(treatment_col_name, axis=1)
    p_values = []

    for i in range(len(data_tmp.columns)):
        pval = shapiro(data_tmp[data_tmp.columns[i]])[1]
        p_values.append(pval)
    data_norm = dict(zip(data_tmp.columns, p_values))
    data_pd = pd.DataFrame(
        data_norm.values(), data_norm.keys()
    ).style.background_gradient(cmap="Reds")
    return data_pd


def get_num_var(data):
    num_var = []
    for label, content in data.items():
        if pd.api.types.is_float_dtype(content):
            num_var.append(label)
    return num_var


def get_elbow(data):
    """
    outputs the graph of the elbow method using a specified range
    """
    wcss = []
    for i in range(1, 10):
        kmeans = KMeans(n_clusters=i, random_state=42)
        kmeans.fit(data)
        wcss.append(kmeans.inertia_)

    fig, ax = plt.subplots(figsize=(5, 5))
    plt.plot(range(1, 10), wcss)
    plt.xlabel("Number of Clusters")
    plt.ylabel("Inertia")
    plt.title("Elbow method")


def get_f_regression(data, num_var, treatment_col_name = 'treatment'):
    '''
    function to get the f_regression output
    '''
    X = data[num_var]
    Y = data[treatment_col_name]

    f_stat, p_val = f_regression(X, Y)

    pd_pc = pd.DataFrame(f_stat, index=X.columns, columns=["F statistics"])
    pd_pc["P values"] = p_val
    return pd_pc.style.background_gradient(cmap="Blues")


def get_hist_comparison(data, readout_col, hue_order=None, treatment_col_name='treatment'):
    '''
    # Parameters
    hue_order: which feature to color by

    # Note:
    Please make sure the clusters column is labeled as 'clusters'
    '''
    fig, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(12, 4))
    sns.kdeplot(
        ax=ax1, x=data[readout_col], hue=data[treatment_col_name], fill=True, alpha=0.2
    )
    ax1.set(title=readout_col + " by Treatment")
    if hue_order is not None:
        sns.kdeplot(
            ax=ax2,
            x=data[readout_col],
            hue=data["clusters"],
            hue_order=hue_order,
            fill=True,
            alpha=0.2,
        )
        ax2.set(title=readout_col + " by Clusters")
    else:
        sns.kdeplot(
            ax=ax2, x=data[readout_col], hue=data["clusters"], fill=True, alpha=0.2
        )
        ax2.set(title=readout_col + " by Clusters")


if __name__ == "__main__":
    pass
