## This script will convert a collection of JSON files in Pubannotation format
# to the 'test.tsv' file necessary for classification in BioBERT.
# It will take denotation information and convert it to
# tags so that the native evaluation script of BioBERT can be used on the
# output produced by the BioBERT models.
# It will also generate a "rebuild_reference.txt" and a 'generated_text.txt' file
# These will allow for the BioBERT output file ("NER_result_conll.txt") to be converted back into a
# PubAnnotation format JSON files. (This conversion can be done by running the
# script "eval_to_pubannot.py")

import json
import sys
import re
from os import listdir

def removeall_replace(x, l):
    t = [y for y in l if y != x]
    del l[:]
    l.extend(t)
    return l

def sentence_to_tokens(text):  # Inspired by https://github.com/spyysalo/standoff2conll/blob/master/common.py
    """Return list of tokens in given sentence using NERsuite tokenization."""
    tok = [t for t in re.compile(r'([^\W_]+|.)').split(text) if t]
    tok_nospace = removeall_replace(' ', tok)
    return tok_nospace


if len(sys.argv) != 2:  # Only input should be folder containing JSON files
    print("Unexpected number of arguments: ", len(sys.argv)-1)
    print("Usage: pubannot_to_tsv.py JSON_files/")
    sys.exit(1)

path_to_jasons = sys.argv[1]
all_jsons = listdir(path_to_jasons)
## ALL TAGS:
#allowed_tags = ['Virus_SARS-CoV-2', 'Virus_family', 'Virus_other', 'Disease_COVID-19', 'Disease_other', 'Symptom', 'Symptom_COVID-19', 'Protein']
## TAGS FOR NCBI_DISEASE:
#allowed_tags = ['Disease_COVID-19', 'Disease_other', 'Disease', 'DISEASE']
## TAGS FOR JNLPBA:
allowed_tags = ['Protein', 'PROTEIN']
# TAGS FOR SYMPTOMS
#allowed_tags = ['Symptom', 'Symptom_COVID-19', 'SYMPTOM']

with open('generated_test.tsv', 'w') as out_file:
    with open('rebuild_reference.txt', 'w') as out_reference:
        with open('generated_text.txt', 'w') as out_fulltext:

            last_cord_uid = 'placeholder_text'
            paragraph_count = 0

            for file_name in all_jsons:
                with open(path_to_jasons + file_name, 'r') as in_json:
                    data = json.load(in_json)

                    #Wrtie reference file
                    cord_uid = data['cord_uid']
                    if cord_uid == ' ':
                        cord_uid = '0'
                    sourcedb = data['sourcedb']
                    sourceid = data['sourceid']

                    #TODO: this info ('divid') might need to be taken from the title, as PubAnnotation
                    # doesn't specify if a text is the title, abstract or body of the paper.
                    # Depending on the data we are given, maybe we can just copy the entire filenames!
                    # It is really hard to make a generalized version though, since the format is often inconsistent
                    if 'divid' in data.keys():
                        divid = data['divid']
                    else:
                        # Cheap workaround specific to the gold standard database
                        if cord_uid == last_cord_uid: #  If it's not the first paragraph
                            divid = 1
                        else:
                            divid = 0

                    if divid == 0:
                        out_reference.write(cord_uid + '-' + str(divid) + '-title '\
                        + cord_uid + ' ' + sourcedb + ' ' + sourceid + ' ' + str(divid) + '\n')
                    else:
                        out_reference.write(cord_uid + '-' + str(divid) + '-abstract '\
                        + cord_uid + ' ' + sourcedb + ' ' + sourceid + ' ' + str(divid) + '\n')

                    last_cord_uid = cord_uid

                    # Extracting denotation data
                    text = data['text']  # Full text of the sentence
                    split_sentence = sentence_to_tokens(text)
                    denots = data['denotations']
                    spans = []  # Will contain spans of all entities in the sentence as a tuple
                    for object in denots:  # For each of the individual denotations/objects/entities
                        if object['obj'] in allowed_tags:
                            begin = object['span']['begin']
                            end = object['span']['end']
                            spans.append((begin,end))  # Append tuple
                    spans.sort(key=lambda x: x[0])  # Reorder tuples from smallest to biggest

                    # For each file, 'entities' is a list of every denotation object
                    # multi-word objects are lists, with an element per word
                    # single-word objects are single item lists
                    entities=[]
                    for span in spans:
                        split_entity = sentence_to_tokens(text[span[0]:span[1]])
                        entities.append(split_entity)


                    #Writting the tsv file

                    #WEAK: it's not able to distinguish separate entities that are right next to one another
                    first_word = True
                    rel_stop = 0
                    position = 0

                    for word in split_sentence:
                        if entities:  # If there are entities left to consider
                            rel_start, rel_stop = re.search(re.escape(word), text[position:]).span()  # Relative span
                            start = position + rel_start  # Actual start
                            if word in entities[0] and start in range(spans[0][0],spans[0][1]):
                                if first_word:  # If it's the first word in a multi-word entity, tag is B
                                    out_file.write(word + '\t' + 'B' + '\n')
                                    first_word = False
                                else:  # If it's not the first word, tag is I
                                    out_file.write(word + '\t' + 'I' + '\n')
                                if word == entities[0][-1]:  # If the word is the last one in that span, pop!
                                    first_word = True
                                    entities.pop(0)
                                    spans.pop(0)

                            else:
                                out_file.write(word + '\t' + 'O' + '\n')
                        else:
                            out_file.write(word + '\t' + 'O' + '\n')

                        position += rel_stop
                    #Space between sentences
                    out_file.write('\n')
                    out_fulltext.write(text + '\n\n')


                paragraph_count += 1
                #if paragraph_count == 1:
                #    break
