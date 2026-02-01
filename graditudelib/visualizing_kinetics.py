import pandas as pd
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show
from bokeh.models import BoxZoomTool, ResetTool, PanTool
from bokeh.models import WheelZoomTool
from bokeh.models import FixedTicker


def plot_kinetics(feature_count_table, feature_count_start_column, feature_count_end_column,
                  gene_name, output_format,  y_label ):
    feature_count_table_df = pd.read_table(feature_count_table)

    gene_row = _extract_gene_row(feature_count_table_df, gene_name)
    value_gene_row = _extract_value_gene_row(gene_row, feature_count_start_column,
                                             feature_count_end_column).iloc[0].tolist()
    if output_format == "pdf":
        _plot_gene_png(value_gene_row, gene_name, y_label)
    else:
        _plot_gene_html(value_gene_row, gene_name, y_label)


def _extract_gene_row(feature_count_table_df, gene_name):
    return feature_count_table_df.loc[feature_count_table_df['Gene'] == gene_name]


def _extract_value_gene_row(gene_row, feature_count_start_column, feature_count_end_column):
    return gene_row.iloc[:, feature_count_start_column:feature_count_end_column]


def _plot_gene_html(counting_value_list, gene_name, y_label):
    output_file(gene_name + '.html')
    plot_html = figure(title=gene_name,
                       x_axis_label='Fraction number',
                       y_axis_label= y_label,
                       tools=[BoxZoomTool(), ResetTool(), PanTool(),
                              WheelZoomTool()])
    plot_html.xaxis.ticker = FixedTicker(
        ticks=list(range(1, len(counting_value_list) + 1)))
    plot_html.yaxis.axis_label_text_font_size = "12pt"
    plot_html.xaxis.axis_label_text_font_size = "12pt"
    plot_html.title.text_font_size = '15pt'
    plot_html.toolbar.logo = None
    y_axis = list(range(1, len(counting_value_list) + 1))
    plot_html.line(y_axis, counting_value_list)
    show(plot_html)


def _plot_gene_png(counting_value_list, gene_name, y_label):
    x = list(range(1, len(counting_value_list) + 1))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.plot(x, counting_value_list, linewidth=2)
    ax.set_xticks(x)
    #plt.grid(True)
    plt.xlabel('Fraction number', fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.title(gene_name, fontsize=18)
    plt.savefig(gene_name + '.pdf', format='pdf', bbox_inches='tight')
