# About GRADitude 

GRADitude - The GRAD-Seq data analysis tool


Grad-seq is a high-throughput profiling approach for the organism-wide detection
of RNA-RNA and RNA-protein interactions in which molecular complexes are
separated in a gradient by shape and size (Smirnov et al. 2016 PNAS). It offers
new means to study the role of different RNA and protein components in various
macromolecular assemblies by analyzing fractions of a glycerol gradient by a high-
throughput sequencing approaches combined with mass spectrometry. The
Grad-seq approach offers a way to study the distribution of all RNA
involvement in various macromolecular assemblies.

GRADitude is a computational tool for the analysis of Grad-seq
in-gradient profiling.
This open source tool performs all required steps to translate sequencing data of a
Grad-seq experiment into a list of potential molecular complexes.

# Documentation

Documentation can be found on [here](https://silviadg87.github.io/GRADitude/).

# Installation

Installation
There is one way to install GRADitude for the moment. Please check the section below. 
GRADitude can only work when the requirements are installed properly. If you install GRADitude through source code, 
please install the pre-required libraries by yourself.


## Github
All the source code of GRADitude can be retrieve 
from our Git repository. Using the following commands can clone the source code easily.

<code>$ git clone https://github.com/foerstner-lab/GRADitude.git

or

<code>$ git clone git@github.com:foerstner-lab/GRADitude.git</code>

In order to make GRADitude runnable, we have to  create a soft 
link of graditudelib in bin.

<code>$ cd GRADitude/bin</code>

<code>$ ln -s ../graditudelib .</code>



## Arguments

```bash
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
                        usually used to drop the lysate column that is not
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
                        This subcommand can be used to interpret the distance
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
                        This subcommand performs the unsupervised clustering
                        of protein data
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
                        proteincomplexes are actually present in our specific
                        data sets.It finds if all the subunit of that specific
                        complexes are present and calculate the correlation

optional arguments:
  -h, --help            show this help message and exit
  --version, -v         show version

```