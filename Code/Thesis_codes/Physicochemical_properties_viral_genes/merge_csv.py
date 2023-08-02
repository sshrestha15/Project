#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 17:13:25 2023

@author: Sojan
"""


import csv

# Define the names of the input files and the output file
input_files = ['1.csv', '2.csv', '3.csv', '4.csv', '5.csv', '6.csv', '7.csv', '8.csv']
output_file = 'combined.csv'


# Define a dictionary to store the combined data
combined_data = {}

# Loop over the input files
for input_file in input_files:
    # Open the file and create a CSV reader object
    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Loop over the rows in the file
        for row in reader:
            # Extract the sequence ID from the row
            seq_id = row['Sequence ID']
            
            # If the sequence ID is not in the combined data dictionary, create a new dictionary entry
            if seq_id not in combined_data:
                combined_data[seq_id] = {}
            
            # Loop over the keys in the row and add them to the combined data dictionary
            for key, value in row.items():
                if key != 'seq_id':
                    combined_data[seq_id][key] = value

# Open the output file and create a CSV writer object
with open(output_file, 'w') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write the header row to the output file
    writer.writerow(['seq_id'] + sorted(list(combined_data.values())[0].keys()))
    
    # Loop over the combined data and write each row to the output file
    for seq_id, data in combined_data.items():
        writer.writerow([seq_id] + [data[key] for key in sorted(data.keys())])




