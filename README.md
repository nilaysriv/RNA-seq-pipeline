# RNA-seq-pipeline
A basic RNA sequence and microarray pipeline with GUI

# Installation
Run the following commands in an Ubuntu terminal to install the dependancies.
'''bash 
sudo apt -y update
sudo apt -y upgrade
sudo apt install curl wget fastqc hisat2 subread samtools default-jre unzip python3-pip build-essential
pip install pandas matplotlib seaborn scikit-learn
'''

#Trimmomatic
wget http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/Trimmomatic-0.39.zip
unzip Trimmomatic-0.39.zip
ln -s Trimmomatic-0.39/trimmomatic-0.39.jar /usr/local/bin/trimmomatic-0.39.jar
