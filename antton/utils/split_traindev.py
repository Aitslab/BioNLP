# This script will generate 'train.tsv' and 'devel.tsv' files from a 'train_dev.tsv' file
# The file is split in two at the defined cutoff point

## Usage: python train_dev.tsv number_of_Bs cutoff_percent 
import sys
import re

train_dev_dir = sys.argv[1]
total_Bs = sys.argv[2]
cutoff_percent = sys.argv[3]

cutoff = int(total_Bs)*int(cutoff_percent)/100
B_count = 0
cutoff_reached = False
with open(train_dev_dir, 'r') as train_dev:
  with open('train.tsv', 'w') as train:
    with open('devel.tsv', 'w') as devel:

        line_count = 0
        for line in train_dev:
            line_count += 1
        #Before cutoff is reached, write lines to 'train'. After cutoff, in 'devel' instead
            if re.search('\tB', line): # Keep track of amount of Bs passed.
                B_count += 1
            if B_count > cutoff and line == '\n':
                cutoff_reached = True

            if cutoff_reached:
                devel.write(line)
            else:
                train.write(line)
            #if line_count >= 20:
            #    break
