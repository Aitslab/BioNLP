import json
import pickle

f = open("../data/hgnc_complete_set.json")
hgnc = json.load(open("../data/hgnc_complete_set.json"))
f.close()

proteins = {}
for entry in hgnc["response"]["docs"]:
    prot = {}
    hgncID = None

    if "symbol" in entry:
        prot["name"] = entry["symbol"]

    if "alias_name" in entry:
        prot.setdefault("altNames", set()).update(entry["alias_name"])

    if "alias_symbol" in entry:
        prot.setdefault("altNames", set()).update(entry["alias_symbol"])

    if "ensembl_gene_id" in entry:
        prot.setdefault("ensemblGeneID", set()).add(entry["ensembl_gene_id"])

    if "hgnc_id" in entry:
        prot.setdefault("hgncID", set()).add(entry["hgnc_id"])
        hgncID = entry["hgnc_id"]

    if "uniprot_ids" in entry:
        prot.setdefault("uniprotID", set()).update(entry["uniprot_ids"])

    if "entrez_id" in entry:
        prot.setdefault("entrezID", set()).add(entry["entrez_id"])

    prot["speciesID"] = "9606"
    prot["speciesName"] = "Homo sapiens"
    proteins[hgncID] = prot

f = open("out/hgnc.out", "wb")
pickle.dump(proteins, f)
f.close()
