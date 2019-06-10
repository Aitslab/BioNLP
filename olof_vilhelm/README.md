# Detecting relationships (A inhibits B)

Jupyter worklog in `Log.ipynb`.

`spacynlp.py` contains the main algorithm for predicting relations. It uses `gui.py` and `entity_relations_model.py` to show the results in a GUI. 
During previous iterations of the algorithm we analyzed sentences scrape from BioInfer using `read_bioinfer.py` and abstracts scraped from PubMed using `scrape_abstracts.py`.

Now in the last (2019-06-10) iteration it uses abstracts from PubMed, but in a docria file with protein/gene/lysosome/cell-death term matches added onto it by Anna Palmqvist Sjövall & Eric Holmström. It generates an output file intended for use by Hannes Berntsson.

There is also a slightly modified version of `spacynlp.py` called `final_test_predict_bioinfer.py`, which was used to generate test data, i.e. the results in `test_results/final_test_results.txt`.
It's been modified to read the binarized BioInfer corpus, and also bypasses the matching for protein/gene/lysosome/cell-death terms from Anna & Eric. This allowed us to evaluate the performance of our algorithm independently.

## Dependencies

- [nltk](https://www.ntlk.org)
- [spacy](https://spacy.io)
- [neuralcoref](https://github.com/huggingface/neuralcoref)
- [docria](https://pypi.org/project/docria)
