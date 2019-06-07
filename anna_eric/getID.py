# method: input protein name --> return ID
import re

def getID(p_name):
    with open('protein_name/protein_names_uniprot.txt', 'r') as file:
        p_names_db = file.readlines()
    with open('protein_name/protein_names_uniprot_indx.txt', 'r') as file:
        id_db = file.readlines()

    for i,line in enumerate(p_names_db):
        line = line.rstrip()
        if line == p_name:
            return id_db[i]

#Enter a protein name and it returns the uniprot ID
result = getID('Helianthinin-G3')
print(result)
