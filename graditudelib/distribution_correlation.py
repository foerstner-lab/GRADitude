import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def d_c_graph(table_with_correlation_coefficient, percentile, index_table,
              output_plot):
    correlation_df = pd.read_table(table_with_correlation_coefficient)
    correlation_df.set_index(index_table, inplace=True)
    data = correlation_df.apply(pd.Series).unstack().reset_index(drop=True)
    data.hist()
    axes_x = data[~np.isnan(data)]
    plot = np.percentile(axes_x, percentile)
    sns.distplot(axes_x, kde=True, rug=False)
    plt.grid(False)
    plt.axvline(x=plot).set_color("black")
    plt.title("Correlation histogram "
              + '\n' +
              "The percentile value is " +
              str(plot),
              fontsize=10)
    plt.xlabel = "Correlation coefficients"

    plt.ylabel = "Number of entries"
    plt.savefig(output_plot)
    plt.show()
