## Second version of the 'eval_to_pubannot.py' script. Intended to fix the issues
# of the previous one.
## USAGE: script.py generated_text.txt NER_result_conll.txt rebuild_reference.txt folder_name obj_name


import os
import re
import json
import sys

if len(sys.argv) != 6:  # Check correct numeber of inputs
    print("Unexpected number of arguments: ", len(sys.argv)-1)
    print("USAGE: script.py generated_text.txt NER_result_conll.txt rebuild_reference.txt folder_name obj_name")
    sys.exit(1)

def relative_to_real(current_pos, strt, stp):
    real_start = current_pos + strt
    real_stop = current_pos + stp
    return real_start, real_stop

def fuse_multiword_entities(denotations):
    # If two entities are multy-word, join them
    denotations.append(['dirty buffer', 0, 0, 0])  # Dirty trick to avoid index out of range
    if len(denotations) > 1:  # If there is more than a single entity
        i = 0
        while i < len(denotations)-1:
            if denotations[i+1][3] == 'I-MISC':
                if denotations[i][2] == denotations[i+1][1]:
                    denotations[i][0] =  denotations[i][0] + denotations[i+1][0]  # Token
                    denotations[i][2] = denotations[i+1][2]  # Span
                else:
                    denotations[i][0] =  denotations[i][0] + ' ' + denotations[i+1][0]  # Token
                    denotations[i][2] = denotations[i+1][2]  # Span
                denotations.pop(i+1)
                i -= 1

            i += 1
    denotations.pop(-1)  # Remove buffer

    return denotations


def build_denot_array(denots):
    d_array = []
    denot_id_counter = 0
    for denotation in denots:  # Each 'denotation' is <token> <start> <stop>
        d_array.append({"id": 'A-biobert_T' + str(denot_id_counter),\
        "span": {"begin": denotation[1], "end": denotation[2]}, "obj": sys.argv[5]})
        denot_id_counter += 1
    return d_array

def write_json_file(full_text, metadata, denotations_raw):
    denot_array = build_denot_array(denotations_raw)

    file_name = metadata[0]
    with open(sys.argv[4] + '/' + file_name + '.json', 'w') as out_file:
        tmp_dict = {
            "cord_uid": metadata[1], # first 4 can be found in 'lines' !
            "sourcedb": metadata[2],
            "sourceid": metadata[3],
            "divid": metadata[4],
            "text": full_text, #Add full text
            "project": "cdlai_CORD-19", # A fixed expression defined by us
            "denotations": denot_array  # Add all entities
            }
        out_file.write(json.dumps(tmp_dict))

## Main:
generated_text = sys.argv[1]
NER_result_conll = sys.argv[2] #'../NCBI_Disease_results/NER_result_conll.txt'
f = open(sys.argv[3], 'r') #'../dataset_generation/rebuild_reference.txt', 'r')
metadata_lines = f.readlines()  # Open the reference file, which contains the names of the output filenames
    # This is necessary because the BioBERT output file has no info of ID or text type (title, abstract...)
if not os.path.exists(sys.argv[4]):  # Folder where results will be stored
    os.mkdir(sys.argv[4])

with open(generated_text, 'r') as full_text:
    with open(NER_result_conll, 'r') as ner_results:
        paragraph_number = 0
        for paragraph in full_text:  # For each paragraph
            if not paragraph =='\n':
                position = 0
                paragraph_denotations = []
                for line in ner_results:  # For each word/token in that paragraph
                    if line == '\n': # If end of paragraph, stop, go to next paragraph
                        break
                    token = re.findall(r'^([\S]+)',line)[0]  # word of this line
                    tag = line[-7:-1]  # tag that corresponds to the word/token
                    try:
                        rel_start, rel_stop = re.search(re.escape(token), paragraph[position:]).span()  # Relative span in paragraph
                    # From 'position' instead of from origin, so that we make sure it's the closest match
                    except:
                        rel_stop = 0
                        #position += 1
                        #pass
                    if tag == 'B-MISC' or tag == 'I-MISC':
                        start, stop = relative_to_real(position, rel_start, rel_stop)
                        paragraph_denotations.append([token, start, stop, tag])

                    position = position + rel_stop
                paragraph_denotations = fuse_multiword_entities(paragraph_denotations)
                paragraph_metadata = metadata_lines[paragraph_number].split()  # [File name, cord_uid, source_x, pmcid, divid]

                write_json_file(paragraph, paragraph_metadata, paragraph_denotations)

                paragraph_number += 1
                #if paragraph_number == 4000: # Counter for testing purposes. DELETE LATER
                #    break # Counter for testing purposes. DELETE LATER
