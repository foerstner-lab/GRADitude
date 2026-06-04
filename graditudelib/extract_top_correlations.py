import pandas as pd
from pathlib import Path


def extract_top_correlations(
    correlation_matrix,
    features,
    output_dir,
    top_n=20,
    separator="\t",
):
    print("Loading matrix... this may take a minute.")

    df = pd.read_table(correlation_matrix, index_col=0, sep=separator)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for feature in features:
        if feature in df.columns:
            hits = df[feature].sort_values(ascending=False).head(top_n)
        elif feature in df.index:
            hits = df.loc[feature].sort_values(ascending=False).head(top_n)
        else:
            print(f"{feature} not found in matrix columns or index.")
            continue

        print(f"\nTop {top_n} genes co-sedimenting with {feature}:")
        print(hits)

        output_file = output_dir / f"{feature}_top_correlations.csv"
        hits.to_csv(output_file, header=["Correlation"])

        print(f"Saved {output_file}")