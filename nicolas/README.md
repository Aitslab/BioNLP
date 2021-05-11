## Paper
https://www.overleaf.com/read/zjkswctdqhhb
## CRAFT conversion to CoNLL
- Install boot:
```
sudo bash -c "cd /usr/local/bin && curl -fsSLo boot https://github.com/boot-clj/boot-bin/releases/download/latest/boot.sh && chmod 755 boot"
```
- Convert to CoNLL from CRAFT folder:
```
boot part-of-speech coreference convert --conll-coref-ident
```
## Using modified parser
First install neuralcoref from source with the following commands:
```
git clone https://github.com/huggingface/neuralcoref.git
cd neuralcoref
pip install -r requirements.txt
pip install -e .
```
Then replace neuralcoref/neuralcoref/train/conllparser.py with conllparser.py
Then use the following commands to prepare the data:
```
python -m neuralcoref.train.conllparser --path ./$path_to_data_directory/train/
python -m neuralcoref.train.conllparser --path ./$path_to_data_directory/test/
python -m neuralcoref.train.conllparser --path ./$path_to_data_directory/dev/
```
