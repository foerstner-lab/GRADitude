from sklearn.decomposition import PCA
from sklearn.decomposition import IncrementalPCA
import pandas as pd
from bokeh.plotting import figure, save, ColumnDataSource
from bokeh.models import HoverTool, BoxZoomTool, ResetTool, PanTool
from bokeh.models import WheelZoomTool, TapTool, OpenURL
import bokeh.palettes


def pca_analysis(feature_count_table, feature_count_start_column):
    feature_count_table_df = pd.read_table(feature_count_table)
    value_matrix = _extract_value_matrix(feature_count_table_df,
                                         feature_count_start_column)
    result_pca = perform_pca(value_matrix)
    plot(feature_count_table_df, result_pca)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):]


def perform_pca(normalized_values):
    pca = PCA(n_components=2)
    pca.fit(normalized_values)
    PCA(copy=True, iterated_power='auto', n_components=2, random_state=None,
        svd_solver='auto', tol=0.0, whiten=False)
    print(pca.explained_variance_ratio_)
    incremental_pca = IncrementalPCA(n_components=2, batch_size=3)
    incremental_pca.fit(normalized_values)
    IncrementalPCA(batch_size=4, copy=True, n_components=2, whiten=False)
    return incremental_pca.transform(normalized_values)


def plot(read_counting_table, result_pca):
    read_counting_table["PCA-component_1"] = [pos[0] for pos in result_pca]
    read_counting_table["PCA-component_2"] = [pos[1] for pos in result_pca]

    read_counting_table["Attributes_split"] = \
        read_counting_table["Attributes"].apply(lambda attr: dict(
            [key_value_pair.split("=")
             for key_value_pair in attr.split(";")]))

    hower_data = dict(
        x=read_counting_table["PCA-component_1"],
        y=read_counting_table["PCA-component_2"],
        feature=read_counting_table["Feature"],
        cluster_label=read_counting_table["Cluster_label"])

    for feature in ["gene", "product", "ID", "type", "ncrna_class",
                    "sRNA_type", "Name", "pseudo"]:
        read_counting_table[feature] = \
            read_counting_table["Attributes_split"].apply(
                lambda attributes: attributes.get(feature, "-"))
        hower_data[feature] = read_counting_table[feature]

    source = ColumnDataSource(hower_data)

    hover = HoverTool(tooltips=[
        ("Gene", "@gene"),
        ("Product", "@product"),
        ("ID", "@ID"),
        ("Type", "@type"),
        ("Ncrna_class", "@ncrna_class"),
        ("sRNA_type", "@sRNA_type"),
        ("Name", "@Name"),
        ("Pseudo", "@pseudo"),
        ("Feature", "@feature"),
        ("Cluster label", "@cluster_label")])

    p = figure(plot_width=700, plot_height=700,
               tools=[hover, BoxZoomTool(), ResetTool(), PanTool(),
                      WheelZoomTool(), "tap"],
               title="Grad-Seq PCA-RNA-Seq", logo=None)

    default_color = "#4271FF"
    # highlight_color = "#FF9C38"
    color = default_color

    # color = read_counting_table.apply(
    #     _color, args=(srnas_and_list_names,), axis=1)

    color_palette = bokeh.palettes.viridis(
        len(read_counting_table["Cluster_label"].unique()))
    color = read_counting_table["Cluster_label"].apply(
        lambda lable: color_palette[lable])

    p.circle("x", "y", source=source, size=5, alpha=0.7, color=color)

    url = "http://www.uniprot.org/uniprot/@protein_id"
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    p.xaxis.axis_label = "Component 1"
    p.yaxis.axis_label = "Component 2"

    save(p)








