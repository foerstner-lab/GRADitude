# Performing an example analysis

In this section you will be able to perform a complete analysis using already 
published GRAD-seq data sets.

In order explore all the potential of a GRADitude here you will be guided through an example analysis 
using the *Escherichia coli* data set downloaded from NCBI  (Höer *et* *al*., 2020, NAR)


# Pre-processing the data, alignment and gene quantification

After downloading the raw data from NCBI, in the original publication, preprocessing steps like read trimming 
and clipping were done with [cutadapt]( https://doi.org/10.14806/ej.17.1.200). 
Read filtering, read mapping, nucleotide‐wise coverage calculation, and genome feature‐wise read
quantification was done using [READemption](https://doi.org/10.1093/bioinformatics/btu533).

To conduce this steps we highly recommend the use of READemption, but anyway any other read mapping are
working too. 

For completeness, we decided to perform the analysis starting from the raw-reads.

## Download singularity image

##### Before starting the analysis you can download the singularity image from Zenodo. In the image you can find all the tools necessary for the analysis

## Create folders

```bash
mkir input output
```

## Dowload the data

```bash
cd READ_LIB_FOLDER &&

    fastq-dump --bzip2 SRR12067299 &
    fastq-dump --bzip2 SRR12067300
    fastq-dump --bzip2 SRR12067301
    fastq-dump --bzip2 SRR12067302
    fastq-dump --bzip2 SRR12067303
    fastq-dump --bzip2 SRR12067304
    fastq-dump --bzip2 SRR12067305
    fastq-dump --bzip2 SRR12067306
    fastq-dump --bzip2 SRR12067307
    fastq-dump --bzip2 SRR12067308
    fastq-dump --bzip2 SRR12067309
    fastq-dump --bzip2 SRR12067310
    fastq-dump --bzip2 SRR12067311
    fastq-dump --bzip2 SRR12067312
    fastq-dump --bzip2 SRR12067313
    fastq-dump --bzip2 SRR12067314
    fastq-dump --bzip2 SRR12067315
    fastq-dump --bzip2 SRR12067316
    fastq-dump --bzip2 SRR12067317
    fastq-dump --bzip2 SRR12067318
    fastq-dump --bzip2 SRR12067319
    fastq-dump --bzip2 SRR12067320

&& cd ..

```



## GRADitude 
Before starting the analysis we recommend These tables are output coming from the 
