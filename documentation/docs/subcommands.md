# GRADitude's subcommands

## Pre-process sequencing data

After the sequencing the resulting reads they have to be mapped against the reference genome. 
The users can use all the mapping tools available. However we recommend the use of READemption tool (Förstner et al., 2014, Bioinformatics). 
This will help you to have all the requested input files without prior elaboration.

After the mapping two tables are relevant to proceed with the usage of GRADitude tool:

1) gene quantification table generated counting the number of overlapped reads for each of the gene
2) read alignment stats table that lists many statistics including the ERCC read counts.

## create

<code>$ create</code> generates the GRADItude folder including the subfolders input and output.
Once created, please move the required files into the input folders.

## min_row_sum_ercc (filter the table)
<code>$ min_row_sum_ercc</code> 

A subcommand, specific for the sequencing data, that filters the ERCC-reads table 
based on the minimum row sum. It calculates the sum of all the ERCC row-wise and discard the ones that they don't reach 
the specified threshold.

* Basic arguments

```text
usage: graditude min_row_sum_ercc [-h] --ref_feature_count_table
                                  REF_FEATURE_COUNT_TABLE
                                  [--min_row_sum MIN_ROW_SUM]
                                  --filtered_ref_feature_count_table
                                  FILTERED_REF_FEATURE_COUNT_TABLE

optional arguments:
  -h, --help            show this help message and exit
  
basic arguments:
  --ref_feature_count_table REF_FEATURE_COUNT_TABLE, -r REF_FEATURE_COUNT_TABLE
                        ERCC reads table
  --min_row_sum MIN_ROW_SUM, -m MIN_ROW_SUM
                        Specify the threshold we would like to apply
  --filtered_ref_feature_count_table FILTERED_REF_FEATURE_COUNT_TABLE, -fr FILTERED_REF_FEATURE_COUNT_TABLE
                        Filtered ERCC reads table as output

```
## min_row_sum (filter the table)
<code>$ min_row_sum</code> 

A subcommand, specific for the sequencing data that filters 
the gene quantification table based on the minimum row sum.  It calculates the sum of all the ERCC row-wise and discard the ones that they don't reach 
the specified threshold.

* Basic arguments

```text
usage: graditude min_row_sum [-h] --feature_count_table FEATURE_COUNT_TABLE
                             --feature_count_start_column
                             FEATURE_COUNT_START_COLUMN --min_row MIN_ROW
                             --output_file OUTPUT_FILE

basic arguments:
  --feature_count_table FEATURE_COUNT_TABLE, -f FEATURE_COUNT_TABLE
                        Gene quantification table
  --feature_count_start_column FEATURE_COUNT_START_COLUMN, -fc FEATURE_COUNT_START_COLUMN
                        Specify the number of the column with the first
                        fraction
  --feature_count_end_column FEATURE_COUNT_END_COLUMN, -fe FEATURE_COUNT_END_COLUMN
                        Specify the number of the last fraction we would like
                        to consider in the analysis
  --min_row MIN_ROW, -m MIN_ROW
                        Specify the threshold we would like to apply
  --output_file OUTPUT_FILE, -o OUTPUT_FILE
                        Filtered table as output

```


## drop_column (filter the table)
<code>$ drop_column</code>

This subcommand is specific for the sequencing data and it can be use to drop a specific column we would not
like to don't consider in the downstream analysis. For example it can be used to drop the Lysate column.

```text

usage: graditude drop_column [-h] --feature_count_table FEATURE_COUNT_TABLE
                             --column_to_drop COLUMN_TO_DROP --output_file
                             OUTPUT_FILE

basic arguments:
  --feature_count_table FEATURE_COUNT_TABLE, -f FEATURE_COUNT_TABLE
                        Gene quantification table or ERCC-reads table
  --column_to_drop COLUMN_TO_DROP, -c COLUMN_TO_DROP
                        This parameter specify the name of the column you
                        would like to drop
  --output_file OUTPUT_FILE, -o OUTPUT_FILE
                        Filtered table as output


```

## selecting_specific_features (filter the table)
<code>$ selecting_specific_features</code>

This subcommand extract from a table specific feature, such as sRNAs or mRNAs. 

```text
usage: graditude selecting_specific_features [-h] --normalized_table
                                             NORMALIZED_TABLE
                                             --feature_count_start_column
                                             FEATURE_COUNT_START_COLUMN
                                             --feature_count_end_column
                                             FEATURE_COUNT_END_COLUMN
                                             --features FEATURES
                                             [FEATURES ...] --output_file
                                             OUTPUT_FILE

optional arguments:
  -h, --help            show this help message and exit
  --normalized_table NORMALIZED_TABLE, -n NORMALIZED_TABLE
                        Normalized table
  --feature_count_start_column FEATURE_COUNT_START_COLUMN, -fc FEATURE_COUNT_START_COLUMN
                        Specify the number of the column with the first
                        fraction
  --feature_count_end_column FEATURE_COUNT_END_COLUMN, -fe FEATURE_COUNT_END_COLUMN
                        Specify the number of the last fraction we would like
                        to consider in the analysis
  --features FEATURES [FEATURES ...], -f FEATURES [FEATURES ...]
                        This parameter specify the features we would like to
                        filter of. It can be a single one or a list
  --output_file OUTPUT_FILE, -o OUTPUT_FILE
                        Filtered table
                        
```



## robust_regression
<code>$ robust_regression</code>

This subcommand, specific for the sequencing data, compares the ERCC concentration in mix (it
could be one or two, depending on the experiment) with the ERCC read counts.

One of the reason behind the use of this particular regression is to find outliers that could generate
bad results. It first finds the regression for each of the 21 fractions separately , it plots them, including
inliers and outliers, and then it finds the outliers ERCC in common and discard them. The outputs
generated are 21 plots showing the regression for each of the fractions and a new table containing
only the inliers ERCCs.

* Basic arguments

```text
usage: graditude robust_regression [-h] --ref_feature_count_table
                                   REF_FEATURE_COUNT_TABLE
                                   --concentration_table CONCENTRATION_TABLE
                                   --number_of_outliers NUMBER_OF_OUTLIERS
                                   [--number_of_ercc_in_common NUMBER_OF_ERCC_IN_COMMON]
                                   --used_mix USED_MIX --output_table
                                   OUTPUT_TABLE
                                   
basic arguments:
  --ref_feature_count_table REF_FEATURE_COUNT_TABLE, -r REF_FEATURE_COUNT_TABLE
                        Filtered ERCC reads table
  --concentration_table CONCENTRATION_TABLE, -c CONCENTRATION_TABLE
                        ERCC concentration table
  --number_of_outliers NUMBER_OF_OUTLIERS, -n NUMBER_OF_OUTLIERS
                        Number of outliers
  --number_of_ercc_in_common NUMBER_OF_ERCC_IN_COMMON, -nc NUMBER_OF_ERCC_IN_COMMON
                        Number of ERCC considered outliers in common within
                        the different fractions
  --used_mix USED_MIX, -mix USED_MIX
                        This parameter as to be used to define which ERCC mix
                        have been used in the experiment, in case of mix1 and
                        mix2 the --mix is either 3 or 4
  --output_table OUTPUT_TABLE, -o OUTPUT_TABLE
                        Output table with the inliers ERCC

```
## normalize
<code>$ normalize</code>

This normalization is specific for the sequencing data.
It normalizes the gene quantification table, that contains all the detectable transcripts using the ERCC
read counts table, filtered or not. This normalization is based on the size factor calculation of DESeq2
(Anders et al., 2010, Bioinformatics).
The purpose of the size factor is to render counts from different samples, which may have been
sequenced to different depths, comparable.
This normalization methods uses the median of the ratios of observed counts and the denominator is
considered as a reference sample obtained by taking the geometric mean across samples.


* Basic arguments

```text
usage: graditude normalize [-h] --feature_count_table FEATURE_COUNT_TABLE
                           [--feature_count_start_column FEATURE_COUNT_START_COLUMN]
                           [--feature_count_end_column FEATURE_COUNT_END_COLUMN]
                           --ref_feature_count_table REF_FEATURE_COUNT_TABLE
                           [--ref_feature_count_start_column REF_FEATURE_COUNT_START_COLUMN]
                           [--ref_feature_count_end_column REF_FEATURE_COUNT_END_COLUMN]
                           --normalized_table NORMALIZED_TABLE
                           [--size_factor_table SIZE_FACTOR_TABLE]

basic arguments:
  --feature_count_table FEATURE_COUNT_TABLE, -f FEATURE_COUNT_TABLE
                        Filtered gene quantification table
  --feature_count_start_column FEATURE_COUNT_START_COLUMN, -fc FEATURE_COUNT_START_COLUMN
                        Specify the number of the column with the first
                        fraction
  --feature_count_end_column FEATURE_COUNT_END_COLUMN, -fe FEATURE_COUNT_END_COLUMN
                        Specify the number of the last fraction we would like
                        to consider in the analysis
  --ref_feature_count_table REF_FEATURE_COUNT_TABLE, -r REF_FEATURE_COUNT_TABLE
                        ERCC table with the ERCC read-counts
  --ref_feature_count_start_column REF_FEATURE_COUNT_START_COLUMN, -rc REF_FEATURE_COUNT_START_COLUMN
                        Specify the number of the column with the first
                        fraction for the ERCC table
  --ref_feature_count_end_column REF_FEATURE_COUNT_END_COLUMN, -re REF_FEATURE_COUNT_END_COLUMN
                        Specify the number of the last fraction we would like
                        to consider in the analysis for the ERCC table
  --normalized_table NORMALIZED_TABLE, -o NORMALIZED_TABLE
                        Table normalized
  --size_factor_table SIZE_FACTOR_TABLE, -s SIZE_FACTOR_TABLE
                        Table with all the size factor

```

## scaling (scale the data)
<code>$ scaling</code>

This subcommand can be used for the protein and the sequencing data. It takes a table, that can be
the normalized or the raw one, as input and scales them using different methods. The default is
normalization to the maximum value but one can modify the behaviour by using parameters such as
normalize to range, log10 or log2.
The scaled table generated by this subcommand can be the input for plotting the in-gradient behavior
of a transcript or a protein.

* Basic arguments

```text
usage: graditude scaling [-h] --feature_count_table FEATURE_COUNT_TABLE
                         --feature_count_start_column
                         FEATURE_COUNT_START_COLUMN
                         [--pseudo_count PSEUDO_COUNT] --scaling_method
                         {no_normalization,normalized_to_max,normalized_to_range,log10,log2}
                         --scaled_table SCALED_TABLE

basic arguments:
  --feature_count_table FEATURE_COUNT_TABLE, -f FEATURE_COUNT_TABLE
                        Normalized gene quantification table or raw tables
  --feature_count_start_column FEATURE_COUNT_START_COLUMN, -fc FEATURE_COUNT_START_COLUMN
                        Specify the number of the column with the first
                        fraction
  --feature_count_end_column FEATURE_COUNT_END_COLUMN, -fe FEATURE_COUNT_END_COLUMN
                        Specify the number of the last fraction we would like
                        to consider in the analysis
  --pseudo_count PSEUDO_COUNT, -p PSEUDO_COUNT
                        the pseudocount is a number that will always be added
                        to each value; Adding this number avoid to have
                        mathematical operation with zeros
  --scaling_method {no_normalization,normalized_to_max,normalized_to_range,log10,log2}, -sm {no_normalization,normalized_to_max,normalized_to_range,log10,log2}
                        Define the scaling methods you would like to apply.
                        The user can choose between a normalization to the
                        maximum value, to a range, a log10 and log 2
                        normalization. Alternatively the user can decide to
                        not use any kind of normalization
  --scaled_table SCALED_TABLE, -o SCALED_TABLE
                        Scaled table as output

```
## clustering_elbow (find number of clusters)
<code>$ clustering_elbow</code>

This subcommand implements a method designed to find the appropriate number 
of clusters in a data set. For several clustering algorithms, 
such as k-means or hierarchical clustering, the user has to
specifies the number of expected clusters as a parameter.
In the elbow method the user gives a range of clusters, 
usually from 0 to 10, and plots the reduction in
variance. The resulting curve contains an elbow that 
indicates the optimal number of clusters.


* Basic arguments

```text
usage: graditude clustering_elbow [-h] --feature_count_table
                                  FEATURE_COUNT_TABLE
                                  --feature_count_start_column
                                  FEATURE_COUNT_START_COLUMN
                                  --feature_count_end_column
                                  FEATURE_COUNT_END_COLUMN
                                  --min_number_of_clusters
                                  MIN_NUMBER_OF_CLUSTERS
                                  --max_number_of_clusters
                                  MAX_NUMBER_OF_CLUSTERS --output_plots1
                                  OUTPUT_PLOTS1 --output_plots2 OUTPUT_PLOTS2

basic arguments:
  --feature_count_table FEATURE_COUNT_TABLE, -f FEATURE_COUNT_TABLE
                        Filtered gene quantification table
  --feature_count_start_column FEATURE_COUNT_START_COLUMN, -fc FEATURE_COUNT_START_COLUMN
                        This parameter specified the number of the column with
                        the first fraction
  --feature_count_end_column FEATURE_COUNT_END_COLUMN, -fe FEATURE_COUNT_END_COLUMN
                        Specify the number of the last fraction we would like
                        to consider in the analysis
  --min_number_of_clusters MIN_NUMBER_OF_CLUSTERS, -min MIN_NUMBER_OF_CLUSTERS
                        Minimum number of clusters that you want to represent
                        in the plot
  --max_number_of_clusters MAX_NUMBER_OF_CLUSTERS, -max MAX_NUMBER_OF_CLUSTERS
                        Maximum number of clusters that you want to represent
                        in the plot
  --output_plots1 OUTPUT_PLOTS1, -o1 OUTPUT_PLOTS1
                        Plot showing the average within cluster sum of squares
                        against the number of clusters
  --output_plots2 OUTPUT_PLOTS2, -o2 OUTPUT_PLOTS2
                        Plot showing the percentage of variance explained
                        versus the number of clusters
```

## clustering (cluster the data)
<code>$ clustering</code>

The subcommands can be used for the sequencing data. It takes the
normalized gene quantification table or the raw one as input and return a table with a new column
that declares the number of clusters as output. It needs the number of cluster and the algorithm to
apply as parameter. So far the k-means, the hierarchical and the DBSCAN clustering algorithms have
been included.

* Basic arguments

```text
usage: graditude clustering [-h] --feature_count_table FEATURE_COUNT_TABLE
                            --feature_count_start_column
                            FEATURE_COUNT_START_COLUMN --number_of_clusters
                            NUMBER_OF_CLUSTERS [--pseudo_count PSEUDO_COUNT]
                            --clustering_methods
                            {k-means,DBSCAN,hierarchical_clustering}
                            [--epsilon EPSILON] [--min_samples MIN_SAMPLES]
                            --scaling_method
                            {no_normalization,normalized_to_max,normalized_to_range,log10,log2}
                            --output_file OUTPUT_FILE

basic arguments:
  --feature_count_table FEATURE_COUNT_TABLE, -f FEATURE_COUNT_TABLE
                        This parameter specified the table we would like to
                        use. It can be the normalized or the raw table
  --feature_count_start_column FEATURE_COUNT_START_COLUMN, -fc FEATURE_COUNT_START_COLUMN
                        This parameter specified the number of the column with
                        the first fraction
  --pseudo_count PSEUDO_COUNT, -p PSEUDO_COUNT
                        The pseudocount represent a number that will always be
                        added to each value; Adding this number avoid to have
                        mathematical operation with zero
  --clustering_methods {k-means,DBSCAN,hierarchical_clustering}, 
   -cm {k-means,DBSCAN,hierarchical_clustering}
                        The user can choose between 3 clustering algorithm,
                        k-means clustering, hierarchical clustering and DB-
                        SCAN clustering
  --scaling_method {no_normalization,normalized_to_max,normalized_to_range,log10,log2}, 
                   -sm {no_normalization,normalized_to_max,normalized_to_range,log10,log2}
                        Define the scaling methods you would like to apply.
                        The user can choose between a normalization to the
                        maximum value, to a range, a log10 and log 2
                        normalization. Alternatively the user can decide to
                        not use any kind of normalization
  --output_file OUTPUT_FILE, -o OUTPUT_FILE
                        Output table with a new column containing the number
                        of clusters
```


* Additional arguments

```text
additional arguments:
  --epsilon EPSILON, -e EPSILON
                        This parameter is specific for the DBSCAN clustering
                        algorithm. It defines how close points should be in
                        order to be considered part of a cluster. only for
                        DBSCAN clustering
  --min_samples MIN_SAMPLES, -ms MIN_SAMPLES
                        This parameter is specific for the DBSCAN clustering
                        algorithm and represent the minimum number of points
                        necessary to form a dense region
  --number_of_clusters NUMBER_OF_CLUSTERS, -nc NUMBER_OF_CLUSTERS
                        This parameter specify the number of clusters, k                        
```
 
## t-sne (dimension reduction)
<code>$ t_sne</code>

To identify biochemically similar transcripts the t-SNE dimension
 reduction algorithm has been implemented.
The t-SNE also known as t-distributed stochastic neighbor embedding, 
help us to visualize the data. In order to visualize interactlivi the 
data-sets we used the python library 
Bokeh and the JavaScript Callbacks one to navigate t the data-set.

* Basic arguments

```text
usage: graditude t_sne [-h] --feature_count_table FEATURE_COUNT_TABLE
                       --feature_count_start_column FEATURE_COUNT_START_COLUMN
                       --perplexity PERPLEXITY
                       [--srna_list SRNA_LIST [SRNA_LIST ...]]
                       [--cluster_names CLUSTER_NAMES [CLUSTER_NAMES ...]]
                       [--color_set COLOR_SET] [--url_link URL_LINK]
                       [--output_file1 OUTPUT_FILE1]
                       [--output_file2 OUTPUT_FILE2]
                       [--output_file3 OUTPUT_FILE3]

basic arguments:
  --feature_count_table FEATURE_COUNT_TABLE, -f FEATURE_COUNT_TABLE
                        This parameter specified the table we would like to
                        use. It can be the normalized or the raw table
  --feature_count_start_column FEATURE_COUNT_START_COLUMN, -fc FEATURE_COUNT_START_COLUMN
                        This parameter specified the number of the column with
                        the first fraction
  --feature_count_end_column FEATURE_COUNT_END_COLUMN, -fe FEATURE_COUNT_END_COLUMN
                        Specify the number of the last fraction we would like
                        to consider in the analysis
  --perplexity PERPLEXITY, -pp PERPLEXITY
                        The perplexity is useful tobalance the attention
                        between the global and the local aspects of data. It
                        is better to select a value between 5 and 50
  --output_file1 OUTPUT_FILE1, -o1 OUTPUT_FILE1
                        Output plot colorized using clusters information
  --output_file2 OUTPUT_FILE2, -o2 OUTPUT_FILE2
                        Output plot colorized using attributes information
  --output_file3 OUTPUT_FILE3, -o3 OUTPUT_FILE3
                        Output plot colorized using a specific list
```


* Additional arguments

```text
additional arguments:
  --srna_list SRNA_LIST [SRNA_LIST ...], -list SRNA_LIST [SRNA_LIST ...]
                        This parameter allow the user to specify a list of
                        features or genes we would like to highlight in the
                        plot
  --cluster_names CLUSTER_NAMES [CLUSTER_NAMES ...], -names CLUSTER_NAMES [CLUSTER_NAMES ...]
                        This parameter is required only if you provide a
                        specific list. It allows the user to specify the label
                        on the third plot
  --color_set COLOR_SET, -set_colors COLOR_SET
                        This parameter can be changed if you are looking for a
                        specific color combination for your output plot
  --url_link URL_LINK, -url URL_LINK
                        This parameter allowed to choose the website you would
                        like to open when clicking on a specific point in the
                        html plot
                        
```
## pca (dimension reduction)
<code>$ pca</code>

To identify biochemically similar transcripts the PCA dimension
reduction algorithm has been implemented.
The PCA also known as principal component analysis, 
help us to visualize the data. In order to visualize interactively the 
data sets we used the python library 
Bokeh and the JavaScript Callbacks one to navigate the data-set.

* Basic arguments

```text
usage: graditude pca [-h] --feature_count_table FEATURE_COUNT_TABLE
                     --feature_count_start_column FEATURE_COUNT_START_COLUMN
                     --feature_count_end_column FEATURE_COUNT_END_COLUMN
                     [--srna_list_files SRNA_LIST_FILES [SRNA_LIST_FILES ...]]
                     [--cluster_names CLUSTER_NAMES [CLUSTER_NAMES ...]]
                     [--color_set COLOR_SET] [--url_link URL_LINK]
                     --output_file_colorized_by_clusters
                     OUTPUT_FILE_COLORIZED_BY_CLUSTERS
                     --output_file_colorized_by_rna_class
                     OUTPUT_FILE_COLORIZED_BY_RNA_CLASS
                     --output_file_colorized_by_lists
                     OUTPUT_FILE_COLORIZED_BY_LISTS

basic arguments:
  --feature_count_table FEATURE_COUNT_TABLE, -f FEATURE_COUNT_TABLE
                        This parameter specified the table we would like to
                        use. It can be the normalized or the raw table
  --feature_count_start_column FEATURE_COUNT_START_COLUMN, -fc FEATURE_COUNT_START_COLUMN
                        This parameter specified the number of the column with
                        the first fraction
  --feature_count_end_column FEATURE_COUNT_END_COLUMN, -fe FEATURE_COUNT_END_COLUMN
                        Specify the number of the last fraction we would like
                        to consider in the analysis

  --output_file_colorized_by_clusters OUTPUT_FILE_COLORIZED_BY_CLUSTERS, -o1 OUTPUT_FILE_COLORIZED_BY_CLUSTERS
                        Output plot colorized using clusters information
  --output_file_colorized_by_rna_class OUTPUT_FILE_COLORIZED_BY_RNA_CLASS, -o2 OUTPUT_FILE_COLORIZED_BY_RNA_CLASS
                        Output plot colorized using attributes information
  --output_file_colorized_by_lists OUTPUT_FILE_COLORIZED_BY_LISTS, -o3 OUTPUT_FILE_COLORIZED_BY_LISTS
                        Output plot colorized using a specific list
```

* Additional arguments

```text
additional arguments:
  --srna_list_files SRNA_LIST_FILES [SRNA_LIST_FILES ...], -list SRNA_LIST_FILES [SRNA_LIST_FILES ...]
                        This parameter allow the user to specify a list of
                        features or genes we would like to highlight in the
                        plot
  --cluster_names CLUSTER_NAMES [CLUSTER_NAMES ...], -names CLUSTER_NAMES [CLUSTER_NAMES ...]
                        This parameter is required only if you provide a
                        specific list. It allows the user to specify the label
                        on the third plot
  --color_set COLOR_SET, -set_colors COLOR_SET
                        This parameter can be changed if you are looking for a
                        specific color combination for your output plot
  --url_link URL_LINK, -url URL_LINK
                        This parameter allowed to choose the website you would
                        like to open when clicking on a specific point in the
                        html plot
```

## plot_kinetics (plot the in-gradient behavior)
<code>$ plot_kinetics</code>

This subcommand is useful to better visualize the behavior of a specific transcript or protein within the gradient. 
One foundation of the Grad-seq analysis is that the kinetic of molecule in the fractionations allows the reconstruction of 
the sedimentation profiles of all detectable RNA and proteins.

* Basic arguments

```text
usage: graditude plot_kinetics [-h] --feature_count_table FEATURE_COUNT_TABLE
                               --feature_count_start_column
                               FEATURE_COUNT_START_COLUMN
                               --feature_count_end_column
                               FEATURE_COUNT_END_COLUMN --gene_name GENE_NAME
                               [--output_format {html,pdf}]

basic arguments:
  --feature_count_table FEATURE_COUNT_TABLE, -f FEATURE_COUNT_TABLE
                        This parameter specified the table we would like to
                        use. It can be the normalized or the raw table
  --feature_count_start_column FEATURE_COUNT_START_COLUMN, -fc FEATURE_COUNT_START_COLUMN
                        Specify the number of the column with the first
                        fraction
  --feature_count_end_column FEATURE_COUNT_END_COLUMN, -fe FEATURE_COUNT_END_COLUMN
                        Specify the number of the last fraction we would like
                        to consider in the analysis
  --gene_name GENE_NAME, -gene GENE_NAME
                        With this parameter you can specify the name of the
                        gene or the proteinyou would like to explore
  --output_format {html,pdf}, -format {html,pdf}
                        You can use this parameter tospecify in which format
                        you would like tosave your plot
                        
```

## heatmap (plot the heatmap)
<code>$ heatmap</code>

This subcommand is useful to better visualize the in-gradient behavior of a
 larger group of transcripts or proteins.

* Basic arguments

```text
usage: graditude heatmap [-h] --feature_count_table FEATURE_COUNT_TABLE
                         [--feature_count_start_column FEATURE_COUNT_START_COLUMN]
                         [--feature_count_end_column FEATURE_COUNT_END_COLUMN]
                         --y_label Y_LABEL --output_file OUTPUT_FILE

basic arguments:
  --feature_count_table FEATURE_COUNT_TABLE, -f FEATURE_COUNT_TABLE
                        Gene quantification table or protein table
  --feature_count_start_column FEATURE_COUNT_START_COLUMN, -fc FEATURE_COUNT_START_COLUMN
                        Specify the number of the column with the first
                        fraction
  --feature_count_end_column FEATURE_COUNT_END_COLUMN, -fe FEATURE_COUNT_END_COLUMN
                        Specify the number of the last fraction we would like
                        to consider in the analysis
  --y_label Y_LABEL, -label Y_LABEL
                        This parameter allow you to specify the label you
                        would like to visualize on the y-axis
  --output_file OUTPUT_FILE, -o OUTPUT_FILE
                        Plot as output
```

## silhouette_analysis (clustering)
<code>$ silhouette_analysis</code>

This subcommand can be used to interpret the distance between clusters. It is useful to see if the number of clusters (k)
you have chosen is correct for the data set.

* Basic arguments

```text
usage: graditude silhouette_analysis [-h] --feature_count_table
                                     FEATURE_COUNT_TABLE
                                     --feature_count_start_column
                                     FEATURE_COUNT_START_COLUMN
                                     --feature_count_end_column
                                     FEATURE_COUNT_END_COLUMN
                                     --min_number_of_clusters
                                     MIN_NUMBER_OF_CLUSTERS
                                     --max_number_of_clusters
                                     MAX_NUMBER_OF_CLUSTERS

basic arguments:
  --feature_count_table FEATURE_COUNT_TABLE, -c FEATURE_COUNT_TABLE
                        Gene quantification table or Protein table
  --feature_count_start_column FEATURE_COUNT_START_COLUMN, -fc FEATURE_COUNT_START_COLUMN
                        This parameter specify the number of the column with
                        the first fraction
  --feature_count_end_column FEATURE_COUNT_END_COLUMN, -fe FEATURE_COUNT_END_COLUMN
                        Specify the number of the last fraction we would like
                        to consider in the analysis
  --min_number_of_clusters MIN_NUMBER_OF_CLUSTERS, -min MIN_NUMBER_OF_CLUSTERS
                        Minimum number of clusters that you want to represent
                        in the plot
  --max_number_of_clusters MAX_NUMBER_OF_CLUSTERS, -max MAX_NUMBER_OF_CLUSTERS
                        Maximum number of clusters that you want to represent
                        in the plot
```
## correlation_specific_gene (correlation coefficient)
<code>$ correlation_specific_gene</code>

This subcommand is useful if you have a gene or a protein of interest and you would like to predict new interactions.
The assumption is that proteins or genes with an high correlation coefficients might interact.

* Basic arguments

```text
usage: graditude correlation_specific_gene [-h] --feature_count_table
                                           FEATURE_COUNT_TABLE
                                           --feature_count_start_column
                                           FEATURE_COUNT_START_COLUMN
                                           [--feature_count_end_column FEATURE_COUNT_END_COLUMN]
                                           --name_column_with_genes_name
                                           NAME_COLUMN_WITH_GENES_NAME --name
                                           NAME --correlation
                                           {Pearson,Spearman}
                                           [--output_file OUTPUT_FILE]

basic arguments:
  --feature_count_table FEATURE_COUNT_TABLE, -f FEATURE_COUNT_TABLE
                        Gene quantification table or Protein table
  --feature_count_start_column FEATURE_COUNT_START_COLUMN, -fc FEATURE_COUNT_START_COLUMN
                        This parameter specify the number of the column with
                        the first fraction
  --feature_count_end_column FEATURE_COUNT_END_COLUMN, -fe FEATURE_COUNT_END_COLUMN
                        Specify the number of the last fraction we would like
                        to consider in the analysis
  --name_column_with_genes_name NAME_COLUMN_WITH_GENES_NAME, -nc NAME_COLUMN_WITH_GENES_NAME
                        This parameter allows the user to specify the name of
                        the column where we want to search the gene or the
                        proteins
  --name NAME, -name NAME
                        Name of the gene or protein of your interest
  --correlation {Pearson,Spearman}, -corr {Pearson,Spearman}
                        Choose if applying the Pearson or Spearman correlation
  --output_file OUTPUT_FILE, -o OUTPUT_FILE
                        Table with correlation coefficients and p-values

```

## correlation_distribution_graph (histogram of correlation coefficients distribution)
<code>$ correlation_distribution_graph</code>

This subcommand creates a histogram to identify the distribution of the
correlation coefficients, to better visualize the generated data and to create a comprehensible plot.
The plot shows the percentile that might be used as cut-off in the network plot or in further analysis.

* Basic arguments

```text
usage: graditude correlation_distribution_graph [-h]
                                                --table_with_correlation_coefficient
                                                TABLE_WITH_CORRELATION_COEFFICIENT
                                                --percentile PERCENTILE
                                                --output_plot OUTPUT_PLOT

basic arguments:
  --table_with_correlation_coefficient TABLE_WITH_CORRELATION_COEFFICIENT, -c TABLE_WITH_CORRELATION_COEFFICIENT
                        Table with a column containing the correlation
                        coefficients
  --percentile PERCENTILE, -p PERCENTILE
                        Define the percentile value
  --output_plot OUTPUT_PLOT, -o OUTPUT_PLOT
                        Histogram with the correlation coefficients
                        distribution

```

## correlation_rnas_protein (correlation coefficient)
<code>$ correlation_rnas_protein</code>

This subcommand find the correlation coefficient of two different tables. It can be used for example for combining 
RNA-sequencing and Mass-spectrometry data set. In this way we can predict RNA-protein interactions.
In the implemented approach an all-against-Spearman or Pearson correlation of the protein and the gene
quantification tables are generated.

* Basic arguments

```text
usage: graditude correlation_rnas_protein [-h] --feature_count_table
                                          FEATURE_COUNT_TABLE
                                          --feature_count_start_column
                                          FEATURE_COUNT_START_COLUMN
                                          [--feature_count_end_column FEATURE_COUNT_END_COLUMN]
                                          --protein_table PROTEIN_TABLE
                                          --protein_count_start_column
                                          PROTEIN_COUNT_START_COLUMN
                                          [--protein_count_end_column PROTEIN_COUNT_END_COLUMN]
                                          [--correlation_type {Pearson,Spearman}]
                                          [--output_file OUTPUT_FILE]

basic arguments:
  --feature_count_table FEATURE_COUNT_TABLE, -f FEATURE_COUNT_TABLE
                        This parameter specify the number of the column with
                        the first fraction in the first table
  --feature_count_start_column FEATURE_COUNT_START_COLUMN, -fc FEATURE_COUNT_START_COLUMN
                        First table, for examplethe sequencing table
  --feature_count_end_column FEATURE_COUNT_END_COLUMN, -fe FEATURE_COUNT_END_COLUMN
                        Specify the number of the last fraction we would like
                        to consider in the analysis in the first table
  --protein_table PROTEIN_TABLE, -p PROTEIN_TABLE
                        Second table, for examplethe protein table
  --protein_count_start_column PROTEIN_COUNT_START_COLUMN, -pc PROTEIN_COUNT_START_COLUMN
                        This parameter specify the number of the column with
                        the first fraction in the second table
  --protein_count_end_column PROTEIN_COUNT_END_COLUMN, -pe PROTEIN_COUNT_END_COLUMN
                        Specify the number of the last fraction we would like
                        to consider in the analysis in the first table
  --correlation_type {Pearson,Spearman}, -corr {Pearson,Spearman}
                        Choose if applying the Pearson or Spearman correlation
  --output_file OUTPUT_FILE, -o OUTPUT_FILE
                        Output table containing the correlation coefficients

```

## plot_network_graph (network plot)
<code>$ plot_network_graph</code>
 
This subcommand plots the network plot. 
The subcommand identifies two kind of nodes: transcripts and proteins. The edges are the correlation coefficients. The graph has
been drawn using a force-directed layout, computed using the Fruchterman-Reingold algorithm.


* Basic arguments

```text
usage: graditude plot_network_graph [-h] --feature_count_table
                                    FEATURE_COUNT_TABLE --threshold THRESHOLD
                                    --max_size MAX_SIZE
                                    [--output_plot OUTPUT_PLOT]

optional arguments:
  --feature_count_table FEATURE_COUNT_TABLE, -f FEATURE_COUNT_TABLE
                        Table with correlation coefficients values
  --threshold THRESHOLD, -t THRESHOLD
                        Cut-off necessary to plot the genes or proteins with
                        an high correlation coefficients
  --max_size MAX_SIZE, -max MAX_SIZE
                        This parameter is useful to set the maximum area of
                        each point. All the points are then scaled based on
                        that
  --output_plot OUTPUT_PLOT, -o OUTPUT_PLOT
                        Network plot

```
