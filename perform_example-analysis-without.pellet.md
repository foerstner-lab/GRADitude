
```bash

graditude scaling \
    -f GRADitude/input/Norm_100.csv \
    -fc 11 \
    -fe 31 \
    -sm to_max \
    -o GRADitude/without-pellet/scaled_100_to_max.csv

```

graditude plot_kinetics \
    -f GRADitude/without-pellet/scaled_100_to_max.csv \
    -fc 11 \
    -fe 31 \
    -g ssrA \
    -format pdf \
    -yl "Normalized and scaled to max read counts"




graditude plot_kinetics \
    -f GRADitude/input/feature_count_table.csv \
    -fc 11 \
    -fe 31 \
    -g ssrA \
    -format pdf \
    -yl "Raw read counts"


graditude plot_kinetics \
    -f GRADitude/input/scaled_100_to_max.csv \
    -fc 11 \
    -fe 32 \
    -g gcvB \
    -format pdf \
    -yl "Normalized and scaled to max read counts with pellet"

graditude plot_kinetics \
    -f GRADitude/without-pellet/scaled_100_to_max.csv \
    -fc 11 \
    -fe 31 \
    -g gcvB \
    -format pdf \
    -yl "Normalized and scaled to max read counts without pellet"


graditude clustering_elbow \
  -f GRADitude/without-pellet/scaled_100_to_max.csv \
  -fc 11 \
  -fe 31 \
  -min 2 \
  -max 15 \
  -o1 elbow_wcss-without-pellet.pdf \
  -o2 elbow_variance_explained_without-pellet.pdf

graditude silhouette_analysis \
    -c GRADitude/without-pellet/scaled_100_to_max.csv \
    -fc 11 \
    -fe 31 \
    -min 2 \
    -max 10 


graditude clustering \
    -f GRADitude/without-pellet/scaled_100_to_max.csv \
    -fc 11 \
    -fe 31 \
    -nc 4 \
    -p 1 \
    -cm 'k-means' \
    -sm no_normalization \
    -o GRADitude/without-pellet/k-means_100_max_4_cl.csv

graditude extract_cluster_tables \
    -f GRADitude/without-pellet/k-means_100_max_4_cl.csv \
    -o GRADitude/without-pellet/gene_list.csv



graditude heatmap \
    -f GRADitude/without-pellet/gene_list_cluster_0.csv \
    -fc 11 \
    -fe 31 \
    -label "Gene" \
    -o GRADitude/without-pellet/heatmap_CLUSTER1.pdf


graditude heatmap \
    -f GRADitude/without-pellet/gene_list_cluster_1.csv \
    -fc 11 \
    -fe 31 \
    -label "Gene" \
    -o GRADitude/without-pellet/heatmap_CLUSTER2.pdf


graditude heatmap \
    -f GRADitude/without-pellet/gene_list_cluster_2.csv \
    -fc 11 \
    -fe 31 \
    -label "Gene" \
    -o GRADitude/without-pellet/heatmap_CLUSTER3.pdf

graditude heatmap \
    -f GRADitude/without-pellet/gene_list_cluster_3.csv \
    -fc 11 \
    -fe 31 \
    -label "Gene" \
    -o GRADitude/without-pellet/heatmap_CLUSTER4.pdf

--------------------------------------------------

graditude selecting_specific_features \
    -n GRADitude/without-pellet/scaled_100_to_max.csv \
    -fc 11 \
    -fe 31\
    -f "sRNA" "ncRNA" "tRNA" "rRNA" \
    -o GRADitude/without-pellet/sRNAs_filtered.csv




graditude clustering \
    -f GRADitude/without-pellet/sRNAs_filtered_without_pellet.csv \
    -fc 11 \
    -fe 31 \
    -nc 3 \
    -cm 'k-means' \
    -sm no_normalization \
    -o GRADitude/without-pellet/k-means-sRNAs_scaled_max_3_cl_without_pellet.csv


graditude silhouette_analysis \
    -c GRADitude/input/sRNAs_filtered.csv \
    -fc 11 \
    -fe 31 \
    -min 2 \
    -max 10 




graditude t_sne \
            -f GRADitude/without-pellet/k-means_scaled_max_3_cl_without_pellet.csv \
            -fc 11 \
            -fe 31 \
            -pp 25 \
            -list input/20180202_classic_CsrA_sRNAs.txt \
            input/20180202_unique_Hfq_sRNAs_manual_curation.txt \
            input/20180202_unique_ProQ_sRNAs_manual_curation.txt \
            -names CsrA-targets Hfq-targets ProQ-targets \  
            -o1 GRADitude/output/t-SNE_clusters_3cl-25pp-no-pellet.html \
            -o2 GRADitude/output/t-SNE_features_3cl-25pp-no-pellet.html \
            -o3 GRADitude/output/t-SNE_lists_3cl-25pp-no-pellet.html


graditude correlation_all_against_all \
    -f GRADitude/input/scaled_100_to_max.csv \
    -fc 11 \
    -fe 31 \
    -corr Spearman \
    -o GRADitude/output/RNA_correlation_matrix.tsv



graditude plot_network_graph \
    -f GRADitude/GRADitude/RNA_correlation_matrix.csv \
    -index Gene \
    -t 0.98 \
    -max 25 \
    -o GRADitude/output/network_RNA_only.html



graditude heatmap \
    -f GRADitude/input/sRNAs_filtered.csv \
    -fc 11 \
    -fe 32 \
    -label "ncRNA Gene Name" \
    -o GRADitude/output/ncRNA_complexome_heatmap.pdf




graditude clustering_elbow \
    -f output/protein-normalisazion_20260210.1206_pgFilt4_MINIMAL.csv \
    -fc 6 \
    -fe 27 \
    -min 2 \
    -max 12 \
    -o1 GRADitude/output/elbow_variance-protein.pdf \
    -o2 GRADitude/output/elbow_sum_squares-protein.pdf


graditude silhouette_analysis \
    -c output/protein-normalisazion_20260210.1206_pgFilt4_MINIMAL.csv \
    -fc 6 \
    -fe 27 \
    -min 2 \
    -max 12 


graditude clustering_proteins \
    -f output/protein-normalisazion_20260210.1206_pgFilt4_MINIMAL.csv \
    -fc 6 \
    -fe 27 \
    -nc 4 \
    -cm k-means \
    -o GRADitude/output/k-mean-clusters-protein.csv


graditude dimension_reduction_proteins \
    -f GRADitude/output/k-mean-clusters-protein.csv \
    -fc 6 \
    -fe 27 \
    -dm t-SNE \
    -pp 30 \
    -o GRADitude/output/interactive_map.html



graditude correlation_all_against_all \
    -f output/protein-normalisazion_20260210.1206_pgFilt4_MINIMAL.csv \
    -fc 6 \
    -fe 27 \
    -name "Protein.names" \
    -corr Spearman \
    -o GRADitude/output/Protein_correlation_matrix.tsv

graditude extract_cluster_tables \
    -f GRADitude/output/k-mean-clusters-protein.csv \
    -o GRADitude/output/protein_list.csv


graditude correlation_all_against_all \
    -f GRADitude/output/protein_list_cluster_2.csv \
    -fc 6 \
    -fe 27 \
    -name Protein.names \
    -corr Spearman \
    -o GRADitude/output/Protein_correlation_matrix.csv


graditude plot_network_graph \
    -f GRADitude/output/Protein_correlation_matrix.csv \
    -index Protein.names \
    -t 0.98 \
    -max 25 \
    -hl "RNA chaperone ProQ" \
    -o GRADitude/output/network_Protein_Cluster3_t099.html


---------------------------------------------------------------------------

graditude clustering_elbow \
    -f output/protein-normalisazion_20260210.1206_pgFilt4_MINIMAL.csv \
    -fc 6 \
    -fe 27 \
    -min 2 \
    -max 12 \
    -o1 GRADitude/output/elbow_variance-protein.pdf \
    -o2 GRADitude/output/elbow_sum_squares-protein.pdf


graditude clustering_proteins \
    -f output/protein-normalisazion_20260426.1816_pgFilt4_MINIMAL_noPellet.csv \
    -fc 6 \
    -fe 26 \
    -nc 4 \
    -cm k-means \
    -o GRADitude/output/k-mean-clusters-protein-no-pellet.csv


graditude dimension_reduction_proteins \
    -f GRADitude/output/k-mean-clusters-protein-no-pellet.csv \
    -fc 6 \
    -fe 26 \
    -dm t-SNE \
    -pp 30 \
    -o GRADitude/output/interactive_map-no-pellet.html

graditude correlation_all_against_all \
    -f output/protein-normalisazion_20260426.1816_pgFilt4_MINIMAL_noPellet.csv \
    -fc 6 \
    -fe 26 \
    -name Protein.names \
    -corr Spearman \
    -o GRADitude/output/Protein_correlation_matrix.csv


graditude plot_network_graph \
    -f GRADitude/output/Protein_correlation_matrix.csv \
    -index Protein.names \
    -t 0.98 \
    -max 25 \
    -hl "RNA chaperone ProQ" \
    -o GRADitude/output/network_Protein_Cluster3_t098_NO-pellet.html