## This script will convert the gold standard dataset (and hopefully the silver
# standard too) to the 'test.tsv' file necessary for BioBERT. Using the correct
# tags so that the native evaluation script of BioBERT can be used.

import json
import re

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

with open('gold_test.tsv', 'w') as out_file:
    with open('rebuild_reference.txt', 'w') as out_reference:
        with open('gold_dataset.json', 'r') as in_json:
            data = json.load(in_json)
            cord_uid = [] # Used for the reference file
            for line in data:  # Get the text of each of the papers
                text = line['text']  # Full text of the sentence
                split_sentence = sentence_to_tokens(text)

                denots = line['denotations']
                spans = []  # Will contain spans of all entities in the sentence as a tuple
                for object in denots:  # For each of the individual denotations/objects/entities
                    begin = object['span']['begin']
                    end = object['span']['end']
                    spans.append((begin,end))  # Append tuple
                spans.sort(key=lambda x: x[0])  # Reorder tuples from smallest to biggest

                entities=[]
                for span in spans:
                    split_entity = sentence_to_tokens(text[span[0]:span[1]])
                    entities.append(split_entity)

                #Fill out the Reference file
                if cord_uid == line['cord_uid']:
                    divid += 1
                else:
                    cord_uid = line['cord_uid']
                    if cord_uid == ' ':
                        cord_uid = 'no_cord_uid'
                    divid = 1
                sourcedb = line['sourcedb']
                sourceid = line['sourceid']

                if divid == 0:
                    out_reference.write(cord_uid + '-' + str(divid) + '-title '\
                + cord_uid + ' ' + sourcedb + ' ' + sourceid + ' ' + str(divid) + '\n')
                else:
                    out_reference.write(cord_uid + '-' + str(divid) + '-abstract '\
                + cord_uid + ' ' + sourcedb + ' ' + sourceid + ' ' + str(divid) + '\n')


                #Writting the tsv file
                first_word = True
                string_index = 0
                index_in_expected_area = False
                area_error = 20
                for word in split_sentence:
                    string_index += len(word)
                    if spans and string_index in range(spans[0][0]-area_error,spans[0][1]):
                        index_in_expected_area = True
                    else:
                        index_in_expected_area = False
                    if entities and index_in_expected_area:  # If there are entities left to consider
                        if word in entities[0]:
                            if first_word:  # If it's the first word in a multi-word entity, tag is B
                                out_file.write(word + '\t' + 'B' + '\n')
                                first_word = False
                            else:  # If it's not the first word, tag is I
                                out_file.write(word + '\t' + 'I' + '\n')
                            if word == entities[0][-1]:
                                first_word = True
                                entities.pop(0)
                                spans.pop(0)
                        else:
                            out_file.write(word + '\t' + 'O' + '\n')
                    else:
                        out_file.write(word + '\t' + 'O' + '\n')
                #Space between sentences
                out_file.write('\n')
