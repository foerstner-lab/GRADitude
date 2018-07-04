import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import BoxZoomTool, ResetTool, PanTool
from bokeh.models import WheelZoomTool


def plot_kinetics(feature_count_table,
                  gene_name, feature_count_start_column):
    feature_count_table_df = pd.read_table(feature_count_table)

    gene_row = _extract_gene_row(feature_count_table_df, gene_name)
    value_gene_row = _extract_value_gene_row(gene_row, feature_count_start_column).values.T.tolist()
    _plot_gene_html(value_gene_row, gene_name)


def _extract_gene_row(feature_count_table_df, gene_name):
    return feature_count_table_df.loc[feature_count_table_df['Gene'] == gene_name]


def _extract_value_gene_row(gene_row, feature_count_start_column):
    return gene_row.iloc[:, feature_count_start_column:]


def _plot_gene_html(counting_value_list, gene_name):
    output_file(gene_name + '.html')
    plot_html = figure(title=gene_name,
                       x_axis_label='Fraction number',
                       y_axis_label='Normalized read counts', tools=[BoxZoomTool(), ResetTool(), PanTool(),
                                                                    WheelZoomTool()])
    plot_html.toolbar.logo = None
    y_axis = range(1, 22)
    plot_html.line(y_axis, counting_value_list)
    show(plot_html)


def _plot_gene_png(counting_value_list, gene_name):
    output_file(gene_name + '.html')
    plot_html = figure(title="GRAD-seq" +
                             '\n' + gene_name,
                       x_axis_label='Fraction number',
                       y_axis_label='Normalized read counts')
    y_axis = range(0, 21)
    plot_html.line(y_axis, counting_value_list)
    show(plot_html)
