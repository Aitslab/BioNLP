import pickle
from lxml import etree

prefix = "{http://uniprot.org/uniprot}"

proteins = {}

for event, element in etree.iterparse("../data/uniprot_sprot.xml", tag=prefix + "entry"):
    prot = {}
    nonEukaryotProtein = False
    uniprotID = None

    for child in element.getchildren():
        if nonEukaryotProtein:
            break

        # Gets uniprot ID
        if child.tag == prefix + "accession" and uniprotID is None:
            prot.setdefault("uniprotID", set()).add(child.text)
            uniprotID = child.text

        # Gets alternative names
        elif child.tag.endswith("protein"):
            for entry in child.getchildren():

                if entry.tag == prefix + "recommendedName" or entry.tag == prefix + "alternativeName":
                    for name in entry.getchildren():
                        prot.setdefault("altNames", set()).add(name.text)

        # Gets name and more alternative names
        elif child.tag == prefix + "gene":
            for entry in child.getchildren():

                if entry.tag == prefix + "name":
                    if entry.attrib["type"] == "primary":
                        prot["name"] = entry.text
                    elif entry.attrib["type"] == "synonym":
                        prot.setdefault("altNames", set()).add(entry.text)

        # Gets species name and ID
        elif child.tag == prefix + "organism":
            for entry in child.getchildren():

                if entry.tag == prefix + "name" and entry.attrib["type"] == "scientific":
                    prot["speciesName"] = entry.text
                elif entry.tag == prefix + "dbReference" and entry.attrib["type"] == "NCBI Taxonomy":
                    prot["speciesID"] = entry.attrib["id"]
                elif entry.tag == prefix + "lineage":
                    if entry.getchildren()[0].text != "Eukaryota":
                        nonEukaryotProtein = True
                        child.clear()
                        break

        # Gets hgnc ID
        elif child.tag == prefix + "dbReference" and child.attrib["type"] == "HGNC":
            prot.setdefault("hgncID", set()).add(child.attrib["id"])

        # Gets ensembl IDs
        elif child.tag == prefix + "dbReference" and child.attrib["type"] == "Ensembl":
            prot.setdefault("ensemblTranscriptID", set()).add(child.attrib["id"])
            for entry in child.getchildren():

                if entry.tag == "property" and entry.attrib["type"] == "protein sequence ID":
                    prot.setdefault("ensemblProteinID", set()).add(child.attrib["value"])
                elif entry.tag == "property" and entry.attrib["type"] == "gene ID":
                    prot.setdefault("ensemblGeneID", set()).add(child.attrib["value"])

        child.clear()

    element.clear()
    if nonEukaryotProtein:
        continue

    proteins[uniprotID] = prot

f = open("out/uniprot.out", "wb")
pickle.dump(proteins, f)
f.close()
