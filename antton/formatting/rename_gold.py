#Script that will rename the gold standard files to the 'cord_uid-divid-section' information
## Usage path_to_gold_standard name_of_output_folder

import sys
import os
import json

path_to_jasons = sys.argv[1]
output_folder = sys.argv[2]
if not os.path.exists(output_folder):  # Folder where results will be stored
    os.mkdir(output_folder)
all_jsons = os.listdir(path_to_jasons)

last_cord_uid = 'placeholder_text'

for file_name in all_jsons:
    with open(path_to_jasons + file_name, 'r') as in_json:
        data = json.load(in_json)
        cord_uid = data['cord_uid']
        if cord_uid == ' ':
            cord_uid = '0'
        if 'divid' in data.keys():
            divid = data['divid']
        else:
            # Cheap workaround specific to the gold standard database
            if cord_uid == last_cord_uid: #  If it's not the first paragraph
                divid = 1
            else:
                divid = 0
        last_cord_uid = cord_uid

        if divid == 0:
            filename = cord_uid + '-' + str(divid) + '-title'
        else:
            filename = cord_uid + '-' + str(divid) + '-abstract'

        # Fuse 'Disease_COVID-19' and 'Disease_other' into just 'Disease'
        denotations = data['denotations']
        for denot in denotations:
            if denot['obj'] == 'Disease_COVID-19' or denot['obj'] == 'Disease_other' or denot['obj'] == 'Symptom':
                denot['obj'] = 'Disease'
            #print(denot['obj'])

        with open(output_folder + '/' + filename + '.json', 'w') as renamed_file:
            renamed_file.write(json.dumps(data))
