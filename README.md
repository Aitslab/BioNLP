BioNLP
=======
Repository for student projects within biomedical text mining from Lund University. All code comes with a GPLv3 licence.


# Resources
## NLP libraries 
AllenNLP

NLP library built on PyTorch

https://allennlp.org/

CoreNLP

contains many of Stanford’s NLP tools

https://stanfordnlp.github.io/CoreNLP/

NLTK

https://www.nltk.org/

pytext

https://github.com/facebookresearch/pytext

spaCy

https://spacy.io/

scispaCy  

scispaCy is a Python package containing spaCy models for processing biomedical, scientific or clinical text  

https://allenai.github.io/scispacy/

https://arxiv.org/abs/1902.07669v3

keras

Hugging Face

https://github.com/huggingface

Gensim

for topic modelling

https://radimrehurek.com/gensim/



## Tokenizers
ChemTok

https://www.ncbi.nlm.nih.gov/pubmed/26942193

Huggingface tokenizers

https://github.com/huggingface/tokenizers

https://www.kaggle.com/funtowiczmo/hugging-face-tutorials-training-tokenizer

NLTK word_tokenize

NLTK regexp_tokenize

NLTK treebank tokenizer

https://www.nltk.org/_modules/nltk/tokenize/treebank.html

scispaCy tokenizer

keras text_to_word_sequence

## Parsers
Stanford Parser

Klein, D. and Manning, C. (2002). Fast Exact Inference with a Factored Model for Natural Language Parsing. In Advances in Neural Information Processing Systems.

https://nlp.stanford.edu/software/lex-parser.shtml

https://drive.google.com/open?id=1AwzeEIUt0Ar_hBEOLkFPRB_5ZNqCSlPp

Enju Parser

Miyao, Y. and Tsujii, J. (2008). Feature forest models for probabilistic HPSG parsing. Computational Linguistics

https://drive.google.com/open?id=1nZXHlnNiyCM9GeNF0fhKezvUaXzSp1bQ

CCG Parser

https://drive.google.com/open?id=1xCVL5lMF021BuqzX3L6A2RhbRqJYXY8a

Clark, S., & Curran, J. R. (2007). Wide-coverage efficient statistical parsing with CCG and log-linear models. Computational Linguistics, 33(4), 493-552.

## Negation and uncertainty detection

negBio

https://github.com/ncbi-nlp/NegBio

negSpacy

https://spacy.io/universe/project/negspacy




## Co-reference resolution and abbreviation resolution
https://github.com/huggingface/neuralcoref

Ab3P 

abbreviation detection tool

Sohn S, Comeau DC, Kim W, Wilbur WJ. (2008) Abbreviation definition identification based on automatic precision estimates. BMC Bioinformatics.  25;9:402. PubMed ID: 1881755

https://drive.google.com/file/d/1nKfgpZ01Qdd_vYm6llYxhZjsadkWM15J/view

scispaCy abbreviation tool

https://github.com/allenai/scispacy

SpanBERT

for co-reference resolution

https://github.com/facebookresearch/SpanBERT


## Annotation tools and formats
Comparison of different annotators

http://knot.fit.vutbr.cz/annotations/comparison.html

Comparison of Pubtator, BioC, PubAnnotations on an example

https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/tmTools/Format.html


BioC Viewer

for viewing and merging BioC annotations

http://viewer.bioqrator.org/

https://github.com/dongseop/bioc_viewer


http://viewer.bioqrator.org/

BioQrator

http://www.bioqrator.org/

brat
http://brat.nlplab.org/

Inception

https://inception-project.github.io/

BioC-JSON

converts between BioC XML and BioC json format

https://github.com/ncbi-nlp/BioC-JSON

BioCconvert

converts between BioC and PubAnnotation format

http://bioc.sourceforge.net/

## Pretrained models, word vectors, embeddings
fastText

https://fasttext.cc/


word2vec applied to corpus of 10,876,004 English abstracts of biomedical articles from PubMed

http://participants-area.bioasq.org/general_information/Task8a/

## Dictionaries & lexical databases
Open English Dictionary

https://www.learnthat.org/dictionary

WordNet

https://wordnet.princeton.edu/

VerbNet

https://verbs.colorado.edu/verbnet/

https://github.com/cu-clear/verbnet

BioVerbNet

https://github.com/cambridgeltl/bio-verbnet

UMLS Metathesaurus

https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/index.html

https://www.ncbi.nlm.nih.gov/books/NBK9684/

SPECIALIST Lexicon

https://lexsrv3.nlm.nih.gov/Specialist/Summary/lexicon.html

British National Corpus

http://www.natcorp.ox.ac.uk/



## Named entity linking
MetaMap

maps terms to UMLS

https://metamap.nlm.nih.gov/


## other BioNLP tools
dkpro core

https://github.com/dkpro/dkpro-core

SPECIALIST NLP tools

https://lexsrv3.nlm.nih.gov/Specialist/Home/index.html


SimConcept

a tool for resolving composite expressions such as BCA1/2 and galectin1-4

https://dl.acm.org/doi/10.1145/2649387.2649420



GENIA tagger

part-of-speech tagging, shallow parsing, and named entity recognition for biomedical text

https://drive.google.com/file/d/1C6xTYGvkJtFGC5gylkel_Rur761n3vz1/view
 
TaggerOne

https://www.ncbi.nlm.nih.gov/research/bionlp/Tools/taggerone/

Jensen Lab Tagger

https://bitbucket.org/larsjuhljensen/tagger/src/default/

EVEX/Turku Event Extraction System

https://turkunlp.org/bionlp.html

PMCID - PMID - Manuscript ID - DOI Converter

https://www.ncbi.nlm.nih.gov/pmc/pmctopmid/

## Bioinformatics databases and ontologies (can be used to build dictionaries)
### General & metadatabases

http://obofoundry.org/

BioPortal

http://bioportal.bioontology.org/


### Proteins & Genes
UniprotKB  

To create a dictionary of gene/protein names (contains protein and gene names including synonyms)  

https://www.uniprot.org/

HGNC

Gene Ontology  

Database with known function of genes 

http://geneontology.org/

Protein Ontology

https://proconsortium.org/

Ensembl

NCBI Gene

### Chemicals
Lists of databases

https://www.ebi.ac.uk/unichem/ucquery/listSources

https://www.sciencedirect.com/science/article/pii/S1740674915000062?via%

http://www.chemspider.com/DataSources.aspx

ChEMBL

manually curated database of bioactive molecules with drug-like properties

https://www.ebi.ac.uk/chembl/

CHEBI

https://www.ebi.ac.uk/chebi/

Chemspider

http://www.chemspider.com/

Human Metabolome Database

https://hmdb.ca/
 
FoodDB

information on food, food components and food additives

https://foodb.ca/


PubChem

To create a dictionary of chemicals/drugs (contains small molecules, but also larger molecules such as nucleotides, carbohydrates, lipids, peptides, and chemically-modified macromolecules) 

https://pubchem.ncbi.nlm.nih.gov/

Drugbank

www.drugbank.ca

Database with drugs and known protein targets (including references for the interaction)

RxNorm

provides normalized names for clinical drugs and links its names to many of the drug vocabularies

https://www.nlm.nih.gov/research/umls/rxnorm/index.html

Toxic Exposome Database

http://www.t3db.ca/

### Diseases & phenotypes
Mondo

https://mondo.monarchinitiative.org/pages/resources/

http://www.ontobee.org/ontology/MONDO?iri=http://purl.obolibrary.org/obo/MONDO_0000001


Human Phenotype Ontology

https://hpo.jax.org/app/

Disease Ontology  

http://disease-ontology.org/

OMIM  

Database with human diseases and known genes

Research Domain Critieria for Mental Health

https://www.nimh.nih.gov/research/research-funded-by-nimh/rdoc/definitions-of-the-rdoc-domains-and-constructs.shtml

### Tissues & Species
Cellosaurus
https://web.expasy.org/cellosaurus/

Cell Ontology

UBERON

anatomical entities; multicellular organisms and life-cycle stages

NCBI Taxonomy

International Committee on Taxonomy of Viruses

https://talk.ictvonline.org/files/master-species-lists/m/msl/8266

### Pathways & Reactions
KEGG
Database with known protein signalling pathways

Molecular Process Ontology


## Corpora for training and validation  
### General
Description of common BioNLP corpora

https://github.com/cambridgeltl/MTL-Bioinformatics-2016/blob/master/Additional%20file%201.pdf

Comparison of corpora

https://f1000research.com/articles/3-96/v1

Links to download several corpora

https://github.com/dterg/biomedical_corpora

http://compbio.ucdenver.edu/ccp/corpora/obtaining.shtml

Pubannotation http://pubannotation.org/

Corpora in BioC format  http://bioc.sourceforge.net/

https://github.com/dmis-lab/biobert

https://github.com/cambridgeltl/MTL-Bioinformatics-2016

https://github.com/openbiocorpora

https://www2.informatik.hu-berlin.de/~hakenber/links/benchmarks.html

http://mars.cs.utu.fi/PPICorpora/

### Individual corpora

BC5CDR

1500 PubMed titles and abstracts from CTD-Pfizer corpus used in BioCreative V chemical-disease relation task
 
CRAFT

97 full-text PMC articles

https://github.com/UCDenver-ccp/CRAFT

GeneTag  

20K Medline sentences; also available in BioC format and updated version GeneTag-05  

https://www.ncbi.nlm.nih.gov/pubmed/15960837

GENIA

http://www.geniaproject.org/

Universal Dependencies (v1.0) for the GENIA 1.0 Treebank, along with additional raw abstracts and metadata. 

https://github.com/allenai/genia-dependency-trees


HPO Gold Standard Corpus

http://www.bio-lark.org/hpo_res.html

Med Mentions

https://github.com/chanzuckerberg/MedMentions

Multilangual Named entity linking corpus

https://github.com/lasigeBioTM/MultiNEL-corpus

n2c2 (i2b2) corpora

https://portal.dbmi.hms.harvard.edu/projects/n2c2-nlp/

NCBI disease
https://www.sciencedirect.com/science/article/pii/S1532046413001974?via%3Dihub

PubMed 200k RCT dataset

to evaluate sentence classification

https://github.com/Franck-Dernoncourt/pubmed-rct

## Biomedical text sources
Cinahl

nursing, physical therapy and occupational therapy

Google scholar

Embase

including Emtree vocabulary, specialized in pharmacology and toxicology


PubMed

PMC

EuropePMC

Web of Science

multidisciplinary database with citation indexing

Libris

Swedish national search service containing titles held by Swedish research and many public libraries: books, reports, dissertations, etc.

Ovid

database interface providing access to PsycInfo, Medline or Global Health

SveMed+

bibliographic database that contains references to articles from Scandinavian journals in the disciplines of medicine, dentistry, health care, occupational therapy, nursing and physiotherapy

Worldcat

largest network of library content and services; excellent for finding books, ebooks, theses and dissertations

Wikipedia

1findr

https://1findr.1science.com/home

## Biomedical nomenclature
Drug naming rules

https://druginfo.nlm.nih.gov/drugportal/jsp/drugportal/DrugNameGenericStems.jsp


## Shared tasks and conferences within BioNLP
BioNLP Open Shared Tasks (BioNLP-OST) 

continuation of BioNLP Shared Task (BioNLP-ST)series

https://2019.bionlp-ost.org/

BioNLP Shared Task (BioNLP-ST) (2009, 2011, 2013, 2016)

http://2016.bionlp-st.org/

http://2013.bionlp-st.org/

http://2011.bionlp-st.org/

http://www.geniaproject.org/shared-tasks/bionlp-shared-task-2009


ACL-BioNLP2019 Workshop and associated MEDIQA 2019 task

https://sites.google.com/view/mediqa2019

https://aclweb.org/aclwiki/BioNLP_Workshop

BioCreative

https://biocreative.bioinformatics.udel.edu/

BioASQ

http://www.bioasq.org/

n2c2 (i2b2)

https://portal.dbmi.hms.harvard.edu/data-challenges/

List of several conferences with description

https://bionlp.info/bionlp-conferences/



## Other (relevant blogs, discussion forums, etc)  
Devblog with working example code for med-text relations extraction  

https://www.microsoft.com/developerblog/2016/09/13/training-a-classifier-for-relation-extraction-from-medical-literature/

BioStars bioinformatics forum  

https://www.biostars.org/

Link lists with many resources   

https://www2.informatik.hu-berlin.de/~hakenber/links/benchmarks.html

http://www.nactem.ac.uk/software.php

https://portal.dbmi.hms.harvard.edu/

http://www.becalm.eu/NerResources

http://bio.nlplab.org/

https://github.com/sebastianruder/NLP-progress/

https://transmartfoundation.org/

http://compbio.ucdenver.edu/corpora/bcresources.html


