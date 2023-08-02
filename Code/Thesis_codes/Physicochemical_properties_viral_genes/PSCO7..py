from Bio.SeqUtils.ProtParam import ProteinAnalysis
import csv

# Define all three functions for calculating transfer free energy
# using Bull-Breese (1974), von Heijne-Blomberg (1979), and Simon (1976) methods

# Function for Bull-Breese (1974) method
def calc_transfer_free_energy_to_surface(sequence):
    """Calculate transfer free energy to surface of an amino acid sequence using Bull-Breese (1974) method"""
    aa_count = ProteinAnalysis(sequence).count_amino_acids()
    hydrophobic = aa_count['A'] + aa_count['I'] + aa_count['L'] + aa_count['M'] + aa_count['F'] + aa_count['V'] + aa_count['W']
    polar = aa_count['N'] + aa_count['C'] + aa_count['Q'] + aa_count['S'] + aa_count['T'] + aa_count['Y']
    charged = aa_count['D'] + aa_count['E'] + aa_count['H'] + aa_count['K'] + aa_count['R']
    transfer_free_energy_to_surface = 0.735 * hydrophobic + 0.49 * polar - 0.71 * charged
    return transfer_free_energy_to_surface


# Function for von Heijne-Blomberg (1979) method
def calc_transfer_free_energy_to_lipophilic_phase(sequence):
    """Calculate transfer free energy to lipophilic phase of an amino acid sequence using von Heijne-Blomberg (1979) method"""
    aa_count = ProteinAnalysis(sequence).count_amino_acids()
    hydrophobic = aa_count['A'] + aa_count['I'] + aa_count['L'] + aa_count['M'] + aa_count['F'] + aa_count['V'] + aa_count['W']
    polar = aa_count['N'] + aa_count['C'] + aa_count['Q'] + aa_count['S'] + aa_count['T'] + aa_count['Y']
    charged = aa_count['D'] + aa_count['E'] + aa_count['H'] + aa_count['K'] + aa_count['R']
    transfer_free_energy_to_lipophilic_phase = 1.84 * hydrophobic - 0.62 * polar - 1.03 * charged
    return transfer_free_energy_to_lipophilic_phase

# Function for Simon (1976) method
def calc_transfer_free_energy(sequence):
    """Calculate transfer free energy of an amino acid sequence using Simon (1976) method"""
    aa_count = ProteinAnalysis(sequence).count_amino_acids()
    hydrophobic = aa_count['A'] + aa_count['I'] + aa_count['L'] + aa_count['M'] + aa_count['F'] + aa_count['V'] + aa_count['W']
    polar = aa_count['N'] + aa_count['C'] + aa_count['Q'] + aa_count['S'] + aa_count['T'] + aa_count['Y']
    charged = aa_count['D'] + aa_count['E'] + aa_count['H'] + aa_count['K'] + aa_count['R']
    transfer_free_energy = 1.714 * hydrophobic + 0.642 * polar - 0.301 * charged
    return transfer_free_energy

# Read input fasta file
with open('E-proteins.fasta', 'r') as f:
    lines = f.readlines()

sequences = {}
current_seq = ''
for line in lines:
    if line.startswith('>'):
        current_seq = line[1:].strip()
        sequences[current_seq] = ''
    else:
        sequences[current_seq] += line.strip()

# Calculate transfer free energies for each sequence using all three methods
# and write to output csv file
with open('7.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Sequence', 'Transfer Free Energy to Surface', 'Transfer Free Energy to Lipophilic Phase', 'Transfer Free Energy'])
    for sequence in sequences:
        transfer_free_energy_to_surface = calc_transfer_free_energy_to_surface(sequences[sequence])
        transfer_free_energy_to_lipophilic_phase = calc_transfer_free_energy_to_lipophilic_phase(sequences[sequence])
        transfer_free_energy = calc_transfer_free_energy(sequences[sequence])
        writer.writerow([sequence, transfer_free_energy_to_surface, transfer_free_energy_to_lipophilic_phase, transfer_free_energy])
