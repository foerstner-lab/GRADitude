import pandas as pd

print("Loading matrix... this may take a minute.")
# Use chunksize if the file is extremely large,
# but for 4000x4000 a standard read should work if you have 8GB+ RAM
df = pd.read_table("RNA_correlation_matrix.tsv", index_col=0)

# 1. Process ssrA
if 'ssrA' in df.columns:
    ssrA_hits = df['ssrA'].sort_values(ascending=False).head(20)
    print("\nTop 20 genes co-sedimenting with ssrA:")
    print(ssrA_hits)
    ssrA_hits.to_csv("ssrA_top_correlations.csv")
else:
    print("ssrA not found in matrix index.")

# 2. Process ryeG
if 'ryeG' in df.columns:
    ryeG_hits = df['ryeG'].sort_values(ascending=False).head(20)
    print("\nTop 20 genes co-sedimenting with ryeG:")
    print(ryeG_hits)
    ryeG_hits.to_csv("ryeG_top_correlations.csv")