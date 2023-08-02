from Bio import SeqIO
import pandas as pd

# Function to calculate Charton-Charton polarizability parameter
def calc_charton_polar(seq):
    polar_dict = {
        "A": 0.217,
        "C": 0.251,
        "D": 0.212,
        "E": 0.215,
        "F": 0.279,
        "G": 0.195,
        "H": 0.245,
        "I": 0.242,
        "K": 0.224,
        "L": 0.233,
        "M": 0.224,
        "N": 0.204,
        "P": 0.205,
        "Q": 0.217,
        "R": 0.226,
        "S": 0.195,
        "T": 0.208,
        "V": 0.234,
        "W": 0.293,
        "Y": 0.274
    }
    polar_sum = 0
    for aa in seq:
        if aa in polar_dict:
            polar_sum += polar_dict[aa]
    return polar_sum / len(seq)

# Function to calculate Chothia average volume of buried residue
def calc_chothia_buried(seq):
    buried_dict = {
        "A": 88.6,
        "C": 108.5,
        "D": 111.1,
        "E": 138.4,
        "F": 189.9,
        "G": 60.1,
        "H": 153.2,
        "I": 166.7,
        "K": 168.6,
        "L": 166.0,
        "M": 162.9,
        "N": 90.0,
        "P": 112.7,
        "Q": 144.1,
        "R": 172.9,
        "S": 89.0,
        "T": 116.1,
        "V": 140.0,
        "W": 227.8,
        "Y": 193.6
    }
    buried_sum = 0
    for aa in seq:
        if aa in buried_dict:
            buried_sum += buried_dict[aa]
    return buried_sum / len(seq)

# Thermophilicity values for each amino acid using TSS scale
tss = {"A": -0.4, "C": -1.0, "D": -3.8, "E": -4.2, "F": -3.7,
       "G": -2.4, "H": -2.6, "I": -1.5, "K": -3.9, "L": 0.0,
       "M": 0.0, "N": -2.6, "P": -0.4, "Q": -3.5, "R": -3.5,
       "S": -1.4, "T": -1.8, "V": 0.0, "W": -3.3, "Y": -3.5}

# Function to calculate average thermophilicity score
def calc_thermophilicity(seq):
    score = sum(tss.get(aa, 0) for aa in seq)
    return score / len(seq)

# Read the fasta file and calculate the average properties for each sequence
sequences = SeqIO.parse("E-proteins.fasta", "fasta")
results = []
for seq in sequences:
    polar = calc_charton_polar(str(seq.seq))
    buried = calc_chothia_buried(str(seq.seq))
    thermophilicity = calc_thermophilicity(str(seq.seq))
    results.append([seq.id, polar, buried, thermophilicity])

# Write the results to a CSV file
df = pd.DataFrame(results, columns=["Sequence ID", "Polarizability Parameter", "Average Volume of Buried Residue", "Thermophilicity"])
df.to_csv("6.csv", index=False)
