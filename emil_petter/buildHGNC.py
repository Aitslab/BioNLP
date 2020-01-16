import json
import pickle
from protein import Protein

# Goes through the HGNC database json and parses all the relevant data

hgnc = json.load(open("in/hgnc_complete_set.json"))

proteins = []
for entry in hgnc["response"]["docs"]:
    prot = Protein()

    # Gets official symbol
    if "symbol" in entry:
        if prot.symbol:
            prot.symbol.add(entry["symbol"])
        prot.names.add(entry["symbol"])

    # Gets names
    if "alias_name" in entry:
        prot.names.update(entry["alias_name"])

    # Gets names
    if "alias_symbol" in entry:
        prot.names.update(entry["alias_symbol"])

    # Gets names
    if "prev_name" in entry:
        prot.names.update(entry["prev_name"])

    # Gets names
    if "prev_symbol" in entry:
        prot.names.update(entry["prev_symbol"])

    # Gets HGNC ID
    if "hgnc_id" in entry:
        prot.hgnc_id.add(entry["hgnc_id"])

    # Gets Uniprot ID
    if "uniprot_ids" in entry:
        prot.uniprot_id.update(entry["uniprot_ids"])

    # All proteins in this database are human proteins, hence the hard coded human ID
    prot.species_id = "9606"

    proteins.append(prot)

pickle.dump(proteins, open("out/hgnc.out", "wb"))
