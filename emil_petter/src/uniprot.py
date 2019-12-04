import pickle
from lxml import etree

prefix = "{http://uniprot.org/uniprot}"

proteins = {}

for event, element in etree.iterparse("../data/uniprot_sprot.xml", tag=prefix + "entry"):
    prot = {"altNames": set()}
    for child in element.getchildren():

        # Gets uniprot ID
        if child.tag == prefix + "accession" and "uniprotID" not in prot:
            prot["uniprotID"] = child.text

        # Gets alternative names
        elif child.tag.endswith("protein"):
            for entry in child.getchildren():

                if entry.tag == prefix + "recommendedName" or entry.tag == prefix + "alternativeName":
                    for name in entry.getchildren():
                        prot["altNames"].add(name.text)

        # Gets name and more alternative names
        elif child.tag == prefix + "gene":
            for entry in child.getchildren():

                if entry.tag == prefix + "name":
                    if entry.attrib["type"] == "primary":
                        prot["name"] = entry.text
                    elif entry.attrib["type"] == "synonym":
                        prot["altNames"].add(entry.text)

        # Gets species name and ID
        elif child.tag == prefix + "organism":
            for entry in child.getchildren():

                if entry.tag == prefix + "name" and entry.attrib["type"] == "scientific":
                    prot["speciesName"] = entry.text
                elif entry.tag == prefix + "dbReference" and entry.attrib["type"] == "NCBI Taxonomy":
                    prot["speciesID"] = entry.attrib["id"]

        # Gets hgnc ID
        elif child.tag == prefix + "dbReference" and child.attrib["type"] == "HGNC":
            prot["hgncID"] = child.attrib["id"]

        # Gets ensembl IDs
        elif child.tag == prefix + "dbReference" and child.attrib["type"] == "Ensembl":
            prot["ensemblTranscriptID"] = child.attrib["id"]
            for entry in child.getchildren():

                if entry.tag == "property" and entry.attrib["type"] == "protein sequence ID":
                    prot["ensemblPropertyID"] = child.attrib["value"]
                elif entry.tag == "property" and entry.attrib["type"] == "gene ID":
                    prot["ensemblGeneID"] = child.attrib["value"]

    proteins[prot["uniprotID"]] = prot
    element.clear()

pickle.dump(proteins, open("uniprot.out", "wb"))
