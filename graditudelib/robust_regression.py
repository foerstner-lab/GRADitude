import pandas as pd
import numpy as np
from numpy import inf
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.linear_model import RANSACRegressor


def robust_regression(
        ref_feature_count_table, concentration_table, number_of_outliers, output_file):
    ref_feature_count_table_df = read_table(ref_feature_count_table)
    concentration_table_df = read_table_concentration(concentration_table)
    gradient_file_combined = merging_dict(ref_feature_count_table_df, concentration_table_df)
    read_grad_value, read_concentration_value, gradient_file = \
        modify_input(gradient_file_combined)
    common_ercc_df = regression(read_grad_value, read_concentration_value, gradient_file,
                                number_of_outliers)
    df_common_ercc = common_ercc(common_ercc_df)
    new_ref_table(df_common_ercc, ref_feature_count_table_df, output_file)


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
    concentration_serie = pd.Series(concentration_list)
    combined_df = pd.DataFrame.from_dict(combined_dict)
    combined_df.loc[:, 'Concentration'] = concentration_serie.values
    combined_df.reset_index(inplace=True)
    return combined_df


def modify_input(gradient_file):
    read_grad_value = gradient_file[list(filter(
        lambda col: col.startswith("Grad_47"), gradient_file.columns))]
    read_concentration_value = gradient_file[list(filter(
        lambda col: col.startswith("Concentration"), gradient_file.columns))]
    return read_grad_value, read_concentration_value, gradient_file


def regression(read_grad_value, read_concentration_value, gradient_file,
               number_of_outliers):
    table_with_outliers = {}
    key = gradient_file.ix[:, 0].ravel()
    concentration_log10 = np.log10(read_concentration_value.values)
    for gradient in read_grad_value:
        read_grad_value_log10 = np.log10(read_grad_value[gradient])
        read_grad_value_log10[read_grad_value_log10 == -inf] = 0
        concentration_log10[concentration_log10 == -inf] = 0
        x_values = read_grad_value_log10.reshape(len(key), 1)
        y_values = concentration_log10.reshape(len(key), 1)
        clt_ransac = linear_model.RANSACRegressor(linear_model.LinearRegression())
        clt_ransac = clt_ransac.fit(x_values, y_values)
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
        plt.title(gradient + '\n'
                             "The intercept values is " +
                  str(clt_ransac.estimator_.intercept_)
                  + '\n' +
                  "The slope values is " +
                  str(clt_ransac.estimator_.coef_),
                  fontsize=10)
        plt.savefig(gradient)
        plt.close()
        outliers_keys = key[index[-number_of_outliers:]]
        table_with_outliers[gradient] = outliers_keys
    outliers_df = pd.DataFrame(table_with_outliers)
    return outliers_df


def common_ercc(csv_file):
    unique_vals = pd.Series(csv_file.values.ravel()).unique()
    data_dict = {}
    for val in unique_vals:
        row = []
        for value in csv_file.columns:
            row.append((csv_file[value] == val).sum())
        data_dict[val] = row

    results_df = pd.DataFrame(data_dict).T
    results_df.columns = csv_file.columns
    results_df = results_df.sum(axis=1).sort_values(ascending=False)
    return results_df


def new_ref_table(csv_common_ercc, ref_table, output_file):
    ercc_table_final = []
    csv_common_ercc_df = pd.Series.to_frame(csv_common_ercc)
    new_csv_common_ercc_df = csv_common_ercc_df.reset_index()
    new_csv_common_ercc_df.columns = ['keys', 'values']
    selected_df = new_csv_common_ercc_df[~(new_csv_common_ercc_df['values'] >= 18)]
    selected_df.reset_index(drop=True, inplace=True)
    ref_table_df = pd.DataFrame.from_dict(ref_table, orient='index')
    my_keys = selected_df['keys'].tolist()
    for index, row in ref_table_df.iterrows():
        if index in my_keys:
            ercc_table_final.append(row)
    df_with_selected_ercc = pd.DataFrame(ercc_table_final)
    df_with_selected_ercc.to_csv(output_file)
