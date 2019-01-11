import pandas as pd
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import numpy as np

from bokeh.plotting import figure, ColumnDataSource, show, output_file
from bokeh.models import HoverTool, BoxZoomTool, ResetTool, PanTool, DataTable, TableColumn
from bokeh.models import WheelZoomTool, CustomJS, Button, TapTool, OpenURL
from bokeh.layouts import row, column


def interactive_plot(table_with_clusters, feature_count_start_column, feature_count_end_column,
                     dimension_reduction_algorithm, perplexity, url_link,
                     output_file_):
    read_counting_table = pd.read_table(table_with_clusters, sep='\t')
    value_matrix = _extract_value_matrix(read_counting_table, feature_count_start_column, feature_count_end_column)
    if dimension_reduction_algorithm == "t-SNE":
        t_sne_result = perform_t_sne(value_matrix, perplexity)
        plot_t_sne(read_counting_table, t_sne_result, url_link, output_file_)
    elif dimension_reduction_algorithm == "PCA":
        pca_result = perform_pca(value_matrix)
        plot_pca(read_counting_table, pca_result, url_link, output_file_)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column, feature_count_end_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):feature_count_end_column]


def perform_t_sne(normalized_values, perplexity):
    model = TSNE(n_components=2, random_state=0, perplexity=perplexity)
    np.set_printoptions(suppress=True)
    tsne_result = model.fit_transform(normalized_values)
    return tsne_result


def perform_pca(normalized_values):
    model = PCA(n_components=3, random_state=0)
    np.set_printoptions(suppress=True)
    pca_result = model.fit_transform(normalized_values)
    return pca_result


def plot_t_sne(read_counting_table, tsne_result, url_link, output_file_):
    read_counting_table["t-SNE-component_1"] = [pos[0] for pos in tsne_result]
    read_counting_table["t-SNE-component_2"] = [pos[1] for pos in tsne_result]

    read_counting_table["Attributes_split"] = \
        read_counting_table["Attributes"].apply(lambda attr: dict(
            [key_value_pair.split("=")
             for key_value_pair in attr.split(";")]))

    hower_data = dict(
        x=read_counting_table["t-SNE-component_1"],
        y=read_counting_table["t-SNE-component_2"],
        feature=read_counting_table["Feature"],
        cluster_label=read_counting_table["Cluster_label"],
        gene=read_counting_table["Gene"],
        attribute=read_counting_table["Attributes"])

    source = ColumnDataSource(hower_data)
    hover = HoverTool(tooltips=[
        ("Gene", "@gene"),
        ("Feature", "@feature"),
        ("Cluster label", "@cluster_label")])

    p = figure(plot_width=900, plot_height=900,
               tools=[hover, BoxZoomTool(), ResetTool(), PanTool(),
                      WheelZoomTool(), "lasso_select", "tap"],
               output_backend="webgl", lod_threshold=100,
               title="Grad-Seq t-SNE RNA-Seq")
    p.toolbar.logo = None
    p.circle("x", "y", source=source, size=7, alpha=3, line_color="grey", color="grey")
    p.yaxis.axis_label_text_font_size = "15pt"
    p.xaxis.axis_label_text_font_size = "15pt"
    p.title.text_font_size = '15pt'
    url = url_link
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    p.xaxis.axis_label = "Dimension 1"
    p.yaxis.axis_label = "Dimension 2"
    s2 = ColumnDataSource(data=dict(x=[], y=[]))
    p2 = figure(plot_width=300, plot_height=300,
                tools="", title="Zoom", output_backend="webgl", lod_threshold=100)
    p2.toolbar.logo = None
    p2.circle('x', 'y', source=s2, alpha=0.6)
    columns = [
        TableColumn(field="gene", title="Genes"),
        TableColumn(field="feature", title="Feature"),
        TableColumn(field="attribute", title="Attributes")
    ]
    data_table = DataTable(source=source, columns=columns, width=450, height=800, fit_columns=True)
    savebutton = Button(label="Save", button_type="success")
    source.selected.js_on_change('indices', CustomJS(args=dict(s1=source, s2=s2), code="""
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

    savebutton.callback = CustomJS(args=dict(source_data=source), code="""
        var inds = source_data.selected['1d'].indices;
        var data = source_data.data;
        console.log("inds", inds);
        console.log("data", data);
        var out = "Features\\tGene\\tAttributes + \\n";
        for (i = 0; i < inds.length; i++) {
                 out += data['feature'][inds[i]] + "\\t" + data['gene'][inds[i]] + "\\t" +  data['attribute'][inds[i]] + "\\n";
        }
        var file = new Blob([out], {type: 'text/plain'});
        var elem = window.document.createElement('a');
        elem.href = window.URL.createObjectURL(file);
        elem.download = 'selected-data.csv';
        document.body.appendChild(elem);
        elem.click();
        document.body.removeChild(elem);
        """)

    output_file(output_file_ + ".html", title="Grad-seq t-SNE")
    layout = row(p, data_table, column(p2, savebutton))
    show(layout)


def plot_pca(read_counting_table, pca_result, url_link, output_file_):
    read_counting_table["PCA-component_1"] = [pos[0] for pos in pca_result]
    read_counting_table["PCA-component_2"] = [pos[1] for pos in pca_result]

    read_counting_table["Attributes_split"] = \
        read_counting_table["Attributes"].apply(lambda attr: dict(
            [key_value_pair.split("=")
             for key_value_pair in attr.split(";")]))

    hower_data = dict(
        x=read_counting_table["PCA-component_1"],
        y=read_counting_table["PCA-component_2"],
        feature=read_counting_table["Feature"],
        cluster_label=read_counting_table["Cluster_label"],
        gene=read_counting_table["Gene"],
        attribute=read_counting_table["Attributes"])

    source = ColumnDataSource(hower_data)
    hover = HoverTool(tooltips=[
        ("Gene", "@gene"),
        ("Feature", "@feature"),
        ("Cluster label", "@cluster_label")])

    p = figure(plot_width=900, plot_height=900,
               tools=[hover, BoxZoomTool(), ResetTool(), PanTool(),
                      WheelZoomTool(), "lasso_select", "tap"],
               output_backend="webgl", lod_threshold=100,
               title="Grad-Seq PCA RNA-Seq")
    p.toolbar.logo = None
    p.circle("x", "y", source=source, size=7, alpha=3, line_color="grey", color="grey")
    p.yaxis.axis_label_text_font_size = "15pt"
    p.xaxis.axis_label_text_font_size = "15pt"
    p.title.text_font_size = '15pt'
    url = url_link
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    p.xaxis.axis_label = "Component 1"
    p.yaxis.axis_label = "Component 2"
    s2 = ColumnDataSource(data=dict(x=[], y=[]))
    p2 = figure(plot_width=300, plot_height=300,
                tools="", title="Zoom", output_backend="webgl", lod_threshold=100)
    p2.toolbar.logo = None
    p2.circle('x', 'y', source=s2, alpha=0.6)
    columns = [
        TableColumn(field="gene", title="Genes"),
        TableColumn(field="feature", title="Feature"),
        TableColumn(field="attribute", title="Attributes")
    ]
    data_table = DataTable(source=source, columns=columns, width=450, height=800, fit_columns=True)
    savebutton = Button(label="Save", button_type="success")
    source.selected.js_on_change('indices', CustomJS(args=dict(s1=source, s2=s2), code="""
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

    savebutton.callback = CustomJS(args=dict(source_data=source), code="""
        var inds = source_data.selected['1d'].indices;
        var data = source_data.data;
        console.log("inds", inds);
        console.log("data", data);
        var out = "Features\\tGene\\tAttributes + \\n";
        for (i = 0; i < inds.length; i++) {
                 out += data['feature'][inds[i]] + "\\t" + data['gene'][inds[i]] + "\\t" +  data['attribute'][inds[i]] + "\\n";
        }
        var file = new Blob([out], {type: 'text/plain'});
        var elem = window.document.createElement('a');
        elem.href = window.URL.createObjectURL(file);
        elem.download = 'selected-data.csv';
        document.body.appendChild(elem);
        elem.click();
        document.body.removeChild(elem);
        """)

    output_file(output_file_ + ".html", title="Grad-seq PCA")
    layout = row(p, data_table, column(p2, savebutton))
    show(layout)
