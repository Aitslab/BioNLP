import re
import os
import sys
import xml.etree.ElementTree as ET
from nltk import sent_tokenize

SEPARATE_ABSTRACTS = False
ABSTRACT_SUFFIX = ".abstract"
ABSTRACT_DIR = "abstracts/"
ABSTRACTS_FILE_PMID_LINE = "#PMID="
ABSTRACTS_SUFFIX = ".abstracts"

def main(args):
    filename = handle_options(args)
    file_encoding = get_encoding(filename)
    print("\'" + filename + "\' uses " + file_encoding + " encoding.")
    abstracts_file = open(filename.split(".")[0] + ABSTRACTS_SUFFIX, "w+", encoding=file_encoding)
    os.makedirs(ABSTRACT_DIR, exist_ok=True)

    nr_abstracts = 0
    print("Parsing XML document \'" + filename + "\'...")
    root = ET.parse(filename).getroot()
    if root.tag == "PubmedArticleSet":
        print("Pubmed article set detected.")
        for article in root:
            pmid = None
            abstract = ""
            for el in article.iter("PMID"):
                if el.tag == "PMID":
                    pmid = el.text
                    continue

            for el in article.iter("AbstractText"):
                if el.text is not None:
                    abstract += el.text

            if abstract != "" and pmid is not None:
                nr_abstracts += 1
                normalized_abstract = normalize_text(abstract)
                if SEPARATE_ABSTRACTS:
                    abstract_fn = ABSTRACT_DIR + str(pmid) + ABSTRACT_SUFFIX
                    with open(abstract_fn, 'w+', encoding=file_encoding) as f:
                        f.write(normalized_abstract)
                else:
                    abstracts_file.write(ABSTRACTS_FILE_PMID_LINE + str(pmid) + "\n")
                    abstracts_file.write(normalized_abstract)

    else:
        print("Unknown corpus type detected. Root tag: \'" + root.tag + "\'")

    abstracts_file.close()
    if SEPARATE_ABSTRACTS:
        print(nr_abstracts, "abstracts extracted to " + ABSTRACT_DIR + ".")
    else:
        print(nr_abstracts, "abstracts extracted to " + filename.split(".")[0] + ABSTRACTS_SUFFIX + ".")

def normalize_text(text):
    sentences = sent_tokenize(text, language="english")
    line_sep_text = ""
    for s in sentences:
        line_sep_text += s + "\n"
    return line_sep_text


def get_encoding(filename):
    encoding_found = False
    with open(filename, "r", buffering=5) as f:
        while not encoding_found:
            line = f.readline()
            result = re.search("encoding=\"(.*)\"", line)
            return result.group(1)



def help():
    print("Usage: python", sys.argv[0], "[OPTIONS] [FILE]\n")
    print("Options:")
    print("  -s        : (Default) Puts abstracts into a single file named [FILE].abstracts.")
    print("  -S        : Put abstracts into individual files named [PMID].abstract in ./[FILE]_abstracts/")
    print("  -b [N]    : Put batches of [N] abstracts into files. NOT IMPLEMENTED YET.")
    exit()


def handle_options(args):
    global SEPARATE_ABSTRACTS
    filename = None
    if len(args) <= 1:
        help()
    elif len(args) <= 2:
        filename = args[1]
    elif len(args) <= 3:
        if "h" in args[1]:
            help()
        if "s" in args[1]:
            SEPARATE_ABSTRACTS = False
        if "S" in args[1]:
            SEPARATE_ABSTRACTS = True
        if "b" in args[1]:
            print("Batching abstracts is not yet implemented.")
            exit()
        filename = args[2]
    elif len(args) <= 4 and "b" in args[1]:
        print("Batching abstracts is not yet implemented.")
        exit()

    try:
        f = open(filename, 'r')
        f.close()
        return filename
    except FileNotFoundError:
        print("File \'" + filename + "\' not found. Exiting...")
        exit(1)


def __main():
    main(sys.argv)


__main()



