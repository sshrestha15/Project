from Bio.SeqUtils.ProtParam import ProteinAnalysis
from Bio import SeqIO
import csv
import pandas as pd

# Define the function to calculate Bulkiness
def bulkiness(sequence):
    bulk = {"A": 88.6, "R": 173.4, "N": 114.1, "D": 111.1, "C": 108.5, "E": 138.4, "Q": 143.8, "G": 60.1, "H": 153.2, "I": 166.7, "L": 166.7, "K": 168.6, "M": 162.9, "F": 189.9, "P": 112.7, "S": 89.0, "T": 116.1, "W": 227.8, "Y": 193.6, "V": 140.0}
    seq = ProteinAnalysis(sequence)
    return round(seq.molecular_weight() / sum([bulk[aa] for aa in sequence]), 3)

# Define the function to calculate Mean polarity
def mean_polarity(sequence):
    pol = {"A": 0.046, "R": -0.034, "N": 0.087, "D": 0.051, "C": 0.128, "E": 0.024, "Q": 0.065, "G": 0.074, "H": 0.024, "I": 0.102, "L": 0.102, "K": -0.023, "M": 0.069, "F": 0.065, "P": 0.052, "S": 0.056, "T": 0.064, "W": 0.085, "Y": 0.081, "V": 0.079}
    seq = ProteinAnalysis(sequence)
    return round(sum([pol[aa] for aa in sequence]) / len(sequence), 3)

# define function to calculate physiochemical properties
def calc_charges_and_norm_vol(seq):
    # Positive charge
    pos_charge = seq.count("R") + seq.count("K") + seq.count("H")
    # Negative charge
    neg_charge = seq.count("D") + seq.count("E")
    # Normalized van der Waals volume
    vol_dict = {"A": 67, "R": 148, "N": 96, "D": 91, "C": 86, "Q": 114, "E": 109, "G": 48,
                "H": 118, "I": 124, "L": 124, "K": 135, "M": 124, "F": 135, "P": 90,
                "S": 73, "T": 93, "W": 163, "Y": 141, "V": 105}
    vol_sum = sum([vol_dict.get(aa, 0) for aa in seq])
    norm_vol = vol_sum / len(seq)
    # return values as a tuple
    return (pos_charge, neg_charge, norm_vol)

results = []
prop_dict = {}
for record in SeqIO.parse("E-proteins.fasta", "fasta"):
    sequence = str(record.seq)
    name = record.id

    bulk = bulkiness(sequence)
    pol = mean_polarity(sequence)
    results.append((name, bulk, pol))

    pos_charge, neg_charge, norm_vol = calc_charges_and_norm_vol(sequence)
    prop_dict[name] = (pos_charge, neg_charge, norm_vol)

prop_df = pd.DataFrame.from_dict(prop_dict, orient="index", columns=["Pos_charge", "Neg_charge", "Norm_vol"])
prop_df.reset_index(inplace=True)
prop_df.columns = ["Name", "Pos_charge", "Neg_charge", "Norm_vol"]

results_df = pd.DataFrame(results, columns=["Name", "Bulkiness", "Mean_polarity"])

combined_df = pd.merge(results_df, prop_df, on="Name")
combined_df.to_csv("2.csv", index=False)
