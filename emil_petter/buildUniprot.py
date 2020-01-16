import pickle
from lxml import etree
from protein import Protein

# Goes through the Swissprot database xml and parses all the relevant data

prefix = "{http://uniprot.org/uniprot}"

proteins = []

for event, element in etree.iterparse("in/uniprot_sprot.xml", tag=prefix + "entry"):

    prot = Protein()

    nonEukaryotProtein = False

    for child in element.getchildren():
        if nonEukaryotProtein:
            break

        # Gets Uniprot ID
        # The xml lists old IDs as well, only the first one is relevant and the rest are ignored
        if child.tag == prefix + "accession":
            if not prot.uniprot_id:
                prot.uniprot_id.add(child.text)

        # Gets names
        elif child.tag.endswith("protein"):
            for entry in child.getchildren():
                if entry.tag == prefix + "recommendedName" or entry.tag == prefix + "alternativeName":
                    for name in entry.getchildren():
                        prot.names.add(name.text)

        # Gets official symbol and more names
        elif child.tag == prefix + "gene":
            for entry in child.getchildren():

                if entry.tag == prefix + "name":
                    if entry.attrib["type"] == "primary":
                        prot.symbol.add(entry.text)
                        prot.names.add(entry.text)
                    elif entry.attrib["type"] == "synonym":
                        prot.names.add(entry.text)

        # Gets species ID
        # Also checks that the protein belongs to a species in the domain Eukaryota
        elif child.tag == prefix + "organism":
            for entry in child.getchildren():

                if entry.tag == prefix + "dbReference" and entry.attrib["type"] == "NCBI Taxonomy":
                    prot.species_id = entry.attrib["id"]
                elif entry.tag == prefix + "lineage":
                    if entry.getchildren()[0].text != "Eukaryota":
                        nonEukaryotProtein = True
                        child.clear()
                        break

        # Gets HGNC ID
        elif child.tag == prefix + "dbReference" and child.attrib["type"] == "HGNC":
            prot.hgnc_id.add(child.attrib["id"])

        child.clear()

    element.clear()
    if nonEukaryotProtein:
        continue

    if len(prot.hgnc_id) > 1:
        counter += 1
    proteins.append(prot)

pickle.dump(proteins, open("out/uniprot.out", "wb"))
