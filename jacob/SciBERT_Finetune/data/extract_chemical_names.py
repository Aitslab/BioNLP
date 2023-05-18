import csv 
import json

entities_file_path = "chemprot/chemprot_training/chemprot_training_entities.tsv"
output_path = "artificial-building-blocks/element2_4_chemical_names_chemprot.txt"

chem_set = set()

# saves all entities marked as chemicals to list
with open(entities_file_path, encoding="utf8") as file:
    tsv_file = csv.reader(file, delimiter="\t")
    for line in tsv_file:
        if line[2] == "CHEMICAL": chem_set.add(line[-1])

# creates a new file with all chemicals
with open(output_path, 'x', encoding="utf8") as outfile:
    for item in chem_set:
        outfile.write(item + "\n")
