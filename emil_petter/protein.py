class Protein():
    def __init__(self):
        self.id = None
        self.symbol = set()
        self.names = set()
        self.species_id = None
        self.uniprot_id = set()
        self.hgnc_id = set()
    
    def update(self, other):
        self.symbol.update(other.symbol)
        self.names.update(other.names)
        self.uniprot_id.update(other.uniprot_id)
        self.hgnc_id.update(other.hgnc_id)
    