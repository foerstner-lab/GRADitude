# Tutorial of GRADitude using Singularity

This tutorial will guide you through a test case to show how to 
perform a GRAD-seq analysis from the pre-processing steps to the
downstream analysis that will be done using GRADitude.
We recommend to execute this analysis in a server or in a virtual machine. The pre-processing 
and mapping steps require a lot of computational time and power.

In this tutorial we will try to show how to use all GRADitude's subcommands
in order to have an overview of all possible complexes.

In order to perform all these steps we need to have many tools and dependencies in 
your pc. To make all simpler and more reproducible we suggest following the example provided below.
All these steps can be then easily adjusted to analyze different 
GRAD-seq experiments.

## Docker containers and singularity

Another way to distribute packages is using Docker. Docker is a service that deliver software
in so called containers. All containers have their own libraries and packages.

A Docker container has inside all dependencies and applications. This increase
the reproducibility of a specific analysis.
In this example all the tools required for the analysis are inside the image that will be generated.

In order to avoid root permission when running Docker, 
Singularity can be used.
For this reason, the example analysis provided, is done using singularity.

You can download singularity in [here](https://sylabs.io/guides/3.0/user-guide/installation.html#)


Once you have singularity in your computer you can run inside your project directory this command:

```bash
singularity build grad-seq-analysis.sif docker://silviadigiorgio/grad-seq-analysis:1.0
```

This will create an image that can be used to perform the analysis.
Before starting the analysis please create the folders input and output in the main directory.

This can be also done via shell using the bash command mkdir.

```bash
mkdir input output
```
We recommend to create subfolders inside the input main folder

```bash
cd input &&
mkdir data_folder raw_reads
```


At the end you will have inside the analysis folder the created image and the two folders

```bash
.
├── grad-seq-analysis.sif
├── input
│   ├── data_folder
│   └── raw_reads
└── output

```

To perform our test case, the raw data have to be retrieved from [NCBI](https://www.ncbi.nlm.nih.gov/Traces/study/?acc=SRP049525&o=acc_s%3Aa).

In order to perform this step the user needs to use the fastq-dump function
provided by the SRA-toolkit that can be downloaded [here](https://anaconda.org/bioconda/sra-tools)

We suggest to download the raw data inside the input folder it has been previously created 

```bash

cd input/raw_reads &&
    fastq-dump --bzip2 SRR12067299
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
    
```
or to automate the process you can run the same command using a for loop

``` bash 
for i in            \
    SRR12067299     \
    SRR12067300     \
    SRR12067301     \
    SRR12067302     \
    SRR12067303     \
    SRR12067304     \
    SRR12067305     \
    SRR12067306     \
    SRR12067307     \
    SRR12067308     \
    SRR12067309     \
    SRR12067310     \
    SRR12067311     \
    SRR12067312     \
    SRR12067313     \
    SRR12067314     \
    SRR12067315     \
    SRR12067316     \
    SRR12067317     \
    SRR12067318     \
    SRR12067319     \
    SRR12067320     \
; do 
    fastq-dump --bzip2 $i; 
  done
```
You can download the reference genome that will be used later on from the NCBI using this command

``` bash 

cd input/data_folder &&
wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2_genomic.fna.gz &&
gzip -d GCF_000005845.2_ASM584v2_genomic.fna.gz

```

You can download the ERCC fasta file that will be necessary for the normalization

``` bash 

cd input/data_folder &&
wget https://assets.thermofisher.com/TFS-Assets/LSG/manuals/ERCC92.zip &&
unzip ERCC92.zip && rm ERCC92.zip && rm ERCC92.gtf

```

The annotation file can be download from Zenodo  (Höer *et* *al*., 2020, NAR)

Once all the raw reads are downloaded. We can start with removing 
the adapter using [cutadapt]( https://doi.org/10.14806/ej.17.1.200).  


``` bash 
ls ${RAW_READ_FOLDER} | parallel -k -j ${CPUS} 
            -q 20 
            -m 1 \
            -a ${ADAPTER} \
            -o ${READEMPTION_FOLDER}/input/reads/'$(basename {} .gz)'.bz2 \
            ${RAW_READ_FOLDER}/{} \
    > ${READ_PROCESSING_STATS_FOLDER}/cutadapt_stats.txt

```