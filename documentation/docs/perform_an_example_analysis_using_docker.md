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
singularity build grad-seq-analysis.sif docker://silviadigiorgio/grad-seq-analysis-ecoli
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

If you are not familiar with Bioinformatics please be aware that some commands we will execute 
they will take some time. So we recommend to run everything in a server and with [tmux](https://github.com/tmux/tmux/wiki)

To perform our test case, the raw data have to be retrieved from [NCBI](https://www.ncbi.nlm.nih.gov/sra?term=SRP268299).

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

After downloading the data I recommend to change the name of the files according the specific 
fraction like suggested here:

``` bash 
cd input/raw_reads &&
mv SRR12067299.fastq.bz2 Grad-00L.fastq.bz2 &&
mv SRR12067300.fastq.bz2 Grad-01.fastq.bz2 &&
mv SRR12067301.fastq.bz2 Grad-02.fastq.bz2 &&  
mv SRR12067302.fastq.bz2 Grad-03.fastq.bz2 &&   
mv SRR12067303.fastq.bz2 Grad-04.fastq.bz2 &&   
mv SRR12067304.fastq.bz2 Grad-05.fastq.bz2 &&   
mv SRR12067305.fastq.bz2 Grad-06.fastq.bz2 &&   
mv SRR12067306.fastq.bz2 Grad-07.fastq.bz2 &&    
mv SRR12067307.fastq.bz2 Grad-08.fastq.bz2 &&   
mv SRR12067308.fastq.bz2 Grad-09.fastq.bz2 &&   
mv SRR12067309.fastq.bz2 Grad-10.fastq.bz2 &&   
mv SRR12067310.fastq.bz2 Grad-11.fastq.bz2 &&   
mv SRR12067311.fastq.bz2 Grad-12.fastq.bz2 &&    
mv SRR12067312.fastq.bz2 Grad-13.fastq.bz2 &&    
mv SRR12067313.fastq.bz2 Grad-14.fastq.bz2 &&   
mv SRR12067314.fastq.bz2 Grad-15.fastq.bz2 &&    
mv SRR12067315.fastq.bz2 Grad-16.fastq.bz2 &&   
mv SRR12067316.fastq.bz2 Grad-17.fastq.bz2 &&   
mv SRR12067317.fastq.bz2 Grad-18.fastq.bz2 &&    
mv SRR12067318.fastq.bz2 Grad-19.fastq.bz2 &&    
mv SRR12067319.fastq.bz2 Grad-20.fastq.bz2 &&   
mv SRR12067320.fastq.bz2 Grad-21P.fastq.bz2    
```


You can download the reference genome that will be used later on from the NCBI using this command

``` bash 

cd input/data_folder &&
wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2_genomic.fna.gz &&
gzip -d GCF_000005845.2_ASM584v2_genomic.fna.gz && cd ../..

```

You can download the ERCC fasta file that will be necessary for the normalization

``` bash 

cd input/data_folder &&
wget https://assets.thermofisher.com/TFS-Assets/LSG/manuals/ERCC92.zip &&
unzip ERCC92.zip && rm ERCC92.zip && rm ERCC92.gtf && cd ../..

```

The annotation file can be download from [tutorial_data folder](https://github.com/foerstner-lab/GRADitude/blob/main/tutorial_data/NC_000913.3_no_duplicates.gff) in github  (Höer *et* *al*., 2020, NAR)

``` bash 

cd input/data_folder &&
wget https://github.com/foerstner-lab/GRADitude/raw/main/tutorial_data/NC_000913.3_no_duplicates.gff && cd ../..

```

Once all the raw reads are downloaded. We can start with removing 
the adapter using [cutadapt]( https://doi.org/10.14806/ej.17.1.200).  


Before doing that we create the READemption folder where we will store the output that comes out from executing cutdadapt

``` bash 

singularity exec grad-seq-analysis-ecoli.sif reademption create -f READemption_analysis

```
If the commands works from your shell it should appear the READemption logo with no errors

``` bash 

   ___  _______   ___                 __  _
  / _ \/ __/ _ | / _ \___ __ _  ___  / /_(_)__  ___
 / , _/ _// __ |/ // / -_)  ' \/ _ \/ __/ / _ \/ _ \
/_/|_/___/_/ |_/____/\__/_/_/_/ .__/\__/_/\___/_//_/
                             / /
====================================================
========================================
=======================
==============

```

Once we create the READemption folder we can execute cutadapt.



``` bash 
ls input/raw_reads | parallel -k -j 10 \
singularity exec grad-seq-analysis-ecoli.sif cutadapt \
-q 20 \
-m 1 \
-a "AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC" \
-o READemption_analysis/input/reads/'$(basename {})'.bz2 \
input/raw_reads/{} \
> output/cutadapt_stats.txt

```
After executing cutadapt the trimmed output are already saved in the READemption/input/reads folder
as requested by READemption subcommand.

Now we have to copy the reference genome and the annotation 
in READemption/input/reference_sequences and READemption/input/annotations respectively
You can do it manually or you can run the following code:

``` bash 
cp -r input/data_folder/NC_000913.3_no_duplicates.gff READemption_analysis/input/annotations/

```

``` bash 
cp -r input/data_folder/GCF_000005845.2_ASM584v2_genomic.fna READemption_analysis/input/reference_sequences/

```

``` bash 
cp -r input/data_folder/ERCC92.fa READemption_analysis/input/reference_sequences/

```

Now we can finally start with the alignment.
The -p parameter can be increase or decreased based on the CPUs that are available

``` bash 

singularity exec grad-seq-analysis-ecoli.sif reademption align \
--project_path READemption_analysis \
-p 5 \
-a 95 \
-l 20 \
--fastq \
--progress

```

After the alignment is finished the user can continue running the coverage subcommand 
``` bash 

singularity exec grad-seq-analysis-ecoli.sif reademption coverage \
-p 4 \
--project_path READemption_analysis
```

Now the user can run the gene quantification. This subcommand will have as output one of the tables necessary for our further 
analysis with GRADitude.
With the parameter --features you can specify which features you want to quantify. For our analysis we decided to use 
CDS, rRNA, tRNA and ncRNA but many more features can be added, depending on the annotation file.


``` bash 
    singularity exec grad-seq-analysis-ecoli.sif reademption gene_quanti \
	    -p 4 \
	    --features CDS,rRNA,tRNA,ncRNA \
	    -l \
        --project_path READemption_analysis

```

After running the gene quantification, the 2 tables necessary for the downstream analysis are found in:

``` bash 
READemption_analysis/output/align/reports_and_stats ---> read_alignment_stats.csv
&
READemption_analysis/output/gene_quanti/gene_quanti_combined --> gene_wise_quantifications_combined.csv

```

Let's have a look at the folder structure we created right now:


``` bash 

├── grad-seq-analysis-ecoli.sif
├── input
└── output
└── READemption_analysis
    ├── input
    └── output


```

Now the user can create a folder GRADitude using the following subcommand

``` bash 

mkdir GRADitude && mkdir GRADitude/input GRADitude/output

```
and then your folder structure will be like the one showed below where there is an input
and output folder inside the GRADitude folder created

``` bash 
├── GRADitude
├── input
    └── output
├── grad-seq-analysis-ecoli.sif
├── input
└── output
└── READemption_analysis
    ├── input
    └── output
```

We now start the analysis copying all the necessary tables inside GRADitude


``` bash 
  cp -r READemption_analysis/output/align/reports_and_stats/read_alignment_stats.csv ./GRADitude/input/ &&
  cp -r READemption_analysis/output/gene_quanti/gene_quanti_combined/gene_wise_quantifications_combined.csv ./GRADitude/input/
```

