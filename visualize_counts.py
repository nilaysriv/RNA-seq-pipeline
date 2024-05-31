import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the output data
data = pd.read_csv('counts_data.txt', sep='\t')

# Plot a histogram of read counts
plt.hist(data.iloc[:, 1:].sum(axis=1), bins=50)
plt.xlabel('Total read count')
plt.ylabel('Number of genes')
plt.title('Distribution of total read counts')
plt.show()

# Plot a heatmap of read counts
plt.figure(figsize=(10, 10))
sns.heatmap(data.iloc[:, 1:], annot=True, cmap='YlGnBu')
plt.xlabel('Genes')
plt.ylabel('Samples')
plt.title('Read counts per gene and sample')
plt.show()

# Plot a boxplot of read counts for each sample
sns.boxplot(data=data.melt(id_vars=data.columns[0], var_name='sample', value_name='count'))
plt.xlabel('Sample')
plt.ylabel('Read count')
plt.title('Distribution of read counts per sample')
plt.show()

# Plot a scatterplot of read counts for each pair of samples
sns.pairplot(data, hue=data.columns[0], diag_kind='kde')
plt.show()

# Plot a correlation matrix of read counts for each pair of genes
corr_matrix = data.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.xlabel('Genes')
plt.ylabel('Genes')
plt.title('Correlation matrix of read counts')
plt.show()