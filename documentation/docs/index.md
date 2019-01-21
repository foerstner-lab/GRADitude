# GRADitude: a computational tool for Grad-seq data analysis

## Introduction

Grad-seq is a high-throughput profiling approach for the organism-wide detection of RNA-RNA and
RNA-protein interactions in which molecular complexes are separated in a gradient by shape and size
(Smirnov et al., 2016, PNAS). Grad-seq separates native cellular lysates including complexes,
according to their molecular weight and shape in a glycerol gradient, independent of charge and
sequence. After this fractionation, RNA-seq and MS-analysis of each of the fractions generated
allows the reconstruction of the sedimentation profiles of all detectable RNAs and protein in a single
experiment. Further analysis can reveal possible interactions between the individual molecules.
So far, Grad-seq has been used to globally study RNA-RNA and RNA-protein interactions in
Salmonella Typhimurium and that allowed us to identify ProQ as a new global RNA-binding protein


```text
usage: graditude [-h] [--version]
                 {create,min_row_sum_ercc,min_row_sum,drop_column,robust_regression,normalize,scaling,correlation_all_against_all,selecting_specific_features,heatmap,plot_kinetics,clustering,clustering_elbow,silhouette_analysis,pca,t_sne,umap,correlation_rnas_protein,correlation_distribution_graph,plot_network_graph,clustering_proteins,dimension_reduction_proteins,correlation_specific_gene,interactive_plots,correlation_replicates,find_complexes}
                 ...

positional arguments:
  {create,min_row_sum_ercc,min_row_sum,drop_column,robust_regression,normalize,scaling,correlation_all_against_all,selecting_specific_features,heatmap,plot_kinetics,clustering,clustering_elbow,silhouette_analysis,pca,t_sne,umap,correlation_rnas_protein,correlation_distribution_graph,plot_network_graph,clustering_proteins,dimension_reduction_proteins,correlation_specific_gene,interactive_plots,correlation_replicates,find_complexes}
                        commands
    min_row_sum_ercc    Filter the ERCC table based on the min row sum. It
                        calculates the sum row_wise and discard the rows with
                        a sum below the threshold specified
    min_row_sum         Filter the gene quantification table based on the min
                        row sum. It calculates the sum row_wise and discard
                        the rows with a sum below the threshold specified
    drop_column         It filters a table dropping a specific column.It is
                        usually used to drop the Lysate column that is not
                        required for the downstream analysis
    robust_regression   It compares the ERCC concentration in mix with the
                        ERCC reads and take it out the outliers
    normalize           This subcommand calculates the ERCC size factor and
                        normalize the gene quantification table based on that
    scaling             This subcommand scales tables using different scaling
                        methods
    correlation_all_against_all
                        This subcommand calculate the correlation coefficients
                        all against all
    selecting_specific_features
                        This subcommand allows to select specific features in
                        a normalized table (ncRNAs, CDS, etc.)
    heatmap             This subcommand is useful to visualize the in-gradient
                        behavior of a larger group of transcripts or proteins
    plot_kinetics       This subcommand plot the kinetics of a specific
                        transcript or protein to better visualize their
                        behavior within the gradient
    clustering          This subcommand performs unsupervised clustering using
                        different algorithm
    clustering_elbow    This subcommands plot the elbow graph in order to
                        choose the ideal number of clusters necessary for the
                        k-means and the hierarchical clustering
    silhouette_analysis
                        This subcommand can be used tointerpret the distance
                        between clusters
    pca                 This subcommand performs the PCA-principal component
                        dimension reduction
    t_sne               This subcommand performs the t-sne dimension reduction
    umap                This subcommand performs the umap dimension reduction
    correlation_rnas_protein
                        This subcommand performs the Spearman or Pearson
                        correlation coefficients of two tables.
    correlation_distribution_graph
                        This subcommand plots the distribution of the
                        correlation coefficients as histogram
    plot_network_graph  This subcommand plots the network plot. It can be used
                        to plot for example sequencing data vs protein data or
                        ncRNAs vs proteins etc.
    clustering_proteins
                        This subcommand performs the unsupervised clustering of
                        protein data
    dimension_reduction_proteins
                        t-sne analysis of Mass spectrometry data
    correlation_specific_gene
                        This subcommand calculate the Spearman or Pearson
                        correlation of a specific gene or protein against all
    interactive_plots   This subcommand is useful to visualize interactive a
                        plot after a dimension reduction algorithm has been
                        applied.
    correlation_replicates
                        This subcommand allows to see the distribution of the
                        correlation coefficient between two biological
                        replicates
    find_complexes      With this subcommand we look at how many of the know
                        protein complexes are actually present in our specific
                        data sets.It finds if all the subunit of that specific
                        complexes are present and calculate the correlation

optional arguments:
  -h, --help            show this help message and exit
  --version, -v         show version

```


## Download

## Source code
The source code of GRADitude can be found at [Github](https://github.com/foerstner-lab/GRADitude)

## License
ISC (Internet Systems Consortium license ~ simplified BSD license)
 - see [LICENSE](license.md)

## Contact
For question and requests feel free to contact 
Silvia Di Giorgio
 
 <digiorgio@zbmed.de>