# Script that will fuse two BioBERT .tsv files into obj_name

import sys

first_file_name = sys.argv[1]
second_file_name = sys.argv[2]

with open('fused_train_dev.tsv', 'w') as out_file:
    with open(first_file_name, 'r') as first_tsv:
        for line in first_tsv:
            out_file.write(line)

    with open(second_file_name, 'r') as second_tsv:
        for line in second_tsv:
            out_file.write(line)
