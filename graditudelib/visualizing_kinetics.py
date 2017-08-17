import pandas as pd
from bokeh.plotting import figure, output_file, show


def plot_kinetics(feature_count_table,
                  gene_name, feature_count_start_column,
                  output_format):
    feature_count_table_df = pd.read_table(feature_count_table)

    gene_row = _extract_gene_row(feature_count_table_df, gene_name)
    value_gene_row = _extract_value_gene_row(gene_row, feature_count_start_column).values.T.tolist()
    _plot_gene_html(value_gene_row, gene_name, output_format, output_file)


def _extract_gene_row(feature_count_table_df, gene_name):
    return feature_count_table_df.loc[feature_count_table_df['Gene'] == gene_name]


def _extract_value_gene_row(gene_row, feature_count_start_column):
    return gene_row.iloc[:, feature_count_start_column:]


def _plot_gene_html(counting_value_list, gene_name, output_format, output_file_):
    output_file_(gene_name + output_format)
    plot_html = figure(title="GRAD-seq" +
                             '\n' + gene_name,
                       x_axis_label='Fraction number',
                       y_axis_label='Read counts')
    y_axis = range(0, 21)
    plot_html.line(y_axis, counting_value_list)
    show(plot_html)