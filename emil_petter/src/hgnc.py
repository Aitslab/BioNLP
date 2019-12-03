import json

hgnc = json.load(open("../data/hgnc_complete_set.json"))
# counter = 0
proteins = {}
for entry in hgnc["response"]["docs"]:
    prot = {"altNames": []}
    
    if "symbol" in entry:
        prot["name"] = entry["symbol"]
    
    if "alias_name" in entry:
        prot["altNames"] += entry["alias_name"]

    if "alias_symbol" in entry:
        prot["altNames"] += entry["alias_symbol"]
    
    if "ensembl_gene_id" in entry:
        prot["ensemblGeneID"] = entry["ensembl_gene_id"]

    if "hgnc_id" in entry:
        prot["hgncID"] = entry["hgnc_id"]
    
    if "uniprot_ids" in entry:
        prot["uniprotID"] = entry["uniprot_ids"][0]
    
    if "entrez_id" in entry:
        prot["entrezID"] = entry["entrez_id"]
    
    prot["speciesID"] = "9606"
    prot["speciesName"] = "Homo sapiens"
    # ID = "LUGE00009606" + "{:08d}".format(counter)
    # counter += 1
    proteins[prot["hgncID"]] = prot

json.dump(proteins, open("hgnc.json", "w+"))