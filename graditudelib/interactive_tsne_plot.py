import pandas as pd
from sklearn.manifold import TSNE
import numpy as np

from bokeh.plotting import figure, ColumnDataSource, show, output_file
from bokeh.models import HoverTool, BoxZoomTool, ResetTool, PanTool, DataTable, TableColumn
from bokeh.models import WheelZoomTool, CustomJS, Button
from bokeh.layouts import row, column
import bokeh.palettes


def interactive_plot(table_with_clusters, start_column, output_file_):
    read_counting_table = pd.read_table(table_with_clusters, sep='\t')
    value_matrix = _extract_value_matrix(read_counting_table, start_column)
    t_sne_result = perform_t_sne(value_matrix, 30)
    plot_t_sne_using_clustering(read_counting_table, t_sne_result, output_file_)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):-1]


def perform_t_sne(normalized_values, perplexity):
    model = TSNE(n_components=2, random_state=0, perplexity=perplexity)
    np.set_printoptions(suppress=True)
    tsne_result = model.fit_transform(normalized_values)
    return tsne_result


def plot_t_sne_using_clustering(read_counting_table, tsne_result, output_file_):
    read_counting_table["t-SNE-component_1"] = [pos[0] for pos in tsne_result]
    read_counting_table["t-SNE-component_2"] = [pos[1] for pos in tsne_result]

    read_counting_table["Attributes_split"] = \
        read_counting_table["Attributes"].apply(lambda attr: dict(
            [key_value_pair.split("=")
             for key_value_pair in attr.split(";")]))

    color_palette = bokeh.palettes.viridis(
        len(read_counting_table["Cluster_label"].unique()))
    color = read_counting_table["Cluster_label"].apply(
        lambda lable: color_palette[lable])

    hower_data = dict(
        x=read_counting_table["t-SNE-component_1"],
        y=read_counting_table["t-SNE-component_2"],
        feature=read_counting_table["Feature"],
        cluster_label=read_counting_table["Cluster_label"],
        gene=read_counting_table["Gene"],
        color=color,
        attribute=read_counting_table["Attributes"])

    s1 = ColumnDataSource(hower_data)
    hover = HoverTool(tooltips=[
        ("Gene", "@gene"),
        ("Feature", "@feature"),
        ("Cluster label", "@cluster_label")])

    p = figure(plot_width=900, plot_height=900,
               tools=[hover, BoxZoomTool(), ResetTool(), PanTool(),
                      WheelZoomTool(), "lasso_select"], logo=None,
               output_backend="webgl", lod_threshold=100,
               title="Grad-Seq t-SNE RNA-Seq")

    p.scatter("x", "y", source=s1, size=5, alpha=2, color='color')
    s2 = ColumnDataSource(data=dict(x=[], y=[]))
    p2 = figure(plot_width=300, plot_height=300,
                tools="", title="Zoom", logo=None, output_backend="webgl", lod_threshold=100)
    p2.circle('x', 'y', source=s2, alpha=0.6)
    columns = [
        TableColumn(field="gene", title="Genes"),
        TableColumn(field="feature", title="Feature"),
        TableColumn(field="attribute", title="Attributes")
    ]
    data_table = DataTable(source=s1, columns=columns, width=450, height=800, fit_columns=True)
    button = Button(label="Save", button_type="success")
    s1.selected.js_on_change('indices', CustomJS(args=dict(s1=s1, s2=s2), code="""
            var inds = cb_obj.indices;
            var d1 = s1.data;
            var d2 = s2.data;
            d2['x'] = []
            d2['y'] = []
            for (var i = 0; i < inds.length; i++) {
                d2['x'].push(d1['x'][inds[i]])
                d2['y'].push(d1['y'][inds[i]])
            }
            s2.change.emit();
        """)
                             )
    button.callback = CustomJS(args=dict(source_data=s1), code="""
            var inds = source_data.selected['1d'].indices;
            var data = source_data.data;
            var out = read.counting_table.columns;
            for (i = 0; i < inds.length; i++) {
                     out += read_counting_table
            var file = new Blob([out], {type: 'text/plain'});
            var elem = window.document.createElement('a');
            elem.href = window.URL.createObjectURL(file);
            elem.download = 'selected-data.csv';
            document.body.appendChild(elem);
            elem.click();
            document.body.removeChild(elem);
            """)

    output_file(output_file_ + ".html", title="Grad-Seq t-SNE RNA-Seq")
    layout = row(p, data_table, column(p2, button))
    show(layout)
