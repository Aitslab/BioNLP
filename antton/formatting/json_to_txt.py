##This script takes a JSON file of a paper (wish I knew the name of the format)
#and makes it into a txt file, puting a newline each paragraph.
#It also creates a 'rebuild_reference.txt' file, necessary at the end of the BioBERT pipeline I created.
#This file contains information not given by the BioBERT output but necessary in the PubAnnotation JSON files.

import sys
import json
import csv
from os import listdir
from os.path import isfile, join


mypath = '../comm_use_subset_100/'  #TODO: Probably better to use 'sys' so that path can be specified by user
#filenames = [f for f in listdir(mypath) if isfile(join(mypath, f))]  # List of all input JSON file names.
with open('generated_text.txt', 'w') as out_file:
    with open('rebuild_reference.txt', 'w') as out_reference:
        # File to use when transforming BioBERT output to PubAnnotation
        # Structure: <name of JSON> <cord_uid> <sourcedb> <sourceid> <divid>
        with open('metadata_comm_use_subset_100.csv', 'r') as metadata_file:
            metadata_reader = csv.reader(metadata_file)
            for line in metadata_reader:
                divid = 0  # Counter used in the reference file for the naming of files
                paper = line[1].split(';')[0]  # Get the file_name of the paper. The metadata file sometimes has two names, hence the split
                try:  # This avoids the first line and names that I don't have files for
                    with open(mypath + paper + '.json', 'r') as json_file:
                        data = json.load(json_file) #Dictionary containing the json file
                        if data["metadata"]['title']:  # If there is a title. Might be better to extract title and abstract from metafile. Some of the JSONs seem incomplete
                            title = data['metadata']['title']
                            out_file.write(title + '\n\n')
                            out_reference.write(line[0] + '-' + str(divid) + '-title '\
                            + line[0] + ' ' + line[2] + ' ' + line[5] + ' ' + str(divid) + '\n')
                            divid += 1
                        if data['abstract']:  # "If there is an abstract"
                            for paragraph in data['abstract']: #Loop is necessary because some papers have several paragrphs in abstract
                                out_file.write(paragraph['text'] + '\n\n')
                                out_reference.write(line[0] + '-' + str(divid) + '-abstract '\
                                + line[0] + ' ' + line[2] + ' ' + line[5] + ' ' + str(divid) + '\n')
                                divid += 1
                        for sentence in data['body_text']:
                            out_file.write(sentence['text'] + '\n\n')
                            out_reference.write(line[0] + '-' + str(divid) + '-body_text '\
                            + line[0] + ' ' + line[2] + ' ' + line[5] + ' ' + str(divid) + '\n')
                            divid += 1
                except:
                    pass
