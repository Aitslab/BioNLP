# EDAN70-project
Repository for the course project in computer science EDAN70.


Day by day log in python notebook [log](log.ipynb).


Final report in [overleaf](https://www.overleaf.com/project/5ca3678e16331457dbbc3c58 "overleaf").


Some of the manually annotated files can be found in [manual annotations](manual_annotations.pdf). The abstracts that were manually annotated is in the text file [selected_abstracts](selected_abstracts.txt).

## Docria files
All docria files can be found in the folder [docria](https://www.dropbox.com/sh/mmcr13996tju74f/AABG2qNlPHDregsoDJ6kXFNaa?dl=0 "dropbox").


## Requirements
* Python 3.6+
* Maven 3.x (the newer the better)


## Downloads
### Pubmed data
[pubmed](https://fileadmin.cs.lth.se/nlp/pubmed/pubmed2018.tar) - 25.6 GiB and corresponding [checksum](https://fileadmin.cs.lth.se/nlp/pubmed/pubmed2018.tar.md5).

### UniProtKB
The xml file can be downloaded directly at [uniprot](ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.xml.gz "download") or at their [website](https://www.uniprot.org/downloads "uniprot") and selecting the Reviewed (Swiss-Prot) version.

### Docria
* For python: ```pip install docria```
* For java: 
```
git clone https://github.com/marcusklang/docria.git
cd docria/java
mvn install
```

## Running Java server
Before running the python code, the Java server needs to be setup. First, make sure that docria is downloaded properly as shown above. Then unzip the file provided by Marcus Klang: [klang](klang.zip), some modifications have been done to his original files. Go to /klang/mention-index-py4j/, and run the commands 
```
mvn package
cd target
java -jar mentions-index-py4j-1.0-SNAPSHOT.jar
```
The server should then be up and running and you are ready to run the python code.


## Running the dictionary
Unpack the pubmed abstracts in the repo (anna_eric/pubmed2018). Then the python code [xml_to_json](xml_to_json) can be run to unpack the zipped xml files and turn them into json files.

Then the file [tagger](tagger.py) can be run to process each of these json files to docria files with matches. By changing the 'run' variable, this python code can also be used to run the highlighter on given text (```run = 'text'```). Also to get a file format that can be used with the GENETAG scorer (```run = 'score'```).

To get the UniProt ID of a given matched protein the code in [getID](getID.py) can be run. If no match is found it could be that the gene/protein name is from GENETAG and not UniProt.

## Validation
Downloading GENETAG from medtag, the evaluator can be run using perl in the terminal as:
```perl alt_eval.perl [Gold] [Scored file]```

If alt_eval.perl is in the same folder as the repo, the evaluator can be run on e.g. the file genetag_all.out specifically with:
```perl alt_eval.perl Gold2.format genetag/genetag_all.out``` . Use this [Gold2.format](Gold2.format) instead of the Gold.format file that you get from GENETAG. 

