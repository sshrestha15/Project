#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 12:16:25 2023

@author: Sojan
"""

import pandas as pd
import numpy as np
from Bio import SeqIO

def calculate_hydrophobic_moment(sequence):
    """
    Calculates the hydrophobic moment for a protein sequence.
    """
    # Define the hydrophobicity scale
    hydrophobicity_scale = {
        'A': 0.5, 'C': 0.5, 'D': -3.5, 'E': -3.5,
        'F': 2.8, 'G': 0.0, 'H': -3.2, 'I': 4.5,
        'K': -3.9, 'L': 3.8, 'M': 1.9, 'N': -3.5,
        'P': -1.6, 'Q': -3.5, 'R': -4.5, 'S': -0.8,
        'T': -0.7, 'V': 4.2, 'W': -0.9, 'Y': -1.3
    }
    
    # Calculate the hydrophobic moment
    x = []
    y = []
    z = []
    for i, aa in enumerate(sequence):
        x.append(hydrophobicity_scale[aa] * np.cos(i * np.pi / len(sequence)))
        y.append(hydrophobicity_scale[aa] * np.sin(i * np.pi / len(sequence)))
        z.append(0.0)
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    z_mean = np.mean(z)
    mag = np.sqrt(x_mean ** 2 + y_mean ** 2 + z_mean ** 2)
    x_mean /= mag
    y_mean /= mag
    z_mean /= mag
    return (x_mean, y_mean, z_mean)


# Define function to calculate Alpha-helix and Beta-strand indices
def calc_indices(seq):
    # Define dictionary with amino acid indices for Alpha-helix and Beta-strand
    alpha_helix_dict = {'A': 1.44, 'R': 0.98, 'N': 0.67, 'D': 0.67, 'C': 1.19,
                        'Q': 0.98, 'E': 0.67, 'G': 1.34, 'H': 1.13, 'I': 1.27,
                        'L': 1.34, 'K': 1.17, 'M': 1.20, 'F': 1.38, 'P': 1.44,
                        'S': 0.77, 'T': 0.83, 'W': 1.37, 'Y': 1.47, 'V': 1.21}
    
    beta_strand_dict = {'A': 0.97, 'R': 0.90, 'N': 0.67, 'D': 0.67, 'C': 1.19,
                        'Q': 1.10, 'E': 0.67, 'G': 1.34, 'H': 0.87, 'I': 1.60,
                        'L': 1.22, 'K': 0.87, 'M': 1.67, 'F': 1.28, 'P': 1.52,
                        'S': 1.33, 'T': 1.20, 'W': 1.40, 'Y': 1.47, 'V': 1.65}

    # Calculate the Alpha-helix and Beta-strand indices
    alpha_helix_index = sum([alpha_helix_dict.get(aa, 0) for aa in seq]) / len(seq)
    beta_strand_index = sum([beta_strand_dict.get(aa, 0) for aa in seq]) / len(seq)

    # Return the indices as a tuple
    return (alpha_helix_index, beta_strand_index)

def calc_alpha_helix(sequence):
    helix_prop = {'A': 1.45, 'L': 1.34, 'R': 0.98, 'K': 1.03, 'N': 0.76, 'M': 1.20,
                  'D': 0.63, 'F': 1.19, 'C': 0.91, 'P': 0.57, 'Q': 0.94, 'S': 0.77,
                  'E': 0.77, 'T': 1.07, 'G': 0.53, 'W': 1.07, 'H': 1.00, 'Y': 0.69,
                  'I': 1.60, 'V': 1.70}
    helix_score = 0
    for aa in sequence:
        if aa in helix_prop:
            helix_score += helix_prop[aa]
    return helix_score/len(sequence)

def calc_beta_sheet(sequence):
    sheet_prop = {'A': 0.97, 'L': 0.57, 'R': 0.81, 'K': 1.16, 'N': 0.68, 'M': 1.67,
                  'D': 0.87, 'F': 1.30, 'C': 0.77, 'P': 0.57, 'Q': 1.10, 'S': 0.77,
                  'E': 0.95, 'T': 0.83, 'G': 0.53, 'W': 1.23, 'H': 0.71, 'Y': 1.47,
                  'I': 0.97, 'V': 0.66}
    sheet_score = 0
    for aa in sequence:
        if aa in sheet_prop:
            sheet_score += sheet_prop[aa]
    return sheet_score/len(sequence)

def calculate_chou_fasman_prop(fasta_file, output_file):
    sequences = []
    for record in SeqIO.parse(fasta_file, "fasta"):
        sequences.append(record.seq)
    helix_frequencies = [calc_alpha_helix(seq) for seq in sequences]
    sheet_frequencies = [calc_beta_sheet(seq) for seq in sequences]
    data = {'Sequence': sequences, 'Alpha Helix Frequency': helix_frequencies, 'Beta Sheet Frequency': sheet_frequencies}
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)


# Read the input FASTA file and calculate properties for each sequence
input_file = "E-proteins.fasta"
sequences = {}
with open(input_file, "r") as f:
    for line in f:
        if line.startswith(">"):
            header = line.strip()[1:]
            sequences[header] = ""
        else:
            sequences[header] += line.strip()

hydrophobic_moments = []
indices = []
chou_fasman = []

for seq_id, sequence in sequences.items():
    hydrophobic_moment = calculate_hydrophobic_moment(sequence)
    hydrophobic_moments.append([seq_id, hydrophobic_moment[0], hydrophobic_moment[1], hydrophobic_moment[2]])

    alpha_helix_index, beta_strand_index = calc_indices(sequence)
    indices.append([seq_id, alpha_helix_index, beta_strand_index])

    helix_freq = calc_alpha_helix(sequence)
    sheet_freq = calc_beta_sheet(sequence)
    chou_fasman.append([seq_id, helix_freq, sheet_freq])

# Save the result to a CSV file
df1 = pd.DataFrame(hydrophobic_moments, columns=['Sequence ID', 'Hydrophobic Moment X', 'Hydrophobic Moment Y', 'Hydrophobic Moment Z'])
df2 = pd.DataFrame(indices, columns=['Sequence ID', 'Alpha-helix index', 'Beta-strand index'])
df3 = pd.DataFrame(chou_fasman, columns=['Sequence ID', 'Alpha Helix Frequency', 'Beta Sheet Frequency'])

combined_df = df1.merge(df2, on='Sequence ID').merge(df3, on='Sequence ID')
combined_df.to_csv('3.csv', index=False)
