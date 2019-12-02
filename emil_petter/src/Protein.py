class Protein:
    def __init__(self):
        self.ID = None
        self.name = None
        self.altNames = []
        self.speciesID = None  # maybe should be list
        self.speciesName = None  # maybe should be list

        self.uniprotID = None
        self.hgncID = None
        self.ncbiID = None
        self.ensemblID = {}
        self.wikidataID = None
        self.entrezID = None
        self.refseqID = None
