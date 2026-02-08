import pandas as pd
import os

def extract_cluster_tables(feature_count_table, output_table):
    print(f"--- Processing file: {feature_count_table} ---")

    # 1. Read the table
    # sep=None allows Python to automatically detect commas or tabs
    try:
        df = pd.read_csv(feature_count_table, sep=None, engine='python')
    except Exception as e:
        print(f"Critical error reading the file: {e}")
        return

    # 2. Check if the Cluster_label column exists
    if 'Cluster_label' not in df.columns:
        print("Error: The column 'Cluster_label' was not found.")
        print(f"Available columns: {list(df.columns)}")
        return

    # 3. Find unique clusters (e.g., 0, 1, 2...)
    unique_clusters = sorted(df['Cluster_label'].unique())
    print(f"Clusters found: {unique_clusters}")

    # 4. Prepare the base filename
    # Splits "results/heatmap_data.tsv" into "results/heatmap_data" and ".tsv"
    base_name, ext = os.path.splitext(output_table)

    # 5. Loop through each cluster and save the file
    for cluster_id in unique_clusters:
        # Filter the rows belonging to the specific cluster
        df_cluster = df.loc[df['Cluster_label'] == cluster_id]

        # Create the dynamic filename
        final_name = f"{base_name}_cluster_{cluster_id}{ext}"

        # --- SAVE SETTINGS ---
        # index=False: Do not save the row numbers (0, 1, 2...)
        # sep='\t': Use tab separation (standard for Grad-seq tools)
        # header=True: KEEP the header! (Essential for heatmaps to know column names)
        df_cluster.to_csv(final_name, index=False, sep='\t', header=True)

        print(f" -> Saved full table: {final_name} (Rows: {len(df_cluster)})")

    print("--- Done! ---")
