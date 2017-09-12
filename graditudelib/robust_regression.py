import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from numpy import inf
from sklearn.linear_model import RANSACRegressor


def robust_regression(
        ref_feature_count_table, concentration_table, output_file, number_of_outliers):
    ref_feature_count_table_df = read_table(ref_feature_count_table)
    concentration_table_df = read_table_concentration(concentration_table)
    merging_dict(ref_feature_count_table_df, concentration_table_df)
    outliers('../data/ERCC_TABLE_reads+concentration.csv', number_of_outliers)


def read_table(ref_feature_count_table):
    ref_feature_count_table_dict = {}
    ref_feature_count_table_df = pd.read_table(ref_feature_count_table, sep=',')
    for index, row in ref_feature_count_table_df.iterrows():
        key = row[0][:row[0].index(' ')]
        ref_feature_count_table_dict[key] = row
    return ref_feature_count_table_dict


def read_table_concentration(concentration_table):
    new_dict_for_conc_table = {}
    concentration_table_df = pd.read_table(concentration_table)
    for index, row in concentration_table_df.iterrows():
        new_dict_for_conc_table[row[1]] = row
    return new_dict_for_conc_table


def merging_dict(ref_feature_count_table_dict, new_dict_for_conc_table):
    combined_dict = {}
    concentration_list = []
    for key in ref_feature_count_table_dict:
        reads = ref_feature_count_table_dict[key][1:]
        concentration = new_dict_for_conc_table[key][4]
        for gradient, val in reads.iteritems():
            if gradient not in combined_dict:
                combined_dict[gradient] = {}
            combined_dict[gradient][key] = val
        concentration_list.append(concentration)
    concentration_df = pd.DataFrame(concentration_list)
    combined_df = pd.DataFrame.from_dict(combined_dict)
    table_with_reads_and_concentration = pd.concat([combined_df, concentration_df])

    table_with_reads_and_concentration.to_csv\
        ('ERCC_TABLE_reads+concentration.csv', sep='\t')


def outliers(gradient_file, number_of_outliers):
    table = pd.read_csv(gradient_file, sep=',', index_col=False, header=0)
    read_grad_value = table[list(filter(
        lambda col: col.startswith("Grad_47"), table.columns))]
    read_concentration_value = table[list(filter(
        lambda col: col.startswith("Concentration"), table.columns))]

    key = table.ix[:, 0].ravel()
    y = np.log10(read_concentration_value.values)
    x = np.log10(read_grad_value.ix[:, 0])
    x[x == -inf] = 0
    y[y == -inf] = 0
    x = x.reshape(len(key), 1)
    y = y.reshape(len(key), 1)
    clt_ransac = linear_model.RANSACRegressor(linear_model.LinearRegression())
    clt_ransac.fit(x, y)
    fig, axes = plt.subplots(ncols=2)
    axes[0].scatter(x, y, c='g')
    axes[0].set_xlabel('Reads')
    axes[0].set_ylabel('Concentration')
    plt.plot(x, clt_ransac.predict(x), color='blue')
    robust_estimator = RANSACRegressor(random_state=0)
    robust_estimator.fit(x, y)
    distance_pred = robust_estimator.predict(x)
    mse = (y - distance_pred) ** 2
    index = np.argsort(mse.ravel())
    axes[1].scatter(x[index[:-number_of_outliers]],
                    y[index[:-number_of_outliers]], c='b', label='inliers', alpha=0.2)
    axes[1].scatter(x[index[-number_of_outliers:]],
                    y[index[-number_of_outliers:]], c='r', label='outliers')
    axes[1].set_xlabel('Reads')
    axes[1].legend(loc=2)
    plt.title('first_gradient' + '\n'
                                 "The intercept values is " +
              str(clt_ransac.estimator_.intercept_)
              + '\n' +
              "The slope values is " +
              str(clt_ransac.estimator_.coef_),
              fontsize=10)
    plt.savefig("first_gradient" + 'with_outliers.pdf')
    outliers_keys = key[index[-number_of_outliers:]]
    df = pd.DataFrame(outliers_keys)
    df.to_csv("first_gradient" + 'ERCC_outliers.csv', index=0,
              header=['ERCC_to_discard' + "first_gradient"])
