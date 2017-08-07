import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument('gene_name')

    args = parser.parse_args()

    normalized_table = pd.read_csv(args.input_file, sep=',')

    gene_row = normalized_table.loc[normalized_table['Gene'] == args.gene_name]
    selected_row = gene_row[list(filter(lambda col: col.startswith("Grad"), normalized_table.columns))]
    list_ = selected_row.values.T.tolist()
    output_file(args.gene_name + ".html")
    matplotlib.style.use('ggplot')
    p = figure(title="GRAD-seq" + '\n' + args.gene_name, x_axis_label='Fraction number', y_axis_label='Normalized read count')
    fig = plt.figure()
    plt.plot(list_)
    ax = fig.add_subplot(111)
    plt.xlabel("Fraction number")
    plt.ylabel("Normalized read count")
    plt.title(args.gene_name)
    plt.xlim([1, 21])
    plt.savefig(args.gene_name + '.png')
    plt.show()
    plt.close(fig)
    y = range(0, 21)
    p.line(y, list_)
    show(p)

main()
