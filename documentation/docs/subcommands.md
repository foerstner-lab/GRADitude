#GRADitude's subcommands

##Pre-process sequencing data

After the sequencing the resulting reads they have to be mapped against the reference genome. 
The users can use all the mapping tools available. However we recommend the use of READemption tool (Förstner et al., 2014, Bioinformatics). 
This will help you to have all the requested input files without prior elaboration.

After the mapping two tables are relevant to proceed with the usage of GRADitude tool:

1) gene quantification table generated counting the number of overlapped reads for each of the gene
2) read alignment stats table that lists many statistics including the ERCC read counts.

##create

<code>$ create</code> generates the GRADItude folder including the subfolders input and output.
Once created, please move the required files into the input folders.

##filtering_tables
<code>$ filtering_tables</code> 

A subcommand, specific for the sequencing data, that filters the ERCC-reads table 
based on the minimum row sum and the gene quantification table based on the column we would like to drop (specifically the lysate 
column that does not have to be included in the analysis).

```text
usage: graditude filtering_tables [-h] --feature_count_table FEATURE_COUNT_TABLE
                                --ref_feature_count_table REF_FEATURE_COUNT_TABLE
                                  [--min_row_sum MIN_ROW_SUM]
                                  --filtered_feature_count_table FILTERED_FEATURE_COUNT_TABLE
                                  --filtered_ref_feature_count_table FILTERED_REF_FEATURE_COUNT_TABLE
                                  [--dropping_lisate DROPPING_LISATE]
                                  
                                  
optional arguments:
  -h, --help            show this help message and exit
  
basic arguments:

  --feature_count_table FEATURE_COUNT_TABLE, -f FEATURE_COUNT_TABLE
                        gene quantification table
  --ref_feature_count_table REF_FEATURE_COUNT_TABLE, -r REF_FEATURE_COUNT_TABLE
                        ERCC reads table
  --min_row_sum MIN_ROW_SUM, -m MIN_ROW_SUM
                        it calculates the sum of the reads for each gene and
                        discard the rows with less then the sum
  --filtered_feature_count_table FILTERED_FEATURE_COUNT_TABLE, -ff FILTERED_FEATURE_COUNT_TABLE
                        Filtered gene quantification table
  --filtered_ref_feature_count_table FILTERED_REF_FEATURE_COUNT_TABLE, -fr FILTERED_REF_FEATURE_COUNT_TABLE
                        Filtered ERCC reads table
  --dropping_lisate DROPPING_LISATE, -l DROPPING_LISATE
                        name of the lysate column

```
#min_row_sum
<code>$ min_row_sum</code> 

A subcommand, specific for the sequencing data that filters 
the gene quantification table based on the minimum row sum. 

```text
usage: graditude min_row_sum [-h] --feature_count_table FEATURE_COUNT_TABLE
                             --feature_count_start_column
                             FEATURE_COUNT_START_COLUMN --min_row MIN_ROW
                             --output_file OUTPUT_FILE

optional arguments:
  -h, --help            show this help message and exit
 
basic arguments:

  --feature_count_table FEATURE_COUNT_TABLE, -f FEATURE_COUNT_TABLE
                        gene quantification table
  --feature_count_start_column FEATURE_COUNT_START_COLUMN, -fc FEATURE_COUNT_START_COLUMN
                        number of the column with the first fraction
  --min_row MIN_ROW, -m MIN_ROW
                        it calculates the sum of the reads for each gene and
                        discard the rows with less then the sum
  --output_file OUTPUT_FILE, -o OUTPUT_FILE
                        Filtered table

```
#robust_regression
<code>$ robust_regression</code>

This subcommand, specific for the sequencing data, compares the ERCC concentration in mix (it
could be one or two, depending on the experiment) with the ERCC read counts.

One of the reason behind the use of this particular regression is to find outliers that could generate
bad results. It first finds the regression for each of the 21 fractions separately , it plots them, including
inliers and outliers, and then it finds the outliers ERCC in common and discard them. The outputs
generated are 21 plots showing the regression for each of the fractions and a new table containing
only the inliers ERCCs.

```text
usage: graditude robust_regression [-h] --ref_feature_count_table
                                   REF_FEATURE_COUNT_TABLE
                                   --concentration_table CONCENTRATION_TABLE
                                   --number_of_outliers NUMBER_OF_OUTLIERS
                                   [--number_of_ercc_in_common NUMBER_OF_ERCC_IN_COMMON]
                                   --used_mix USED_MIX --output_table
                                   OUTPUT_TABLE
                                   
optional arguments:
  -h, --help            show this help message and exit
  
basic arguments:

  --ref_feature_count_table REF_FEATURE_COUNT_TABLE, -r REF_FEATURE_COUNT_TABLE
                        Filtered ERCC reads table
  --concentration_table CONCENTRATION_TABLE, -c CONCENTRATION_TABLE
                        ERCC concentration table
  --number_of_outliers NUMBER_OF_OUTLIERS, -n NUMBER_OF_OUTLIERS
                        number of outliers
  --number_of_ercc_in_common NUMBER_OF_ERCC_IN_COMMON, -nc NUMBER_OF_ERCC_IN_COMMON
  --used_mix USED_MIX, -mix USED_MIX
                        define the ERCC mix used in the experiment,in case of
                        mix1 and mix2 the --mix is either 3 or 4
  --output_table OUTPUT_TABLE, -o OUTPUT_TABLE
                        output table with ercc in common

```
#normalize
<code>$ normalize</code>

This normalization is specific for the sequencing data.
It normalizes the gene quantification table, that contains all the detectable transcripts using the ERCC
read counts table, filtered or not. This normalization is based on the size factor calculation of DESeq2
(Anders et al., 2010, Bioinformatics).
The purpose of the size factor is to render counts from different samples, which may have been
sequenced to different depths, comparable.
This normalization methods uses the median of the ratios of observed counts and the denominator is
considered as a reference sample obtained by taking the geometric mean across samples.

```text
usage: graditude normalize [-h] --feature_count_table FEATURE_COUNT_TABLE
                           [--feature_count_start_column FEATURE_COUNT_START_COLUMN]
                           [--feature_count_end_column FEATURE_COUNT_END_COLUMN]
                           --ref_feature_count_table REF_FEATURE_COUNT_TABLE
                           [--ref_feature_count_start_column REF_FEATURE_COUNT_START_COLUMN]
                           [--ref_feature_count_end_column REF_FEATURE_COUNT_END_COLUMN]
                           --normalized_table NORMALIZED_TABLE
                           [--size_factor_table SIZE_FACTOR_TABLE]

optional arguments:
  -h, --help            show this help message and exit
  --feature_count_table FEATURE_COUNT_TABLE, -f FEATURE_COUNT_TABLE
                        Filtered gene quantification table
  --feature_count_start_column FEATURE_COUNT_START_COLUMN, -fc FEATURE_COUNT_START_COLUMN
                        number of the column with the first fraction
  --feature_count_end_column FEATURE_COUNT_END_COLUMN, -fe FEATURE_COUNT_END_COLUMN
                        number of the column with the last fraction
  --ref_feature_count_table REF_FEATURE_COUNT_TABLE, -r REF_FEATURE_COUNT_TABLE
                        ERCC table with the ERCC read -counts
  --ref_feature_count_start_column REF_FEATURE_COUNT_START_COLUMN, -rc REF_FEATURE_COUNT_START_COLUMN
                        number of the column with the first fraction
  --ref_feature_count_end_column REF_FEATURE_COUNT_END_COLUMN, -re REF_FEATURE_COUNT_END_COLUMN
                        number of the column with the last fraction
  --normalized_table NORMALIZED_TABLE, -o NORMALIZED_TABLE
                        normalized table
  --size_factor_table SIZE_FACTOR_TABLE, -s SIZE_FACTOR_TABLE
                        size_factor_table

```

#scaling
<code>$ scaling</code>

This subcommand can be used for the protein and the sequencing data. It takes a table, that can be
the normalized or the raw one, as input and scales them using different methods. The default is
normalization to the maximum value but one can modify the behaviour by using parameters such as
normalize to range, log10 or log2.
The scaled table generated by this subcommand can be the input for plotting the in-gradient behavior
of a transcript or a protein.

```text
usage: graditude scaling [-h] --feature_count_table FEATURE_COUNT_TABLE
                         --feature_count_start_column
                         FEATURE_COUNT_START_COLUMN
                         [--pseudo_count PSEUDO_COUNT] --scaling_method
                         {no_normalization,normalized_to_max,normalized_to_range,log10,log2}
                         --scaled_table SCALED_TABLE

optional arguments:
  -h, --help            show this help message and exit
  --feature_count_table FEATURE_COUNT_TABLE, -f FEATURE_COUNT_TABLE
                        normalized gene quantification table
  --feature_count_start_column FEATURE_COUNT_START_COLUMN, -fc FEATURE_COUNT_START_COLUMN
                        number of the column with the first fraction
  --pseudo_count PSEUDO_COUNT, -p PSEUDO_COUNT
                        the pseudocount is a number that will always be added
                        to each value; Adding this number avoid to have
                        mathematical operation with zeros
  --scaling_method {no_normalization,normalized_to_max,normalized_to_range,log10,log2}, -sm {no_normalization,normalized_to_max,normalized_to_range,log10,log2}
                        the scaling methods we would like to apply
  --scaled_table SCALED_TABLE, -o SCALED_TABLE
                        scaled table
                        
 ```