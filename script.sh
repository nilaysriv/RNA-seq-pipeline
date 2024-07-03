#!/bin/bash
#Installation of required programs
sudo apt -y update
sudo apt -y upgrade
sudo apt install curl wget fastqc hisat2 subread samtools default-jre unzip python3-pip build-essential python3-tk
pip install pandas matplotlib seaborn scikit-learn

#Trimmomatic
wget http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/Trimmomatic-0.39.zip
unzip Trimmomatic-0.39.zip
ln -s Trimmomatic-0.39/trimmomatic-0.39.jar /usr/local/bin/trimmomatic-0.39.jar

#Annotation and Index files
wget ftp://ftp.ensembl.org/pub/release-111/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz 
wget ftp://ftp.ensembl.org/pub/release-111/gtf/homo_sapiens/Homo_sapiens.GRCh38.111.gtf.gz
gunzip *.gz
mkdir -p grch38
hisat2-build Homo_sapiens.GRCh38.dna.primary_assembly.fa grch38/genome 

THREAD_COUNT=$(($(nproc) - 2))
#Input
echo "Enter the path to the fastq labeled 1:"
read fastq_path
#Working directories
mkdir -p data
mkdir -p data/fastqc1
mkdir -p data/trimmed_reads
mkdir -p data/fastqc2
mkdir -p data/alignments
mkdir -p data/quant
#FastQC
echo "Running FastQC..."
for file in $fastq_path; do
    base=$(basename -s _1.fastq "$file")
    fastqc "$file" "Reads/${base}_2.fastq" -o data/fastqc1
done
#Trimmomatic
echo "Running Trimmomatic..."
for file in $fastq_path; do
    base=$(basename -s _1.fastq "$file")
    java -jar /usr/local/bin/trimmomatic-0.39.jar PE "Reads/${base}_1.fastq" "Reads/${base}_2.fastq" \
        "data/trimmed_reads/${base}.trimmed.paired.R1.fastq" "data/trimmed_reads/${base}.trimmed.unpaired.R1.fastq" \
        "data/trimmed_reads/${base}.trimmed.paired.R2.fastq" "data/trimmed_reads/${base}.trimmed.unpaired.R2.fastq" TRAILING:10 -phred33 -threads $THREAD_COUNT
done
#FastQC after trimming
echo "Running FastQC again after trimming..."
for file in data/trimmed_reads/*.trimmed.paired.R1.fastq; do
    base=$(basename -s .trimmed.paired.R1.fastq "$file")
    fastqc "$file" "data/trimmed_reads/${base}.trimmed.paired.R2.fastq" -o data/fastqc2
done
#HISAT2
echo "Running HISAT2 for alignment..."
for file in data/trimmed_reads/*.trimmed.paired.R1.fastq; do
    base=$(basename -s .trimmed.paired.R1.fastq "$file")
    hisat2 -q -x grch38/genome -1 "data/trimmed_reads/${base}.trimmed.paired.R1.fastq" -2 "data/trimmed_reads/${base}.trimmed.paired.R2.fastq" | samtools sort -o "data/alignments/${base}.bam"
done
#featureCounts
echo "Running featureCounts for quantification..."
BAM_FILES=(data/alignments/${base}.bam)
featureCounts -a Homo_sapiens.GRCh38.111.gtf -T 10 -p -o data/quant/output_data.txt "${BAM_FILES[@]}"
# Clean up feature matrix
echo "Cleaning up feature matrix..."
cut -f1,7- -s data/quant/output_data.txt | cat > data/quant/counts_data.txt
#visualization
echo "Running the Python script for visualization..."
python3 visualize_counts.py
