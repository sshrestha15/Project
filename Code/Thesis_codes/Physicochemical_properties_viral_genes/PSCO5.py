from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import csv
import pandas as pd

# Define a function to calculate physiochemical properties for a protein sequence
def calculate_properties(sequence):
    # Calculate molecular weight
    molecular_weight = ProteinAnalysis(sequence).molecular_weight()

    # Calculate instability index
    instability_index = ProteinAnalysis(sequence).instability_index()

    # Calculate Gravy score
    gravy = ProteinAnalysis(sequence).gravy()

    # Calculate isoelectric point
    isoelectric_point = ProteinAnalysis(sequence).isoelectric_point()

    # Calculate net charge at pH 7
    net_charge = ProteinAnalysis(sequence).charge_at_pH(7)

    # Calculate molar extinction without disulfides at 280 nm
    extinction_280 = ProteinAnalysis(sequence).molar_extinction_coefficient()

    # Calculate molar extinction with disulfides at 280 nm
    n_cys = sequence.count('C')
    n_trp = sequence.count('W')
    n_tyr = sequence.count('Y')
    extinction_280_disulfides = (n_cys * 120 + n_trp * 5600 + n_tyr * 1490) / molecular_weight

    return (molecular_weight, instability_index, gravy, isoelectric_point, net_charge, extinction_280, extinction_280_disulfides)
# Read the input FASTA file
sequences = SeqIO.parse("E-proteins.fasta", "fasta")

# Define the function to calculate Residue volume (Goldsack-Chalifoux, 1973)
def residue_volume(sequence):
    volume = {"A": 88.6, "R": 173.4, "N": 114.1, "D": 111.1, "C": 108.5, "E": 138.4, "Q": 143.8, "G": 60.1, "H": 153.2, "I": 166.7, "L": 166.7, "K": 168.6, "M": 162.9, "F": 189.9, "P": 112.7, "S": 89.0, "T": 116.1, "W": 227.8, "Y": 193.6, "V": 140.0}
    seq = ProteinAnalysis(sequence)
    return round(seq.molecular_weight() / sum([volume[aa] for aa in sequence]), 3)

# Define the function to calculate Steric parameter (Charton, 1981)
def steric_parameter(sequence):
    sp = {"A": 0.046, "R": 0.323, "N": 0.134, "D": 0.105, "C": 0.128, "E": 0.179, "Q": 0.182, "G": 0.000, "H": 0.226, "I": 0.186, "L": 0.186, "K": 0.292, "M": 0.221, "F": 0.318, "P": 0.059, "S": 0.062, "T": 0.108, "W": 0.388, "Y": 0.298, "V": 0.140}
    seq = ProteinAnalysis(sequence)
    return round(sum([sp[aa] for aa in sequence]) / len(sequence), 3)

# Define function to calculate refractivity (McMeekin et al., 1964)
def calc_refractivity(sequence):
    # Define dictionary of refractivity values for each amino acid
    refractivity = {"A": 4.34, "R": 26.66, "N": 10.76, "D": 11.47, "C": 2.35, "Q": 14.45, "E": 15.72, "G": 0.00, "H": 19.77, "I": 9.99, "L": 9.99, "K": 21.29, "M": 5.67, "F": 21.81, "P": 8.36, "S": 4.44, "T": 6.82, "W": 49.65, "Y": 29.05, "V": 7.44}

    # Calculate the refractivity of the sequence
    refractivity_seq = sum([refractivity[aa] for aa in sequence])

    return refractivity_seq

# Define function to calculate bitterness (Venanzi, 1984)
def calc_bitterness(sequence):
    # Define dictionary of bitterness values for each amino acid
    bitterness = {"A": 0.17, "R": 1.81, "N": 0.42, "D": 1.23, "C": 0.05, "Q": 1.10, "E": 1.45, "G": 0.01, "H": 0.96, "I": 0.31, "L": 0.36, "K": 1.16, "M": 0.19, "F": 0.45, "P": 0.13, "S": 0.13, "T": 0.14, "W": 0.38, "Y": 0.32, "V": 0.21}

    # Calculate the bitterness of the sequence
    bitterness_seq = sum([bitterness[aa] for aa in sequence])

    return bitterness_seq

# Initialize dataframe to store the results
results = pd.DataFrame(columns=["Sequence ID", "Molecular Weight", "Instability Index", "Gravy", "Isoelectric Point", "Net Charge at pH 7", "Molar Extinction at 280 nm", "Molar Extinction at 280 nm with disulfides", "Residue volume", "Steric parameter", "Refractivity", "Bitterness"])

# Iterate over each sequence in the input file
for sequence in sequences:
    # Calculate the physiochemical properties for the sequence
    properties = calculate_properties(str(sequence.seq))
    
    # Calculate additional properties for the sequence
    vol = residue_volume(str(sequence.seq))
    sp = steric_parameter(str(sequence.seq))
    refractivity = calc_refractivity(str(sequence.seq))
    bitterness = calc_bitterness(str(sequence.seq))

    # Append the results to the dataframe
    results = results.append({"Sequence ID": sequence.id, "Molecular Weight": properties[0], "Instability Index": properties[1], "Gravy": properties[2], "Isoelectric Point": properties[3], "Net Charge at pH 7": properties[4], "Molar Extinction at 280 nm": properties[5], "Molar Extinction at 280 nm with disulfides": properties[6], "Residue volume": vol, "Steric parameter": sp, "Refractivity": refractivity, "Bitterness": bitterness}, ignore_index=True)

# Write the results to a csv file
results.to_csv("5.csv", index=False)
