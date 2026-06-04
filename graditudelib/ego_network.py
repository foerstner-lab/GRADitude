import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


# Define a function to draw a clean "Ego Network"
def plot_ego_network(correlation_table, central_node, output_plot,  color):
    """
        Plot an ego network for a selected RNA or protein.

        The input table should contain correlation partners as row names and
        one column with correlation values. If the column is not named
        'Correlation', the first numeric column is used.
        """
    try:
        # Load the specific top-20 list you just made
        df = pd.read_csv(correlation_table, index_col=0, header=0, names=['Correlation'])

        # Create graph
        G = nx.Graph()

        # Add edges from the center node to everyone in the list
        for partner, row in df.iterrows():
            if partner != central_node:  # Skip self-loop
                G.add_edge(central_node, partner, weight=row['Correlation'])

        # Draw
        plt.figure(figsize=(6, 6))
        pos = nx.spring_layout(G, k=0.5)  # k regulates the distance between nodes

        # Draw center node large
        nx.draw_networkx_nodes(G, pos, nodelist=[central_node], node_color=color, node_size=2500)
        # Draw partners smaller
        nx.draw_networkx_nodes(G, pos, nodelist=[n for n in G.nodes if n != central_node], node_color='lightgrey',
                               node_size=1000)

        # Draw edges
        nx.draw_networkx_edges(G, pos, width=2, alpha=0.5)

        # Labels
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

        plt.title(f"Interaction neighborhood: {central_node}")
        plt.axis('off')
        plt.savefig(output_plot, dpi=300)
        plt.show()
        print(f"Saved {output_plot}")

    except Exception as e:
        print(f"Skipped {output_plot}: {e}")


# Run for ssrA (use Orange to match your cluster colors if possible)
plot_ego_network("GRADitude/output/ssrA_top_correlations.csv", "ssrA", "Figure_3_12_ssrA.png", "orange")

# Run for ryeG (use Yellow/Green if it was ribosomal)
plot_ego_network("GRADitude/output/ryeG_top_correlations.csv", "ryeG", "Figure_3_12_ryeG.png", "green")