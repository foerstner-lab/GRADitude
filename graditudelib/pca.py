from sklearn.decomposition import PCA
from sklearn.decomposition import IncrementalPCA
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from bokeh.plotting import figure, output_file, save, ColumnDataSource
from bokeh.models import HoverTool, BoxZoomTool, ResetTool, PanTool
from bokeh.models import WheelZoomTool, TapTool, OpenURL
import bokeh.palettes


def pca_analysis(feature_count_table, feature_count_start_column,
                 pseudo_count, number_of_clusters, scaling_method, clustering_method, file_output, plot_output):
    feature_count_table_df = pd.read_table(feature_count_table)
    value_matrix = _extract_value_matrix(feature_count_table_df,
                                         feature_count_start_column)
    attribute_matrix = _extract_attributes(feature_count_table_df,
                                           feature_count_start_column)
    normalized_table = normalize_values(value_matrix, scaling_method, pseudo_count)
    result_pca = perform_pca(normalized_table)
    if clustering_method == 'k-means':
        table_with_attributes = k_means_clustering(result_pca, normalized_table, number_of_clusters, attribute_matrix)
        table_with_attributes.to_csv(file_output, sep='\t', index=0)
    elif clustering_method == 'hierarchical_clustering':
        table_with_attributes = hierarchical_clustering(result_pca, normalized_table, number_of_clusters,
                                                        attribute_matrix)
        table_with_attributes.to_csv(file_output, sep='\t', index=0)
    elif clustering_method == 'DBSCAN':
        table_with_attributes = dbscan_clustering(result_pca, normalized_table,
                                                  attribute_matrix)
        table_with_attributes.to_csv(file_output, sep='\t', index=0)

    plot_with_clusters(table_with_attributes, result_pca, plot_output)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):]


def _extract_attributes(feature_count_table_df,
                        feature_count_start_column):
    return feature_count_table_df.iloc[:, : int(feature_count_start_column)]


def perform_pca(value_matrix):
    pca = PCA(n_components=2)
    pca.fit(value_matrix)
    PCA(copy=True, iterated_power='auto', n_components=2, random_state=None,
        svd_solver='auto', tol=0.0, whiten=False)
    print(pca.explained_variance_ratio_)
    incremental_pca = IncrementalPCA(n_components=2, batch_size=3)
    incremental_pca.fit(value_matrix)
    IncrementalPCA(batch_size=4, copy=True, n_components=2, whiten=False)
    return incremental_pca.transform(value_matrix)


def normalize_values(values_matrix, scaling_method, pseudo_count):
    if scaling_method == "no_normalization":
        normalized_values = values_matrix
    elif scaling_method == "log2":
        normalized_values = values_matrix.applymap(
            lambda val: val + pseudo_count).applymap(np.log2)
    elif scaling_method == "log10":
        normalized_values = values_matrix.applymap(
            lambda val: val + pseudo_count).applymap(np.log10)
    elif scaling_method == "normalized_to_max":
        values_matrix = values_matrix.fillna(lambda x: 0)
        row_max_values = values_matrix.max(axis=1)
        normalized_values = values_matrix.divide(
            row_max_values, axis=0)
        normalized_values = pd.DataFrame(normalized_values).fillna(0)
    elif scaling_method == "normalized_to_range":
        row_max_values = values_matrix.max(axis=1)
        row_min_values = values_matrix.min(axis=1)
        normalized_values = values_matrix.subtract(
            row_min_values, axis=0).divide(row_max_values, axis=0)
    else:
        print("Normalization method not known")
    return normalized_values


def k_means_clustering(result_pca, values_matrix, number_of_clusters, attribute_matrix):
    values_matrix.as_matrix()
    k_means = KMeans(n_clusters=number_of_clusters, random_state=0)
    k_means.fit(result_pca)
    labels = k_means.labels_
    pd.DataFrame(data=labels, columns=['cluster'])
    values_matrix["Cluster_label"] = pd.Series(k_means.labels_).astype(int)
    table_with_clusters = pd.concat([attribute_matrix, values_matrix],
                                    axis=1)
    return table_with_clusters


def hierarchical_clustering(result_pca, values_matrix, number_of_clusters, attribute_matrix):
    h_clustering = AgglomerativeClustering(n_clusters=number_of_clusters,
                                           affinity="euclidean", linkage="ward")
    h_clustering.fit(result_pca)
    labels = h_clustering.labels_
    pd.DataFrame(data=labels, columns=['cluster'])
    values_matrix["Cluster_label"] = pd.Series(h_clustering.labels_).astype(int)
    table_with_clusters = pd.concat([attribute_matrix, values_matrix],
                                    axis=1)
    return table_with_clusters


def dbscan_clustering(result_pca, values_matrix, attribute_matrix):
    dbscan = DBSCAN(eps=0.5, min_samples=42)
    dbscan.fit_predict(result_pca)
    labels = dbscan.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    print('Estimated number of clusters: %d' % n_clusters_)
    pd.DataFrame(data=labels, columns=['cluster'])
    values_matrix["Cluster_label"] = pd.Series(dbscan.labels_).astype(int)
    table_with_clusters = pd.concat([attribute_matrix, values_matrix],
                                    axis=1)
    return table_with_clusters


def plot_with_clusters(read_counting_table, pca_result, output_file_path):
    read_counting_table["pca-component_1"] = [pos[0] for pos in pca_result]
    read_counting_table["pca-component_2"] = [pos[1] for pos in pca_result]

    read_counting_table["Attributes_split"] = \
        read_counting_table["Attributes"].apply(lambda attr: dict(
            [key_value_pair.split("=")
             for key_value_pair in attr.split(";")]))

    hower_data = dict(
        x=read_counting_table["pca-component_1"],
        y=read_counting_table["pca-component_2"],
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
               title="Grad-Seq PCA RNA-Seq", logo=None)

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

    output_file(output_file_path)
    save(p)
