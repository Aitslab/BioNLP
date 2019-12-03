import pickle
from lxml import etree
from Protein import Protein

counter = 0
prefix = "{http://uniprot.org/uniprot}"

proteins = []

for event, element in etree.iterparse("uniprot_sprot.xml", tag=prefix + "entry"):
    prot = Protein()
    for child in element.getchildren():

        # Gets uniprot ID
        if child.tag == prefix + "accession" and prot.uniprotID is None:
            prot.uniprotID = child.text

        # Gets alternative names
        elif child.tag.endswith("protein"):
            for entry in child.getchildren():

                if entry.tag == prefix + "recommendedName" or entry.tag == prefix + "alternativeName":
                    for name in entry.getchildren():
                        prot.altNames.append(name.text)

        # Gets name and more alternative names
        elif child.tag == prefix + "gene":
            for entry in child.getchildren():

                if entry.tag == prefix + "name":
                    if entry.attrib["type"] == "primary":
                        prot.name = entry.text
                    elif entry.attrib["type"] == "synonym":
                        prot.altNames.append(entry.text)

        # Gets species name and ID
        elif child.tag == prefix + "organism":
            for entry in child.getchildren():

                if entry.tag == prefix + "name" and entry.attrib["type"] == "scientific":
                    prot.speciesName = entry.text
                elif entry.tag == prefix + "dbReference" and entry.attrib["type"] == "NCBI Taxonomy":
                    prot.speciesID = entry.attrib["id"]

        # Gets hgnc ID
        elif child.tag == prefix + "dbReference" and child.attrib["type"] == "HGNC":
            prot.hgncID = child.attrib["id"]

        # Gets ensembl IDs
        elif child.tag == prefix + "dbReference" and child.attrib["type"] == "Ensembl":
            prot.ensemblID["transcript"] = child.attrib["id"]
            for entry in child.getchildren():

                if entry.tag == "property" and entry.attrib["type"] == "protein sequence ID":
                    prot.ensemblID["protein"] = child.attrib["value"]
                elif entry.tag == "property" and entry.attrib["type"] == "gene ID":
                    prot.ensemblID["gene"] = child.attrib["value"]

    if prot.speciesID is not None:
        prot.ID = "LUGE" + "{:08d}".format(int(prot.speciesID)) + "{:08d}".format(counter)
    else:
        prot.ID = "LUGE00000000" + "{:08d}".format(counter)

    counter += 1

    proteins.append(prot)
    element.clear()
    if counter % 1000 == 0:
        print(counter)

pickle.dump(proteins, open("uniprot.out", "wb"))