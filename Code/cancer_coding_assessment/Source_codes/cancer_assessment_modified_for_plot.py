#!/usr/bin/env python3
# -*- coding: utf-8 -*-



"""
Created on Sun Apr 30 15:28:00 2023

@author: sojanshrestha
"""
import os
import pandas as pd
import numpy as np
from scipy.stats import fisher_exact
import matplotlib.pyplot as plt

#path of the file

#path = "/directory/folder_name/mafs"
path = "/Users/Sojan/Desktop/coding_assessment/mafs"

#All 50 mafs file are read and combined using the above path
#create empty list
all_maf_data = []
#Initiate a loop to iterate through the files
for file in os.listdir(path):
    #read the file with .maf
    if file.endswith(".maf"):
        #read maf file, appended, and combined
        maf_data = pd.read_csv(os.path.join(path, file), sep='\t', comment='#')
        all_maf_data.append(maf_data)

combined_maf = pd.concat(all_maf_data, ignore_index=True)
#print(combined_maf)

#Subset for mutations that are not of the variant classifictaion "Silennt. Filtering out silent mutations. 
nonsilent_mutations = combined_maf[combined_maf['Variant_Classification'] != 'Silent']

#Output results of nonsilent mutations to a csv file
#nonsilent_mutations.to_csv('nonsilent_mutations.csv', index=False)

#group the non-silent mutation
count_mutations = nonsilent_mutations.groupby(['Hugo_Symbol', 'Protein_Change']).size().reset_index(name='counts')
#Output results of count_mutations to a csv file
#count_mutations.to_csv('count_mutations.csv', index=True)

#Find the most common mutations (15)
common_mutations = count_mutations.nlargest(15,'counts')

#Output results of common mutations to a csv file
common_mutations.to_csv('common_mutations.csv', index=False)

#load the tsv file which consists individual patient response
#sample_information = pd.read.csv( '/directory/folder_name/filename,tsv', sep='\t')
sample_information = pd.read_csv('/Users/Sojan/Desktop/coding_assessment/sample-information.tsv', sep='\t')

#Merge patient response
merged_data = nonsilent_mutations.merge(sample_information[['Tumor_Sample_Barcode', 'Response']], on='Tumor_Sample_Barcode')

#Count mutated samples based on patient response
counts_mutation_response = merged_data.groupby(['Hugo_Symbol', 'Response']).size().unstack().fillna(0)
#print(counts_mutation_response)

#Perform a statistcial test to find any mutated genes that is enriching in patients. 
#Fisher's exact test to compare the non random assocaiton between two variables. 
#create empty list
odds_ratios = []
p_values = []
#iterate through count mutation response and calculate odds ratio and p-value for each gene
for index, row in counts_mutation_response .iterrows():
    odds_ratio, p_value = fisher_exact([[row['Responder'], row['Non-Responder']], [row['Non-Responder'].sum(), row['Responder'].sum()]])
    odds_ratios.append(odds_ratio)
    p_values.append(p_value)

#Odds-ratios and p-values are added as new columns
counts_mutation_response ['odds_ratio'] = odds_ratios
counts_mutation_response ['p_value'] = p_values
#Output results of counts_mutation_response to a csv file
#counts_mutation_response.to_csv('counts_mutation_response.csv', index=False)

#list of genes with p-value
significant_genes = counts_mutation_response [counts_mutation_response ['p_value'] < 0.05]
#print(significant_genes)

#Output results of significant_genes  to a csv file
#significant_genes.to_csv('significant_genes.csv', index=True)

#create a scatter plot of genes 
p_values = counts_mutation_response['p_value']
significant_indices = p_values < 0.05
fig = plt.figure(figsize=(10, 8))

plt.scatter(counts_mutation_response ['Responder'] + counts_mutation_response ['Non-Responder'], counts_mutation_response ['p_value'], c=['r' if significant else 'b' for significant in significant_indices])
plt.xlabel('Number of Mutated Patients')
plt.ylabel("P-Value")
plt.title("Number of Mutations for Treatment from Patients Response")
plt.grid(True)
plt.axhline(y=0.05, color='g', linestyle='dashed', label="P-Value threshold (p-value < 0.05 indcated by red dot)")
plt.ylim([-0.1, 1.1])
plt.legend()
plt.show()

#Identify the most sigficantly enriched genes
most_significant_genes = counts_mutation_response .loc[counts_mutation_response ['odds_ratio'].idxmax()].name

#Count the mutant sanples and wild type samples
mutant_samples = set(merged_data[merged_data['Hugo_Symbol'] == most_significant_genes]['Tumor_Sample_Barcode'])
#print(mutant_samples)
wild_type_samples = set(sample_information['Tumor_Sample_Barcode']) - mutant_samples
#print(wild_type_samples)

mutant_mutation_rate = sample_information[sample_information['Tumor_Sample_Barcode'].isin(mutant_samples)]['Mutations_per_Mb']
#print(mutant_mutation_rate)
wild_type_mutation_rate = sample_information[sample_information['Tumor_Sample_Barcode'].isin(wild_type_samples)]['Mutations_per_Mb']
#print(wild_type_mutation_rate)

#Output results (most sigficantly enriched genes) to a csv
#mutation_summary = pd.DataFrame({'Sample Type': ['Wild-type', 'Mutant'], 'Number of Samples': [len(wild_type_samples), len(mutant_samples)]})
#mutation_summary.to_csv('mutation_summary.csv', index=False)

#with open('Mutation_summary_with_most_significant_genes.csv', 'w') as f:
    #f.write("Mutation Summary:\n")
    #f.write(mutation_summary.to_string(index=False))
    #f.write("\n\nMost significant gene: " + most_significant_genes)
    
#Scatter  plotfor nonsynonymous mutaions per megabase in the mutant vs. wild-type samples
fig, ax = plt.subplots(figsize=(10,8))
plt.scatter(np.zeros(len(mutant_mutation_rate)), mutant_mutation_rate, marker='o', color='r', alpha=0.5)
plt.scatter(np.ones(len(wild_type_mutation_rate)), wild_type_mutation_rate, marker='o', color='b', alpha=0.5)
plt.xticks([0, 1], ['Mutant', 'Wild-type'])
plt.xlim([-0.5, 1.5])
plt.ylabel('Non-synonymous Mutations per Mb')
plt.title(f"Mutation Rate in Mutant Sample against Wild-type Samples")
plt.show()
