#Process protein names and cell death names using docria and print docria to file

import json
import re
import time
from docria import Document, MsgpackCodec, DocumentIO, set_large_screen, T
import os.path
from docria.algorithm import group_by_span, dominant_right_span, dominant_right
from docria.printout import options
from docria.storage import DocumentIO
from nltk.corpus import stopwords


set_large_screen()

def connect_jvm(port):
    from py4j.java_gateway import GatewayParameters, JavaGateway
    gateway_parameters=GatewayParameters(port=port, auto_convert=True, auto_field=True)
    gateway = JavaGateway(gateway_parameters=gateway_parameters)
    app = gateway.entry_point
    return gateway, gateway.jvm, app

def get_java_file(jvm, path):
        return jvm.java.io.File(os.path.abspath(path))

def setup_java(p, c):
    gateway, jvm, app = connect_jvm(6006)
    app.buildIndex(get_java_file(jvm, "{}.txt".format(p)), get_java_file(jvm, "{}.fst".format(p)))
    app.buildIndex(get_java_file(jvm, "{}.txt".format(c)), get_java_file(jvm, "{}.fst".format(c)))

    indx = app.loadIndex(get_java_file(jvm, "{}.fst".format(p)))
    indx2 = app.loadIndex(get_java_file(jvm, "{}.fst".format(c)))

    return (app, indx, indx2)

# Create a document and tag it
def create_doc(id, text, app, i, i2):
    doc = Document()
    doc.add_text("main", text)
    doc.props["id"] = id
    binary_doc = MsgpackCodec.encode(doc)
    search_binary_doc = app.search(i, i2, binary_doc)
    doc = MsgpackCodec.decode(search_binary_doc)
    return doc

def filter_away_nodes(d, stop_w):
    rm_nodes = []
    for node in d['protmatches']:
        #If node is a stopword or number or length less than 2
        if len(str(node["text"])) < 2 or re.match( "^[0-9-]+$", str(node["text"])) or str(node["text"]) in stop_w:
            rm_nodes.append(node)
    [n.detach() for n in rm_nodes]
    return d

#Taggs the abstracts in abstracts_genetag
def file_tagger(app, indx, indx2, stop_w):
    # Add the abstracts[key = PMID] = Abstract Text
    abstracts = {}
    with open('genetag/abstracts_genetag.txt', 'r',encoding="utf-8", errors='ignore') as file:
        abstracts = json.loads(file.read())

    # One doc for each abstract
    out = []; dr = []
    for key in abstracts:
        dr.append(create_doc(key, abstracts[key], app, indx, indx2))
    for d in dr:
        d = filter_away_nodes(d, stop_w)

    # Print one file per 50 000 abstracts
    i = 0; j = 0
    while i < len(dr):
        with DocumentIO.write('pubmed/pubmed1905({}).docria'.format(str(j))) as dw:
            while i < len(dr) and i < 50000:
                dw.write(dr[i])
                i += 1
        j += 1
    return len(dr)


# Tags a given string, s, and prints matches and returns new string, s_out
def text_tagger(s, app, indx, indx2):

    doc = filter_away_nodes(create_doc('id', s, app, indx, indx2))

    tuls = []
    for term in doc["protmatches"]:
        tuls.append((term["text"].start, term["text"].stop, str(term["text"])))

    tuls2 = []
    for term in doc["lysomatches"]:
        tuls2.append((term["text"].start, term["text"].stop, str(term["text"])))

    i = 0; s_out = ''

    for d in tuls:
        print('------------------\nMATCH, PROT:\n{}\n------------------'.format(d[2]))
        i_s = d[0]
        i_e = d[1]
        s_out += s[i:i_s] + "\033[43m{}\033[m".format(s[i_s:i_e])
        i = i_e

    s_out += s[i:]

    for d in tuls2:
        print('------------------\nMATCH, LYSO:\n{}\n------------------'.format(d[2]))
        s_out = re.sub(d[2], "\033[45m{}\033[m".format(d[2]), s_out, flags = re.IGNORECASE)
    return s_out

#A tagger which prints to genetag in eval format
def score_tagger(c):
    p = 'protein_name/protein_names_uniprot(2)'

    (app, indx, indx2) = setup_java(p, c)

    # Read dictionary with genetag abstracts
    with open('genetag/abstracts_genetag.txt', 'r',encoding="utf-8", errors='ignore') as file:
        d = json.loads(file.read())

    # Write to genetag
    out = []

    for key in d:
        doc = filter_away_nodes(create_doc(key, d[key], app, indx, indx2))
        tuls = []

        for term in doc["protmatches"]:
            tuls.append((term["text"].start, term["text"].stop, str(term["text"])))

        for m in tuls:
            out.append('|'.join([key, str(m[0]) + ' ' + str(m[1]), m[2]]))

    with open('genetag/genetag_all.out', 'w+', encoding="utf-8", errors='ignore') as file:
        file.write('\n'.join(out))

    return len(d)

p = 'protein_name/protein_names_uniprot(2)'
c = 'cell_death_names'

stop_w = set()
[stop_w.add(t) for t in stopwords.words('english')]

(app, indx, indx2) = setup_java(p, c)

#file_tagger = 'file', text_tagger = 'text',  score_tagger = 'score'
run = 'file'

if run == 'file':
    start = time.time()
    l = file_tagger(app, indx, indx2, stop_w)
    end = time.time()
    print('total time: {} s\nnbr of abstracts: {}\ntime per abstract: {} s'.format(str(end-start), l, str((end-start)/l)))

elif run == 'text':
    #text = 'Improvement of nursing instruction to be given at the time of discharge from the ward for premature infants'
    text = "the apoptosis the. The constraints of Cr10HGO, 110 kDa antigen, and the effects of additional proteins on oligoribonucleotide synthesis by the 63-kDa gene 4 protein have been examined using templates of defined sequence. cell death is caused by cells dying."
    s = text_tagger(text, app, indx, indx2)
    matches = "{} \n\n\033[43m{}\033[m\n\033[45m{}\033[m".format(s, 'PROTEIN', 'CELL DEATH')
    print(matches)

elif run == 'score':
    start = time.time()
    l = score_tagger(c)
    end = time.time()
    print('total time: {} s\ntime per abstract: {} s'.format(str(end-start), str((end-start)/l)))
