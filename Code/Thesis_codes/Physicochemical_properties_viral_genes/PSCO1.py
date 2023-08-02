from Bio import SeqIO
import pandas as pd


# Function to calculate Radzicka-Wolfenden accessible surface area
def calc_radzicka_surf(seq):
    surf_dict = {
        "A": 115.0,
        "C": 135.0,
        "D": 150.0,
        "E": 190.0,
        "F": 210.0,
        "G": 75.0,
        "H": 195.0,
        "I": 175.0,
        "K": 200.0,
        "L": 170.0,
        "M": 185.0,
        "N": 160.0,
        "P": 145.0,
        "Q": 180.0,
        "R": 225.0,
        "S": 115.0,
        "T": 140.0,
        "V": 155.0,
        "W": 255.0,
        "Y": 230.0
    }
    surf_sum = 0
    for aa in seq:
        if aa in surf_dict:
            surf_sum += surf_dict[aa]
    return surf_sum / len(seq)

# Function to calculate Dayhoff relative mutability
def calc_dayhoff_mut(seq):
    mut_dict = {
        "A": 0.2,
        "C": 1.5,
        "D": 6.7,
        "E": 8.1,
        "F": 0.8,
        "G": 0.3,
        "H": 2.8,
        "I": 0.5,
        "K": 10.9,
        "L": 0.4,
        "M": 1.2,
        "N": 4.4,
        "P": 2.1,
        "Q": 3.5,
        "R": 6.6,
        "S": 1.6,
        "T": 1.2,
        "V": 0.6,
        "W": 1.3,
        "Y": 2.3
    }
    mut_sum = 0
    for aa in seq:
        if aa in mut_dict:
            mut_sum += mut_dict[aa]
    return mut_sum / len(seq)



def calculate_amp07(sequence):
    """
    Calculates the AMP07 value for a protein sequence.
    """
    # Define the hydrophobicity scale
    hydrophobicity_scale = {
        'A': 0.5, 'C': 0.5, 'D': -3.5, 'E': -3.5,
        'F': 2.8, 'G': 0.0, 'H': -3.2, 'I': 4.5,
        'K': -3.9, 'L': 3.8, 'M': 1.9, 'N': -3.5,
        'P': -1.6, 'Q': -3.5, 'R': -4.5, 'S': -0.8,
        'T': -0.7, 'V': 4.2, 'W': -0.9, 'Y': -1.3
    }
    
    # Calculate the AMP07 value
    amp07 = sum([hydrophobicity_scale[aa] for aa in sequence]) / len(sequence)
    
    return amp07

def calculate_fasman(sequence):
    """
    Calculates the Melting Point (Fasman) value for a protein sequence.
    """
    # Define the melting point (Fasman) scale
    melting_point_scale = {
        'A': 47.0, 'C': 47.0, 'D': 146.0, 'E': 155.0,
        'F': 92.0, 'G': 8.0, 'H': 114.0, 'I': 119.0,
        'K': 135.0, 'L': 119.0, 'M': 105.0, 'N': 97.0,
        'P': 57.0, 'Q': 110.0, 'R': 148.0, 'S': 77.0,
        'T': 92.0, 'V': 105.0, 'W': 84.0, 'Y': 114.0
    }
    
    # Calculate the Melting Point (Fasman) value
    fasman = sum([melting_point_scale[aa] for aa in sequence]) / len(sequence)
    
    return fasman


# Define function to calculate amphiphilicity index (Mitaku et al., 2002)
def calc_amphiphilicity(sequence):
    # Define dictionary of amphiphilicity values for each amino acid
    amphiphilicity = {"A": 0.00, "R": -0.72, "N": -0.42, "D": -1.04, "C": 0.77, "Q": -0.58, "E": -1.03, "G": 0.01, "H": -0.40, "I": 0.60, "L": 0.60, "K": -0.99, "M": 0.26, "F": 0.94, "P": 0.12, "S": -0.22, "T": -0.06, "W": 1.03, "Y": 0.62, "V": 0.54}

    # Calculate the amphiphilicity index of the sequence
    amphiphilicity_seq = sum([amphiphilicity[aa] for aa in sequence])/len(sequence)

    return amphiphilicity_seq

# Define function to calculate buriability (Zhou-Zhou, 2004)
def calc_buriability(sequence):
    # Define dictionary of buriability values for each amino acid
    buriability = {"A": 0.178, "R": 0.590, "N": 0.463, "D": 0.511, "C": 0.886, "Q": 0.229, "E": 0.497, "G": 0.202, "H": 0.478, "I": 0.905, "L": 0.899, "K": 0.466, "M": 0.772, "F": 0.850, "P": 0.336, "S": 0.131, "T": 0.274, "W": 0.748, "Y": 0.531, "V": 0.829}

    # Calculate the buriability of the sequence
    buriability_seq = sum([buriability[aa] for aa in sequence])/len(sequence)

    return buriability_seq


# Read the input fasta file and create a dataframe to store the results
with open("E-proteins.fasta") as handle:
    records = list(SeqIO.parse(handle, "fasta"))

results = pd.DataFrame(columns=["Sequence ID", "Accessible Surface Area", "Relative Mutability", "AMP07", "Melting Point (Fasman)", "Amphiphilicity Index", "Buriability"])

# Iterate over each sequence and calculate the various properties
for record in records:
    surf = calc_radzicka_surf(str(record.seq))
    mut = calc_dayhoff_mut(str(record.seq))
    amp07 = calculate_amp07(str(record.seq))
    fasman = calculate_fasman(str(record.seq))
    amphiphilicity = calc_amphiphilicity(str(record.seq))
    buriability = calc_buriability(str(record.seq))

    results = results.append({
        "Sequence ID": record.id,
        "Accessible Surface Area": surf,
        "Relative Mutability": mut,
        "AMP07": amp07,
        "Melting Point (Fasman)": fasman,
        "Amphiphilicity Index": amphiphilicity,
        "Buriability": buriability
    }, ignore_index=True)

# Write the results to a csv file
results.to_csv("1.csv", index=False)
