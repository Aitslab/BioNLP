Evaluation code and corpora are in this main folder as they will be shared. Taggers, files containing the metric tables and output files are in the folder for each group.

The first prototype of each tagger is named version 1, and it is named typeoftagger_taggername_group_version e.g. NER_dictionary+rule_AnniSofi_1, NER_dictionary_JennieJesper_v1 or NER_biobert-jnlpba_Antton_1. Any new improvement of the tagger that is evaluated will get a new version number. Each group has a table containing the evaulations with one row for each evaluation round you have done and the following columns:
Column 1: corpus used for evaluation, e.g. aitslab_corona_gold, aitslab_corona_silver, biobert_jnlpba
Column 2: name of tagger, e.g. NER_dictionary_AnniSofi_1
Column 3: name of output files, or if several files, name of output folder (subfolder in your main group folder)
Column 4: annotated classes, e.g. disease_covid19, virus_sarscov2
Column 5: precision per class
Column 6: recall per class
Column 7: precision for all classes combined
Column 8: recall for all classes combined
Column 9: runtime
