echo "Combining cell lines..."
cat $(echo HUNER_NER_DATASETS_MINIMAL/huner_cell_line*/*_train.conll | tr ' ' '\n' | sort | tr '\n' ' ') | python converter.py > combined/HunFlair_NER_cell_lines/train.tsv
cat $(echo HUNER_NER_DATASETS_MINIMAL/huner_cell_line*/*_dev.conll | tr ' ' '\n' | sort | tr '\n' ' ') | python converter.py > combined/HunFlair_NER_cell_lines/devel.tsv
cat $(echo HUNER_NER_DATASETS_MINIMAL/huner_cell_line*/*_test.conll | tr ' ' '\n' | sort | tr '\n' ' ') | python converter.py > combined/HunFlair_NER_cell_lines/test.tsv
cat combined/HunFlair_NER_cell_lines/train.tsv combined/HunFlair_NER_cell_lines/devel.tsv > combined/HunFlair_NER_cell_lines/train_dev.tsv

echo "Combining chemicals..."
cat $(echo HUNER_NER_DATASETS_MINIMAL/huner_chemical*/*train.conll | tr ' ' '\n' | sort | tr '\n' ' ') | python converter.py > combined/HunFlair_NER_chemical/train.tsv
cat $(echo HUNER_NER_DATASETS_MINIMAL/huner_chemical*/*dev.conll | tr ' ' '\n' | sort | tr '\n' ' ') | python converter.py > combined/HunFlair_NER_chemical/devel.tsv
cat $(echo HUNER_NER_DATASETS_MINIMAL/huner_chemical*/*test.conll | tr ' ' '\n' | sort | tr '\n' ' ') | python converter.py > combined/HunFlair_NER_chemical/test.tsv
cat combined/HunFlair_NER_chemical/train.tsv combined/HunFlair_NER_chemical/devel.tsv > combined/HunFlair_NER_chemical/train_dev.tsv

echo "Combining disease..."
cat $(echo HUNER_NER_DATASETS_MINIMAL/huner_disease*/*train.conll | tr ' ' '\n' | sort | tr '\n' ' ') | python converter.py > combined/HunFlair_NER_disease/train.tsv
cat $(echo HUNER_NER_DATASETS_MINIMAL/huner_disease*/*dev.conll | tr ' ' '\n' | sort | tr '\n' ' ') | python converter.py > combined/HunFlair_NER_disease/devel.tsv
cat $(echo HUNER_NER_DATASETS_MINIMAL/huner_disease*/*test.conll | tr ' ' '\n' | sort | tr '\n' ' ') | python converter.py > combined/HunFlair_NER_disease/test.tsv
cat combined/HunFlair_NER_disease/train.tsv combined/HunFlair_NER_disease/devel.tsv > combined/HunFlair_NER_disease/train_dev.tsv

echo "Combining gene..."
cat $(echo HUNER_NER_DATASETS_MINIMAL/huner_gene*/*train.conll | tr ' ' '\n' | sort | tr '\n' ' ') | python converter.py > combined/HunFlair_NER_gene/train.tsv
cat $(echo HUNER_NER_DATASETS_MINIMAL/huner_gene*/*dev.conll | tr ' ' '\n' | sort | tr '\n' ' ') | python converter.py > combined/HunFlair_NER_gene/devel.tsv
cat $(echo HUNER_NER_DATASETS_MINIMAL/huner_gene*/*test.conll | tr ' ' '\n' | sort | tr '\n' ' ') | python converter.py > combined/HunFlair_NER_gene/test.tsv
cat combined/HunFlair_NER_gene/train.tsv combined/HunFlair_NER_gene/devel.tsv > combined/HunFlair_NER_gene/train_dev.tsv

echo "Combining species..."
cat $(echo HUNER_NER_DATASETS_MINIMAL/huner_species*/*train.conll | tr ' ' '\n' | sort | tr '\n' ' ') | python converter.py > combined/HunFlair_NER_species/train.tsv
cat $(echo HUNER_NER_DATASETS_MINIMAL/huner_species*/*dev.conll | tr ' ' '\n' | sort | tr '\n' ' ') | python converter.py > combined/HunFlair_NER_species/devel.tsv
cat $(echo HUNER_NER_DATASETS_MINIMAL/huner_species*/*test.conll | tr ' ' '\n' | sort | tr '\n' ' ') | python converter.py > combined/HunFlair_NER_species/test.tsv
cat combined/HunFlair_NER_species/train.tsv combined/HunFlair_NER_species/devel.tsv > combined/HunFlair_NER_species/train_dev.tsv