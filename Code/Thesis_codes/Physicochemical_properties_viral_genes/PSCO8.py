from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import pandas as pd
import math

# Define all functions for calculating the properties

# Define the average volumes of residues dictionary
avg_volumes = {'A': 88.6, 'R': 173.4, 'N': 114.1, 'D': 111.1, 'C': 108.5, 'Q': 143.8, 'E': 138.4, 'G': 60.1,
               'H': 153.2, 'I': 166.7, 'L': 166.7, 'K': 168.6, 'M': 162.9, 'F': 189.9, 'P': 112.7, 'S': 89.0,
               'T': 116.1, 'W': 227.8, 'Y': 193.6, 'V': 140.0}

# Define the linker index dictionary
linker_index = {'A': 4.34, 'C': 4.32, 'D': 4.66, 'E': 4.68, 'F': 5.98, 'G': 3.97, 'H': 5.24, 'I': 5.34,
                'K': 5.70, 'L': 5.98, 'M': 5.98, 'N': 4.91, 'P': 4.34, 'Q': 4.91, 'R': 5.70, 'S': 4.01,
                'T': 4.77, 'V': 5.11, 'W': 6.48, 'Y': 5.66}

# Define a function to calculate the average volume of residues for a sequence
def calc_avg_volume(seq):
    vol_sum = 0
    for aa in seq:
        vol_sum += avg_volumes[aa]
    return round(vol_sum / len(seq), 2)

# Define a function to calculate the linker index for a sequence
def calc_linker_index(seq):
    index_sum = 0
    for aa in seq:
        index_sum += linker_index[aa]
    return round(index_sum / len(seq), 2)

# Define function to calculate absolute entropy using Hutchens (1970) method
def calc_absolute_entropy(sequence):
    """Calculate absolute entropy of an amino acid sequence using Hutchens (1970) method"""
    aa_count = ProteinAnalysis(sequence).count_amino_acids()
    n = sum(aa_count.values())
    entropy = 0
    for aa in aa_count:
        p_i = aa_count[aa] / n
        if p_i > 0:
            entropy += p_i * math.log2(p_i)
    absolute_entropy = -1.43 * entropy + 1.38
    return absolute_entropy

def calc_norm_nt_helix(seq):
    helix_score = {'A': 1.45, 'C': 0.77, 'D': -0.18, 'E': -0.26, 'F': 1.38,
                   'G': 0.38, 'H': 0.11, 'I': 1.32, 'K': -0.35, 'L': 1.70,
                   'M': 2.00, 'N': -0.64, 'P': 0.12, 'Q': -0.69, 'R': -0.16,
                   'S': 0.85, 'T': 0.52, 'V': 1.22, 'W': 0.85, 'Y': 0.76}
    n_term_seq = seq[:5]
    norm_helix_score = sum([helix_score[aa] for aa in n_term_seq]) / 5
    return norm_helix_score

def calc_norm_ct_helix(seq):
    helix_score = {'A': 0.72, 'C': 0.44, 'D': 0.72, 'E': 0.62, 'F': 0.94,
                   'G': 0.50, 'H': 0.78, 'I': 1.00, 'K': 1.42, 'L': 0.76,
                   'M': 0.67, 'N': 0.48, 'P': 0.12, 'Q': 0.98, 'R': 0.95,
                   'S': 0.55, 'T': 0.70, 'V': 0.92, 'W': 1.14, 'Y': 0.61}
    c_term_seq = seq[-5:]
    norm_helix_score = sum([helix_score[aa] for aa in c_term_seq]) / 5
    return norm_helix_score
# Read input fasta file
records = list(SeqIO.parse("E-proteins.fasta", "fasta"))

# Loop over each sequence and calculate the properties
results = []
for record in records:
    seq = str(record.seq)

    # Calculate properties from the first code
    avg_volume = calc_avg_volume(seq)
    linker = calc_linker_index(seq)

    # Calculate property from the second code
    absolute_entropy = calc_absolute_entropy(seq)

    # Calculate properties from the third code
    norm_nt_helix = calc_norm_nt_helix(seq)
    norm_ct_helix = calc_norm_ct_helix(seq)

    # Store the results in a dictionary
    result = {'ID': record.id,
              'Average Volume': avg_volume,
              'Linker Index': linker,
              'Absolute Entropy': absolute_entropy,
              'NormNTHelix': norm_nt_helix,
              'NormCTHelix': norm_ct_helix}

    # Append the dictionary to the list of results
    results.append(result)

# Convert the list of results to a Pandas dataframe and save it to a CSV file
df = pd.DataFrame(results)
df.to_csv('8.csv', index=False)
