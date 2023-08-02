from Bio import SeqIO
import pandas as pd

# Define functions for calculating hydrophobicity and hydrophobicity index
def calc_hydrophobicity(seq):
    # Prabhakaran, 1990
    hyd_phob = {'A': 0.47, 'R': -2.03, 'N': -0.6, 'D': -0.22, 'C': 1.54,
                'Q': -0.22, 'E': -0.19, 'G': 0.01, 'H': -0.41, 'I': 1.8,
                'L': 1.7, 'K': -1.42, 'M': 2.4, 'F': 2.91, 'P': 0.14,
                'S': -0.13, 'T': -0.14, 'W': 2.61, 'Y': 1.6, 'V': 1.22}
    return sum([hyd_phob[aa] for aa in seq]) / len(seq)

def calc_hydrophobicity_index(seq):
    # Fasman, 1989
    hyd_phob_index = {'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
                      'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
                      'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
                      'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2}
    return sum([hyd_phob_index[aa] for aa in seq]) / len(seq)
# Define the hydrophilicity scale
hydrophobicity = {
    'A': 1.8, 'C': 2.5, 'D': -3.5, 'E': -3.5, 'F': 2.8,
    'G': -0.4, 'H': -3.2, 'I': 4.5, 'K': -3.9, 'L': 3.8,
    'M': 1.9, 'N': -3.5, 'P': -1.6, 'Q': -3.5, 'R': -4.5,
    'S': -0.8, 'T': -0.7, 'V': 4.2, 'W': -0.9, 'Y': -1.3
}

# Define the side-chain contribution to protein stability
stability = {
    'A': -0.22, 'C': -0.13, 'D': -0.72, 'E': -0.62, 'F': -0.59,
    'G': -0.01, 'H': -0.40, 'I': -0.34, 'K': -1.10, 'L': -0.21,
    'M': -0.32, 'N': -0.60, 'P': -0.25, 'Q': -0.22, 'R': -1.76,
    'S': -0.18, 'T': -0.05, 'V': -0.07, 'W': -0.46, 'Y': -0.31
}

def calc_hydrophobicity_v2(seq):
    hydrophobicity_sum = 0
    for aa in seq:
        hydrophobicity_sum += hydrophobicity.get(aa, 0)
    return hydrophobicity_sum / len(seq)

# Define the function to calculate the side-chain contribution to protein stability for a sequence
def calc_stability(seq):
    stability_sum = 0
    for aa in seq:
        stability_sum += stability.get(aa, 0)
    return stability_sum

# Cid et al., 1992
hydrophobicity_scale = {
    'A': 0.17,
    'C': 0.77,
    'D': -1.53,
    'E': -1.61,
    'F': 1.06,
    'G': 0.01,
    'H': -0.96,
    'I': 0.31,
    'K': -0.23,
    'L': 0.56,
    'M': 0.23,
    'N': -0.48,
    'P': -0.01,
    'Q': -0.97,
    'R': -0.16,
    'S': -0.13,
    'T': -0.14,
    'V': 0.07,
    'W': 0.81,
    'Y': 0.26,
}

def calc_avg_hydrophobicity(seq):
    hydrophobicity_scores = [hydrophobicity_scale.get(aa, 0) for aa in seq]
    return sum(hydrophobicity_scores) / len(seq)

# Manavalan-Ponnuswamy, 1978
def calc_surrounding_hydrophobicity(seq, window=9):
    hydros = {
        "A": 0.62, "L": 1.21, "R": -2.53, "K": -1.5, "N": -0.78,
        "M": 0.64, "D": -0.9, "F": 1.38, "C": 0.79, "P": 0.12,
        "Q": -0.85, "S": -0.18, "E": -0.74, "T": -0.05, "G": 0.01,
        "W": 1.37, "H": 0.26, "Y": 0.49, "I": 1.02, "V": 0.91,
    }
    
    hydroscores = [hydros.get(aa, 0) for aa in seq]
    scores = []
    for i in range(len(seq)):
        scores.append(sum(hydroscores[max(0, i - window):i+window+1]))
    return sum(scores) / len(seq)

# Read in FASTA file and calculate physicochemical properties for each sequence
input_file = 'E-proteins.fasta'
output_file = '4.csv'

records = list(SeqIO.parse(input_file, 'fasta'))
results = []

for record in records:
    seq = str(record.seq)
    hyd_phob = calc_hydrophobicity(seq)
    hyd_phob_index = calc_hydrophobicity_index(seq)
    hyd_phob_v2 = calc_hydrophobicity_v2(seq)
    stability_val = calc_stability(seq)
    avg_hydro = calc_avg_hydrophobicity(seq)
    surr_hydro = calc_surrounding_hydrophobicity(seq)

    results.append([record.id, hyd_phob, hyd_phob_index, hyd_phob_v2, stability_val, avg_hydro, surr_hydro])

# Output results to CSV file
df = pd.DataFrame(results, columns=['Sequence ID', 'Hydrophobicity', 'Hydrophobicity Index', 'Hydrophobicity_v2', 'Stability', 'Average Hydrophobicity', 'Surrounding Hydrophobicity'])
df.to_csv(output_file, index=False)
