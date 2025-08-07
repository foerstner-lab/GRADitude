# 🧪 GRADitude Tutorial — Complete Analysis Example

This tutorial will guide you through a **complete GRAD-seq analysis** using published data and the tool **GRADitude**.

We will use *Escherichia coli* GRAD-seq data from [Höer et al., 2020 (NAR)](https://www.ncbi.nlm.nih.gov/sra?term=SRP268299).

---

# 🛠️ Environment Setup (Conda-based, No Docker/Singularity)

We use **Conda** for reproducibility and ease of setup. This includes the installation of `READemption`, `cutadapt`, and other required tools.

## ➤ Step 1: Configure Conda Channels (only once)

```bash
conda config --add channels conda-forge
conda config --add channels bioconda
conda config --add channels till_sauerwein
```

## ➤ Step 2: Create and Activate Environment

```bash
conda create -n reademption_env python=3.9 reademption -c till_sauerwein -c conda-forge -c bioconda -y
conda activate reademption_env
```

This will install:

- `READemption`
- `cutadapt`
- `sra-tools`
- `parallel`
- all Python dependencies

---

# 📁 Set Up Directory Structure

```bash
mkdir -p GRADseq_analysis/input/{raw_reads,data_folder} GRADseq_analysis/output
cd GRADseq_analysis
```

---

# ⬇️ Download the Raw Data

```bash
cd input/raw_reads
for i in $(seq -f "SRR120672%02g" 99 120); do
    fastq-dump --bzip2 $i
done
```

Rename for clarity:

```bash
mv SRR12067299.fastq.bz2 Grad-00L.fastq.bz2
mv SRR12067300.fastq.bz2 Grad-01.fastq.bz2
# ...
mv SRR12067320.fastq.bz2 Grad-21P.fastq.bz2
```

---

# 📚 Download Reference Files

```bash
cd ../data_folder

# Reference genome
wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2_genomic.fna.gz
gzip -d GCF_000005845.2_ASM584v2_genomic.fna.gz

# ERCC spike-ins
wget https://assets.thermofisher.com/TFS-Assets/LSG/manuals/ERCC92.zip
unzip ERCC92.zip && rm ERCC92.zip ERCC92.gtf

# Annotation file
wget https://github.com/foerstner-lab/GRADitude/raw/main/tutorial_data/NC_000913.3_no_duplicates.gff

cd ../../
```

---

# ✂️ Trim Adapters with Cutadapt

```bash
reademption create -f READemption_analysis

ls input/raw_reads | parallel -k -j 10 \
cutadapt \
-q 20 \
-m 1 \
-a "AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC" \
-o READemption_analysis/input/reads/{.}.fastq.bz2 \
input/raw_reads/{} \
> output/cutadapt_stats.txt
```

---

# 📁 Prepare Reference Files for READemption

```bash
cp input/data_folder/*.gff READemption_analysis/input/annotations/
cp input/data_folder/*.fna READemption_analysis/input/reference_sequences/
cp input/data_folder/ERCC92.fa READemption_analysis/input/reference_sequences/
```

---

# 🎯 Align Reads

```bash
reademption align \
--project_path READemption_analysis \
-p 5 \
-a 95 \
-l 20 \
--fastq \
--progress
```

---

# 📊 Generate Coverage

```bash
reademption coverage \
--project_path READemption_analysis \
-p 4
```

---

# 📈 Gene Quantification

```bash
reademption gene_quanti \
--project_path READemption_analysis \
--features CDS,rRNA,tRNA,ncRNA \
-p 4 \
-l
```

---

# 📁 Prepare Input for GRADitude

```bash
mkdir -p GRADitude/input GRADitude/output

cp READemption_analysis/output/align/reports_and_stats/read_alignment_stats.csv GRADitude/input/
cp READemption_analysis/output/gene_quanti/gene_quanti_combined/gene_wise_quantifications_combined.csv GRADitude/input/
```

---

# ✅ Ready for GRADitude!

You have successfully:

- Preprocessed the data
- Performed read alignment
- Generated coverage
- Quantified genes

You're now ready to continue the analysis using **GRADitude**!
