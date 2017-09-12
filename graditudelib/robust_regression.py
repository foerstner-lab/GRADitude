import pandas as pd
import numpy as np
from numpy import inf
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.linear_model import RANSACRegressor


def robust_regression(
        # TODO don't print the file but only return and use directly as input for the new functions
        ref_feature_count_table, concentration_table, output_file, number_of_outliers,
        output_plot):
    ref_feature_count_table_df = read_table(ref_feature_count_table)
    concentration_table_df = read_table_concentration(concentration_table)
    merging_dict(ref_feature_count_table_df, concentration_table_df)
    read_grad_value, read_concentration_value, gradient_file = \
        modify_input('../data/ERCC_TABLE_reads+concentration.csv')
    clt_ransac, x_values, y_values, key = regression(read_grad_value, read_concentration_value,
                                                     gradient_file)
    plot_and_list_outlier(clt_ransac, x_values, y_values, key, number_of_outliers, output_file,
                          output_plot)


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
    table_reads_and_concentration = pd.concat([combined_df, concentration_df])

    table_reads_and_concentration.to_csv \
        ('ERCC_TABLE_reads+concentration.csv', sep='\t')


def modify_input(gradient_file):
    table = pd.read_csv(gradient_file, sep=',', index_col=False, header=0)
    read_grad_value = table[list(filter(
        lambda col: col.startswith("Grad_47"), table.columns))]
    read_concentration_value = table[list(filter(
        lambda col: col.startswith("Concentration"), table.columns))]
    return read_grad_value, read_concentration_value, table


def regression(read_grad_value, read_concentration_value, gradient_file):
    key = gradient_file.ix[:, 0].ravel()
    concentration_log10 = np.log10(read_concentration_value.values)
    read_grad_value_log10 = np.log10(read_grad_value.ix[:, 0])
    read_grad_value_log10[read_grad_value_log10 == -inf] = 0
    concentration_log10[concentration_log10 == -inf] = 0
    x_values = read_grad_value_log10.reshape(len(key), 1)
    y_values = concentration_log10.reshape(len(key), 1)
    clt_ransac = linear_model.RANSACRegressor(linear_model.LinearRegression())
    clt_ransac = clt_ransac.fit(x_values, y_values)
    return clt_ransac, x_values, y_values, key


def plot_and_list_outlier(clt_ransac, x_values, y_values, key,
                          number_of_outliers, output_file, output_plot):
    fig, axes = plt.subplots(ncols=2)
    axes[0].scatter(x_values, y_values, c='g')
    axes[0].set_xlabel('Reads')
    axes[0].set_ylabel('Concentration')
    plt.plot(x_values, clt_ransac.predict(x_values), color='blue')
    robust_estimator = RANSACRegressor(random_state=0)
    robust_estimator.fit(x_values, y_values)
    distance_pred = robust_estimator.predict(x_values)
    mean_squared_error = (y_values - distance_pred) ** 2
    index = np.argsort(mean_squared_error.ravel())
    axes[1].scatter(x_values[index[:-number_of_outliers]],
                    y_values[index[:-number_of_outliers]], c='b', label='inliers', alpha=0.2)
    axes[1].scatter(x_values[index[-number_of_outliers:]],
                    y_values[index[-number_of_outliers:]], c='r', label='outliers')
    axes[1].set_xlabel('Reads')
    axes[1].legend(loc=2)
    plt.title('first_gradient' + '\n'
                                 "The intercept values is " +
              str(clt_ransac.estimator_.intercept_)
              + '\n' +
              "The slope values is " +
              str(clt_ransac.estimator_.coef_),
              fontsize=10)
    plt.savefig(output_plot)
    outliers_keys = key[index[-number_of_outliers:]]
    outliers_df = pd.DataFrame(outliers_keys)
    outliers_df.to_csv(output_file, index=0,
                       header=['ERCC_to_discard'])
