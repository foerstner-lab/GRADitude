# 🧪 GRADitude Tutorial — Complete Analysis Example (No Docker/Singularity)

This tutorial will guide you through a **complete GRAD-seq analysis** using published data and the tool **GRADitude**.

We will use *Escherichia coli* GRAD-seq data from [Höer et al., 2020 (NAR)](https://www.ncbi.nlm.nih.gov/sra?term=SRP268299).  
Gradient fractions come from [Experiment SRX8595091](https://www.ncbi.nlm.nih.gov/sra?term=SRX8595091).

---

## 🛠 Environment Setup (Conda-based)

We use **Conda** for reproducibility and ease of setup. This will install `READemption`, `cutadapt`, `sra-tools`, and other required tools.

### Step 1: Configure Conda Channels (only once)

```bash
conda config --add channels conda-forge
conda config --add channels bioconda
```

### Step 2: Create and Activate Environment

```bash
conda create -n gradseq_env python=3.10 -y
conda activate gradseq_env
```

If you see: *Your shell has not been properly configured to use 'conda activate'*  
run `conda init` and restart your shell, or `source ~/.bashrc` (Linux bash) / `source ~/.zshrc` (macOS zsh).

### Step 3: Install required tools

```bash
conda install cutadapt sra-tools parallel wget unzip pigz bzip2 coreutils -y
conda install -c bioconda -c conda-forge -c till_sauerwein reademption -y
```

**SSL note:** If `fastq-dump` fails with certificate errors, check version:  
```bash

```
If < 2.11, update with:  
```bash
conda install -c bioconda -c conda-forge sra-tools=3.0.10 -y
```

** if `fastq-dump` --version still gives you a previous version then please install using it this:
```bash
wget https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/3.0.10/sratoolkit.3.0.10-mac64.tar.gz
tar -xzf sratoolkit.3.0.10-mac64.tar.gz
export PATH="$PWD/sratoolkit.3.0.10-mac64/bin:$PATH"
fastq-dump --version
```
---

## 📂 Set Up Directory Structure

```bash
mkdir -p GRADseq_analysis/input/{raw_reads,data_folder} GRADseq_analysis/output
cd GRADseq_analysis
```

Folder structure after setup:

```
GRADseq_analysis/
├── input/
│   ├── raw_reads/
│   └── data_folder/
└── output/
```

---

## ⬇ Download raw sequencing data from NCBI SRA

We download the **22 gradient fractions** from experiment SRX8595091 (Höer et al., 2020).  
Each SRR accession corresponds to one gradient fraction.

```bash
cd input/raw_reads

for i in SRR12067299 SRR12067300 SRR12067301          SRR12067302 SRR12067303 SRR12067304          SRR12067305 SRR12067306 SRR12067307          SRR12067308 SRR12067309 SRR12067310          SRR12067311 SRR12067312 SRR12067313          SRR12067314 SRR12067315 SRR12067316          SRR12067317 SRR12067318 SRR12067319          SRR12067320
do
    fastq-dump --bzip2 "$i"
done

cd ../..
```

Rename files for clarity:

```bash
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
cd ../../
```

---

## 📚 Download Reference Files

```bash
cd input/data_folder

# Reference genome
wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2_genomic.fna.gz
gzip -d GCF_000005845.2_ASM584v2_genomic.fna.gz

# ERCC spike-ins
wget https://assets.thermofisher.com/TFS-Assets/LSG/manuals/ERCC92.zip
unzip ERCC92.zip && rm ERCC92.zip ERCC92.gtf

# Annotation file
wget https://github.com/foerstner-lab/GRADitude/raw/main/tutorial_data/NC_000913.3_no_duplicates.gff

cd ../..
```

---

## ✂️ Trim Adapters with Cutadapt

```bash
reademption create -f READemption_analysis -s 'ecoli=Escherichia coli K-12 MG1655'

ls input/raw_reads | parallel -k -j 10   "cutadapt -q 20 -m 1 -a AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC   -o READemption_analysis/input/reads/{/.}.fastq.bz2 input/raw_reads/{}"   > output/cutadapt_stats.txt
```

---

## 📁 Prepare Reference Files for READemption

```bash
cp input/data_folder/NC_000913.3_no_duplicates.gff READemption_analysis/input/ecoli_annotations/
cp input/data_folder/GCF_000005845.2_ASM584v2_genomic.fna READemption_analysis/input/ecoli_reference_sequences/
cp input/data_folder/ERCC92.fa READemption_analysis/input/ecoli_reference_sequences/
```

---

## 🎯 Align Reads

```bash
reademption align --project_path READemption_analysis \
-p 5 \
-a 95 \
-l 20 \
--fastq \
--progress

```

---

## 📊 Generate Coverage

```bash
reademption coverage --project_path READemption_analysis -p 4
```

---

## 📈 Gene Quantification

```bash
reademption gene_quanti --project_path READemption_analysis --features CDS,rRNA,tRNA,ncRNA -p 4 -l
```

Output files required for GRADitude are located at:

```
READemption_analysis/output/align/reports_and_stats/read_alignment_stats.csv
READemption_analysis/output/gene_quanti/gene_quanti_combined/gene_wise_quantifications_combined.csv
```

---

## 📁 Prepare Input for GRADitude

```bash
mkdir -p GRADitude/input GRADitude/output

cp READemption_analysis/output/align/reports_and_stats/read_alignment_stats.csv GRADitude/input/
cp READemption_analysis/output/ecoli_gene_quanti_combined/gene_wise_quantifications_combined.csv GRADitude/input/
```

Folder structure now looks like:

```
GRADseq_analysis/
├── input/
│   ├── raw_reads/
│   └── data_folder/
├── output/
├── READemption_analysis/
│   ├── input/
│   └── output/
└── GRADitude/
    ├── input/
    └── output/
```

---

## ✅ Ready for GRADitude!

You have successfully:

- Preprocessed the raw reads  
- Performed read alignment  
- Generated coverage files  
- Quantified genes  

You're now ready to continue the analysis using **GRADitude**!



# Grad-seq Data Preprocessing & Formatting

Once the raw quantification tables are generated, the data must be formatted to be compatible with 
GRADitude's statistical modules. This phase involves extracting gene identifiers, removing non-relevant fractions 
(e.g., Total Lysate), and filtering out low-expression genes to ensure robust downstream analysis.


## Attribute Extraction & Merging

The first step is to extract specific identifier columns (such as Gene ID and Common Name) from the combined quantification file.

### Extract Attributes

Raw quantification tables (like those from READemption) often store gene metadata in a single, semi-structured column called Attributes (e.g., ID=gene01;Name=dnaA;Type=CDS). 
To perform analysis, these values must be extracted into their own separate columns.

Use the ```extract_gene_columns``` command to parse the GFF-style Attributes column and extract specific metadata keys 
(such as gene ID or Name) into their own dedicated columns.

```bash

graditude extract_gene_columns \
    -f input/gene_wise_quantifications_combined.csv \
    -names "gene" "Name" \
    -o input/gene_wise_extended.csv

```


### Consolidate Gene Identifiers 

After extracting attributes, gene identifiers may be scattered across different columns depending on
the annotation completeness (e.g., some entries use "Parent", others "name" or "ID"). This subcommand consolidates these columns into a single, 
definitive 'Gene' column to ensure every feature is uniquely identified for downstream analysis.

**Command:**

```bash
graditude merge_attributes \
    -f input/gene_wise_extended.csv \
    -o input/gene_wise_extended_merged.csv
```



### Data Cleaning: Removing Unwanted Columns

After consolidating the identifiers, the dataset often still includes experimental controls—such as
the Lysate (or Input)—and redundant metadata columns. While the lysate is essential for quality control,
it represents the cellular state prior to fractionation and does not belong to the sedimentation profile.
Including it can skew downstream statistical analyses (like normalization and clustering).

The ```drop_column``` removes the specified columns to produce a clean numerical matrix for analysis.


```bash
graditude drop_column \
    -f input/gene_wise_extended_merged.csv \
    -c "Grad-00L.fastq" "Name" "gene"\
    -o input/gene_wise_quanti.csv
    
```

To ensure accurate downstream normalization, the table containing the ERCC spike-in read counts
must undergo the same cleaning process as the gene quantification table. 
This involves removing the Lysate fraction,
so that the control data perfectly matches the dimensions of the gradient data.

```bash
graditude drop_column \
    -f input/read_alignment_stats.csv \
    -c "Grad-00L.fastq" "Species" \
    -o input/read_alignment_stats_no_lysate.csv
    
```
### Reorder Columns


After the previous processing steps (merging attributes and dropping controls), the definitive Gene 
identifier column is typically located at the very end of the table. To prepare the matrix for downstream analysis 
where the row identifier is expected to be the first column needs to be executed.

The ```move_columns``` shifts the specified number of columns from the end of the table to the beginning

```bash
graditude move_columns \
    -f input/gene_wise_quanti.csv \
    -n 1 \
    -o input/feature_count_table.csv

```

### Filter Low-Abundance Genes in the gene quantification table


Before running statistical analyses (like clustering or correlation), it is good practice to 
remove genes that have very low expression levels across the entire gradient. 
These "noisy" low-count features can destabilize normalization and clustering algorithms. 
This command filters the quantification table by summing the reads for each gene across 
the specified fractions and keeping only those that meet a minimum threshold.

The ```min_row_sum``` is used to filter out genes that have a total count less than the specified value.

```bash
graditude min_row_sum \
    -f input/feature_count_table.csv \
    -fc 11 \
    -fe 32 \
    -m 100 \
    -o input/gene_wise_100.csv

```


###  Filter Low-Abundance Genes in the ERCC table


This subcommand filters the ERCC quantification table based on a minimum read count threshold. 
It calculates the sum of reads for each ERCC transcript across all gradient fractions and discards those that
do not meet the specified threshold. 
This ensures that only robustly detected spike-ins are used for normalization and regression analysis

The ```min_row_sum_ercc``` is used to filter out ERCC transcripts that have a total count less than the specified value.```

```bash
graditude min_row_sum_ercc \
    -r input/read_alignment_stats_no_lysate.csv \
    -m 100 \
    -fr input/read_alignment_stats_100.csv
```


### Outlier Detection 
After filtering for read depth, we must verify that the ERCC spike-ins behave as expected. 
Theoretically, there should be a linear relationship between the log10(Read Counts) and the log10(Concentration) of the spike-ins.

This command performs a Robust Regression (RANSAC) on each gradient fraction to identify ERCCs that deviate significantly 
from this linear relationship. By removing these "bad" controls (outliers), we create a high-quality standard for the final normalization.

The ```robust_regression``` command is used to perform a robust regression analysis on the ERCC spike-in data. 
It identifies outliers that deviate significantly from the expected linear relationship between log10(Read Counts) and log10(Concentration) of the spike-ins. 
By removing these outliers, we ensure that the normalization process is based on a high-quality standard.


```bash
graditude robust_regression \
    -r input/read_alignment_stats_100.csv \
    -c ../input/data_folder/cms_095046.txt \
    -n 20 \
    -nc 18 \
    -mix 4 \
    -o input/read_alignment_stats_correlated_ERCC.csv

```

### Normalization

After removing the outlier spike-ins, we proceed to normalize the gene count data. 
Since sequencing depth can vary between different gradient fractions due to technical reasons (e.g., library preparation efficiency), 
raw read counts are not directly comparable.

The ```normalize``` subcommand uses the filtered, high-quality ERCC spike-ins to calculate Size Factors for each gradient fraction.
The method used is the "Median of Ratios" (similar to DESeq2), which is robust against extreme values. 
The command then divides the raw counts of the target genes by these specific size factors to produce a normalized 
expression table that allows for accurate comparison across the gradient.


```bash
graditude normalize \
    -f input/gene_wise_100.csv \
    -fc 11 \
    -fe 32 \
    -r input/read_alignment_stats_correlated_ERCC.csv \
    -rc 1 \
    -re 22 \
    -o input/Norm_100.csv \
    -s input/size_factor_100.csv

```


### Data Scaling 

Once the data has been normalized for sequencing depth, it is often useful to scale the expression profiles to facilitate visualization (e.g., heatmaps) 
and pattern recognition. Scaling focuses on the shape
of the distribution along the gradient rather than the absolute abundance.

The ```scaling``` command transforms the normalized counts row-by-row. In this analysis, we use the to_max method, 
which divides the counts of each gene by its maximum expression value across the gradient. This transformation 
sets the peak expression of every gene to 1.0, allowing for a direct comparison of sedimentation profiles between genes with very different expression levels.

```bash
graditude scaling \
    -f input/Norm_100.csv \
    -fc 11 \
    -fe 32 \
    -sm to_max \
    -o input/scaled_100_to_max.csv

```


### Clustering Analysis

To identify groups of genes with similar sedimentation profiles, we performed clustering analysis on the scaled expression data. 
Genes falling into the same cluster share similar sedimentation properties, suggesting they may be part of the same macromolecular complexes 
(e.g., ribosomal subunits) or share similar functional characteristics.

The clustering command applies unsupervised learning algorithms to partition the genes. In this workflow, we utilized the K-Means algorithm (-cm 'k-means').
The number of clusters was set to 6 (-nc 6) based on prior knowledge of the expected sedimentation patterns (e.g., free mRNA, monosomes, polysomes).
The input data was already scaled to the maximum value, so no further internal normalization was applied (-sm no_normalization)

```bash
graditude clustering \
    -f input/scaled_100_to_max.csv \
    -fc 11 \
    -fe 32 \
    -nc 6 \
    -p 1 \
    -cm 'k-means' \
    -sm no_normalization \
    -o output/k-means_100_max_6_cl.csv

```

### Visualization (t-SNE)   


To intuitively visualize the relationships between thousands of genes simultaneously, we employed t-Distributed Stochastic Neighbor Embedding (t-SNE).
While clustering groups genes into discrete sets, t-SNE projects the high-dimensional data (expression across 20+ gradient fractions) 
into a 2D space. In this map, genes with similar sedimentation profiles appear close to each other, while dissimilar genes are far apart.

The t_sne command generates interactive HTML plots (viewable in a web browser) where each dot represents a gene. We generate three views:

- Colored by Cluster: Validates the K-Means results (clusters should appear as distinct islands).
- Colored by RNA Class: Highlights the global distribution of RNA types (e.g., rRNA vs mRNA).
- Colored by Custom Lists: Specifically highlights proteins or genes of interest (e.g., RBPs) to see where they sediment relative to the RNA clusters.

```bash
graditude t_sne \
    -f output/k-means_100_max_6_cl.csv \
    -fc 11 \
    -fe 32 \
    -pp 30 \
    -list ../input/data_folder/2019-11-22_predicted_RBPs.txt \
    -names RBPs \
    -o1 output/t-SNE_cl_6cl_30pp.html \
    -o2 output/t-SNE_fe_6cl_30pp.html \
    -o3 output/t-SNE_RBPs_6cl_30pp.html

```






graditude plot_kinetics \
    -f GRADitude/input/scaled_100_to_max.csv \
    -fc 11 \
    -fe 32 \
    -g ssrA \
    -format pdf \
    -yl Normalized and scaled to max read counts




graditude plot_kinetics \
    -f GRADitude/input/feature_count_table.csv \
    -fc 11 \
    -fe 32 \
    -g ssrA \
    -format pdf \
    -yl "Raw read counts"

graditude plot_kinetics \
    -f GRADitude/input/scaled_100_to_max.csv \
    -fc 11 \
    -fe 32 \
    -g rnpB \
    -format pdf \
    -yl "Normalized and scaled to max read counts"

graditude plot_kinetics \
    -f GRADitude/input/feature_count_table.csv \
    -fc 11 \
    -fe 32 \
    -g rnpB \
    -format pdf \
    -yl "Raw read counts"


graditude clustering_elbow \
  -f GRADitude/input/scaled_100_to_max.csv \
  -fc 11 \
  -fe 32 \
  -min 2 \
  -max 15 \
  -o1 elbow_wcss.pdf \
  -o2 elbow_variance_explained.pdf


graditude selecting_specific_features \
    -n GRADitude/input/scaled_100_to_max.csv \
    -fc 11 \
    -fe 32 \
    -f sRNA ncRNA \
    -o GRADitude/input/sRNAs_filtered.csv


graditude clustering_elbow \
  -f GRADitude/input/sRNAs_filtered.csv \
  -fc 11 \
  -fe 32 \
  -min 2 \
  -max 15 \
  -o1 elbow_wcss-ncRNAs.pdf \
  -o2 elbow_variance_explained-ncRNAs .pdf



graditude clustering \
    -f GRADitude/input/sRNAs_filtered.csv \
    -fc 11 \
    -fe 32 \
    -nc 3 \
    -cm 'k-means' \
    -sm no_normalization \
    -o GRADitude/output/k-means_scaled_max_3_cl.csv


graditude silhouette_analysis \
    -c GRADitude/input/sRNAs_filtered.csv \
    -fc 11 \
    -fe 32 \
    -min 2 \
    -max 10 


graditude silhouette_analysis \
    -c GRADitude/input/scaled_100_to_max.csv \
    -fc 11 \
    -fe 32 \
    -min 2 \
    -max 10 


graditude t_sne \
            -f GRADitude/output/k-means_scaled_max_3_cl.csv \
            -fc 11 \
            -fe 32 \
            -pp 25 \
            -list input/20180202_classic_CsrA_sRNAs.txt \
            -names CsrA-targets Hfq-targets ProQ-targets \
            input/20180202_unique_Hfq_sRNAs_manual_curation.txt \
            input/20180202_unique_ProQ_sRNAs_manual_curation.txt \
            -o1 GRADitude/output//t-SNE_clusters__3cl-25pp \
            -o2 GRADitude/output//t-SNE_features_3cl-25pp \
           -o3 GRADitude/output/t-SNE_lists_3cl-25pp.html


graditude correlation_all_against_all \
    -f GRADitude/input/scaled_100_to_max.csv \
    -fc 11 \
    -fe 32 \
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


graditude extract_cluster_lists \
    -f GRADitude/output/k-means_scaled_max_3_cl.csv \
    -o GRADitude/output/gene_list.csv