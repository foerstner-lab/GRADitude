#GRADitude's subcommands

##Pre-process sequencing data

After the sequencing the resulting reads they have to be mapped against the reference genome. 
The users can use all the mapping tools available. However we recommend the use of READemption tool (Förstner et al., 2014, Bioinformatics). 
This will help you to have all the requested input files without prior elaboration.

After the mapping two tables are relevant to proceed with the usage of GRADitude tool:

1) gene quantification table generated counting the number of overlapped reads for each of the gene
2) read alignment stats table that lists many statistics including the ERCC read counts.

##create (create analysis folder)

<code>$ create</code> generates the GRADItude folder including the subfolders input and output.
Once created, please move the required files into the input folders.

##filtering_tables
<code>$ filtering_tables</code> 

```text
usage: annogesic filtering_tables [-h] --feature_count_table FEATURE_COUNT_TABLE
                                --ref_feature_count_table REF_FEATURE_COUNT_TABLE
                                  [--min_row_sum MIN_ROW_SUM]
                                  --filtered_feature_count_table FILTERED_FEATURE_COUNT_TABLE
                                  --filtered_ref_feature_count_table FILTERED_REF_FEATURE_COUNT_TABLE
                                  [--dropping_lisate DROPPING_LISATE]
                                  
                                  
optional arguments:
  -h, --help            show this help message and exit
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

