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