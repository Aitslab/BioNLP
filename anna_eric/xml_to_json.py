#Read xml files to json dictionaries
from xml.etree import ElementTree as ET
import json
import os

path = 'pubmed2018/pubmed/'

directory = os.fsencode(path)

for file in os.listdir(directory):
    filename = os.fsdecode(file)

    if filename.endswith('.xml'):
        parser = ET.iterparse(path + filename)
        id = ''
        abbe = {}
        for event, element in parser:
            tag = element.tag
            if tag == 'PMID':
                id = element.text
            elif tag == 'AbstractText':
                abbe.setdefault(id, []).append(element.text)
            element.clear()

        with open('pubmed/json_{}.txt'.format(filename[:-4]), 'w+',encoding="utf-8", errors='ignore') as file:
            file.write(json.dumps(abbe))
        os.remove(path + filename)
