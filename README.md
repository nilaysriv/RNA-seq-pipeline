# RNA-seq-pipeline
A basic RNA sequence and microarray pipeline with GUI

# Installation
## Installation of dependancies
Run the following commands in an Ubuntu terminal(WSL2/Native).
```bash
sudo apt -y update
sudo apt -y upgrade
sudo apt install curl wget fastqc hisat2 subread samtools default-jre unzip python3-pip build-essential
pip install pandas matplotlib seaborn scikit-learn
```
### Trimmomatic
```bash
wget http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/Trimmomatic-0.39.zip
unzip Trimmomatic-0.39.zip
ln -s Trimmomatic-0.39/trimmomatic-0.39.jar /usr/local/bin/trimmomatic-0.39.jar
```

## Running the script
```bash
git clone https://github.com/nilaysriv/RNA-seq-pipeline
cd RNA-seq-pipeline
python3 runme.py
```
