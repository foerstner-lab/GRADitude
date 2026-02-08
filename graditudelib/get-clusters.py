import pandas as pd
import os


def extract_cluster_lists(feature_count_table, output_table):
    """
    Splits a table into multiple files based on the 'Cluster_label' column.
    It automatically detects the number of clusters.
    """
    # 1. Read the table
    df = pd.read_csv(feature_count_table, sep='\t')

    # 2. Check if the required column exists
    if 'Cluster_label' not in df.columns:
        raise ValueError("The column 'Cluster_label' was not found in the table.")

    # 3. Automatically find all unique cluster IDs (e.g., 0, 1, 2... 8)
    unique_clusters = sorted(df['Cluster_label'].unique())
    print(f"Found {len(unique_clusters)} unique clusters: {unique_clusters}")

    # 4. Prepare the filename base (e.g., split "results/list.txt" into "results/list" and ".txt")
    base_name, ext = os.path.splitext(output_table)

    # 5. Loop through every cluster found
    for cluster_id in unique_clusters:
        # Filter rows belonging to this cluster
        sub_df = df[df['Cluster_label'] == cluster_id]

        # Extract only the first column (Gene names/IDs)
        gene_list = sub_df.iloc[:, 0]

        # Create the dynamic filename: "output_cluster_1.txt"
        final_output_name = f"{base_name}_cluster_{cluster_id}{ext}"

        # Save the file (no header, no index, ready for GO analysis)
        gene_list.to_csv(final_output_name, index=None, sep='\t', header=None)
        print(f"Cluster {cluster_id} saved to: {final_output_name}")