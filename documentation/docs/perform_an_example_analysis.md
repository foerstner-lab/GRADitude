# 🧪 GRADitude Tutorial — Complete Analysis Example (No Docker/Singularity)

This tutorial will guide you through a **complete GRAD-seq analysis** using published data and the tool **GRADitude**.

We will use *Escherichia coli* GRAD-seq data from [Höer et al., 2020 (NAR)](https://www.ncbi.nlm.nih.gov/sra?term=SRP268299).  
Gradient fractions come from [Experiment SRX8595091](https://www.ncbi.nlm.nih.gov/sra?term=SRX8595091).

---

## 🛠 Environment Setup (Conda-based)

We use **Conda** for reproducibility and ease of setup. This includes the installation of `READemption`, `cutadapt`, and other required tools.

### Step 1: Configure Conda Channels (only once)

```
conda config --add channels conda-forge
conda config --add channels bioconda
conda config --add channels till_sauerwein
```

### Step 2: Create and Activate Environment

```
conda create -n reademption_env python=3.9 -y
conda activate reademption_env
```

If you see: *Your shell has not been properly configured to use 'conda activate'*  
run `conda init` and restart your shell, or `source ~/.bashrc` (Linux bash) / `source ~/.zshrc` (macOS zsh).

### Step 3: Install required tools

```
conda install cutadapt -y
conda install sra-tools -y
conda install parallel -y
conda install -c till_sauerwein reademption -y
```

**SSL note:** If `fastq-dump` fails with certificate errors, check version:  
```
fastq-dump --version
```
If < 2.11, update:  
```
conda install -c bioconda sra-tools -y
```

---

## 📂 Set Up Directory Structure

```
mkdir -p GRADseq_analysis/input/{raw_reads,data_folder} GRADseq_analysis/output
cd GRADseq_analysis
```

---

## ⬇ Download raw sequencing data from NCBI SRA

We download the **22 gradient fractions** from experiment SRX8595091 (Höer et al., 2020).  
Each SRR accession corresponds to one gradient fraction.

```
cd input/raw_reads

for i in SRR12067299 SRR12067300 SRR12067301 \
         SRR12067302 SRR12067303 SRR12067304 \
         SRR12067305 SRR12067306 SRR12067307 \
         SRR12067308 SRR12067309 SRR12067310 \
         SRR12067311 SRR12067312 SRR12067313 \
         SRR12067314 SRR12067315 SRR12067316 \
         SRR12067317 SRR12067318 SRR12067319 \
         SRR12067320
do
    fastq-dump --bzip2 "$i"
done
```

Rename files for clarity:  
```
mv SRR12067299.fastq.bz2 Grad-00L.fastq.bz2
mv SRR12067300.fastq.bz2 Grad-01.fastq.bz2
mv SRR12067301.fastq.bz2 Grad-02.fastq.bz2
mv SRR12067302.fastq.bz2 Grad-03.fastq.bz2
mv SRR12067303.fastq.bz2 Grad-04.fastq.bz2
mv SRR12067304.fastq.bz2 Grad-05.fastq.bz2
mv SRR12067305.fastq.bz2 Grad-06.fastq.bz2
mv SRR12067306.fastq.bz2 Grad-07.fastq.bz2
mv SRR12067307.fastq.bz2 Grad-08.fastq.bz2
mv SRR12067308.fastq.bz2 Grad-09.fastq.bz2
mv SRR12067309.fastq.bz2 Grad-10.fastq.bz2
mv SRR12067310.fastq.bz2 Grad-11.fastq.bz2
mv SRR12067311.fastq.bz2 Grad-12.fastq.bz2
mv SRR12067312.fastq.bz2 Grad-13.fastq.bz2
mv SRR12067313.fastq.bz2 Grad-14.fastq.bz2
mv SRR12067314.fastq.bz2 Grad-15.fastq.bz2
mv SRR12067315.fastq.bz2 Grad-16.fastq.bz2
mv SRR12067316.fastq.bz2 Grad-17.fastq.bz2
mv SRR12067317.fastq.bz2 Grad-18.fastq.bz2
mv SRR12067318.fastq.bz2 Grad-19.fastq.bz2
mv SRR12067319.fastq.bz2 Grad-20.fastq.bz2
mv SRR12067320.fastq.bz2 Grad-21P.fastq.bz2
```

```
cd ../..
```

---

## 📚 Download Reference Files

```
cd input/data_folder

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

## ✂️ Trim Adapters with Cutadapt

```
reademption create -f READemption_analysis

ls input/raw_reads | parallel -k -j 10 cutadapt -q 20 -m 1 -a "AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC" -o READemption_analysis/input/reads/{.}.fastq.bz2 input/raw_reads/{} > output/cutadapt_stats.txt
```

---

## 📁 Prepare Reference Files for READemption

```
cp input/data_folder/NC_000913.3_no_duplicates.gff READemption_analysis/input/annotations/
cp input/data_folder/GCF_000005845.2_ASM584v2_genomic.fna READemption_analysis/input/reference_sequences/
cp input/data_folder/ERCC92.fa READemption_analysis/input/reference_sequences/
```

---

## 🎯 Align Reads

```
reademption align --project_path READemption_analysis -p 5 -a 95 -l 20 --fastq --progress
```

---

## 📊 Generate Coverage

```
reademption coverage --project_path READemption_analysis -p 4
```

---

## 📈 Gene Quantification

```
reademption gene_quanti --project_path READemption_analysis --features CDS,rRNA,tRNA,ncRNA -p 4 -l
```

---

## 📁 Prepare Input for GRADitude

```
mkdir -p GRADitude/input GRADitude/output

cp READemption_analysis/output/align/reports_and_stats/read_alignment_stats.csv GRADitude/input/
cp READemption_analysis/output/gene_quanti/gene_quanti_combined/gene_wise_quantifications_combined.csv GRADitude/input/
```

---

## ✅ Ready for GRADitude!

You have successfully:

- Preprocessed the data
- Performed read alignment
- Generated coverage
- Quantified genes

You're now ready to continue the analysis using **GRADitude**!
