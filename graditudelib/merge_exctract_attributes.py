import pandas as pd
import numpy as np


def merge_exctracted_attributes(feature_count_table, output_table):
    table = pd.read_csv(feature_count_table, sep='\t')

    # Prefer gene identifiers in this order (works with tutorial_data/gene_wise_extended.csv):
    # gene -> Name -> Parent -> name -> ID
    candidates = ["gene", "Name", "Parent", "name", "ID"]
    present = [c for c in candidates if c in table.columns]

    if not present:
        raise ValueError(
            "Cannot create 'Gene' column. None of these columns were found: "
            f"{', '.join(candidates)}"
        )

    # Start with the first available column and fill missing values from the next ones
    gene_series = table[present[0]]
    for col in present[1:]:
        gene_series = np.where(pd.isna(gene_series), table[col], gene_series)

    table["Gene"] = gene_series
    table.to_csv(output_table, index=None, sep='\t')
