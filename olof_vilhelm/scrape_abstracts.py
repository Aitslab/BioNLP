import re
import os
import sys
import xml.etree.ElementTree as ET
from nltk import sent_tokenize

ABSTRACTS_SEPARATE_FILES = 0
ABSTRACTS_SINGLE_FILE = 1
ABSTRACTS_BATCHED_FILES = 2

ABSTRACT_SUFFIX = ".abstract"
ABSTRACTS_SUFFIX = ".abstracts"
SEPARATE_ABSTRACT_DIR = "_abstracts/"
BATCHED_ABSTRACT_DIR = "_batched_abstracts/"
BATCHED_PMID_SUFFIX = ".pmids"

ABSTRACTS_FILE_PMID_LINE = "#PMID="


def main(filename, mode, batch_size=-1, verbose=False):
    abstracts = get_abstracts(filename, verbose)
    file_encoding = get_encoding(filename)
    save_abstracts(abstracts, filename, file_encoding, mode, batch_size)


# Returns a dictionary of abstracts, key: PMID, value: the abstract text.
def get_abstracts(filename, verbose=False):
    abstracts = dict()
    if verbose:
        print("Parsing XML document \'" + filename + "\'...")
    root = ET.parse(filename).getroot()
    if root.tag == "PubmedArticleSet":
        if verbose:
            print("Pubmed article set detected. Gathering abstracts...")
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
                abstracts[pmid] = abstract

    else:
        print("Unknown corpus type detected. Root tag: \'" + root.tag + "\'")
        print("Exiting...")
        exit(1)
    return abstracts


# TODO Fix so it doesnt store abstracts in same folder as the corpus file
def save_abstracts(abstracts, filename, file_encoding, mode, batch_size=-1):
    filename_no_suffix = filename[:filename.rfind('.')]
    if mode == ABSTRACTS_SINGLE_FILE:
        abstracts_fn = filename_no_suffix + ABSTRACTS_SUFFIX
        with open(abstracts_fn, "w+", encoding=file_encoding) as abstracts_file:
            for pmid, abstract in abstracts:
                abstracts_file.write(ABSTRACTS_FILE_PMID_LINE + str(pmid) + "\n")
                abstracts_file.write(abstract)

        print(len(abstracts), "abstracts extracted to " + abstracts_fn + ".")

    elif mode == ABSTRACTS_SEPARATE_FILES:
        abstracts_dir = filename_no_suffix + SEPARATE_ABSTRACT_DIR
        os.makedirs(abstracts_dir, exist_ok=True)
        for pmid in abstracts:
            abstract = abstracts[pmid]
            abstract_fn = abstracts_dir + str(pmid) + ABSTRACTS_SUFFIX
            with open(abstract_fn, 'w+', encoding=file_encoding) as abstract_file:
                abstract_file.write(abstract)

        print(len(abstracts), "abstracts extracted to " + abstracts_dir + ".")

    elif mode == ABSTRACTS_BATCHED_FILES:
        abstracts_dir = filename_no_suffix + BATCHED_ABSTRACT_DIR
        os.makedirs(abstracts_dir, exist_ok=True)

        batch_nr = 0
        b_abstract_fn = abstracts_dir + "batch_" + str(batch_nr) + ABSTRACT_SUFFIX
        b_abstract_file = open(b_abstract_fn, "w+", encoding=file_encoding)
        b_pmid_fn = abstracts_dir + "batch_" + str(batch_nr) + BATCHED_PMID_SUFFIX
        b_pmid_file = open(b_pmid_fn, "w+", encoding=file_encoding)
        i = 0
        for pmid in abstracts:
            if batch_nr < int(i / batch_size):
                batch_nr = int(i / batch_size)

                b_abstract_file.close()
                b_abstract_fn = abstracts_dir + "batch_" + str(batch_nr) + ABSTRACT_SUFFIX
                b_abstract_file = open(b_abstract_fn, "w+", encoding=file_encoding)

                b_pmid_file.close()
                b_pmid_fn = abstracts_dir + "batch_" + str(batch_nr) + BATCHED_PMID_SUFFIX
                b_pmid_file = open(b_pmid_fn, "w+", encoding=file_encoding)

            abstract = abstracts[pmid]
            b_abstract_file.write(ABSTRACTS_FILE_PMID_LINE + str(pmid) + "\n")
            b_abstract_file.write(abstract)
            b_pmid_file.write(pmid + "\n")
            i += 1

        b_abstract_file.close()
        b_pmid_file.close()
        print(len(abstracts), "abstracts extracted to " + abstracts_dir + " in", batch_nr, "batches of " + str(batch_size) + ".")


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


def print_help():
    print("Usage: python", sys.argv[0], "[OPTIONS] [FILE]\n")
    print("[FILE]      : An XML file containing abstracts.")
    print("Options:")
    print("  -s        : (Default) Puts abstracts into a single file named [FILE].abstracts.")
    print("  -v        : Provides extra output to display progress.")
    print("  -S        : Put abstracts into individual files named [PMID].abstract in ./[FILE]_abstracts/")
    print("  -b [N]    : Put batches of [N] abstracts into files.")
    exit()


def handle_options(args):
    filename = None
    mode = ABSTRACTS_SINGLE_FILE
    batch_size = -1
    verbose = False
    if len(args) <= 1:
        print_help()
    elif len(args) <= 2:
        filename = args[1]
    elif len(args) <= 3:
        if "h" in args[1]:
            print_help()
        if "v" in args[1]:
            verbose = True
        if "s" in args[1]:
            mode = ABSTRACTS_SINGLE_FILE
        if "S" in args[1]:
            mode = ABSTRACTS_SEPARATE_FILES
        if "b" in args[1]:
            print("-b detected wrong")
            try:
                _ = int(args[2])
                print("Filename missing.")
                exit(1)
            except ValueError:
                print("Missing batch size.")
                exit(1)
        filename = args[2]
    elif len(args) <= 4 and "b" in args[1]:
        print("-b detected")
        mode = ABSTRACTS_BATCHED_FILES
        try:
            batch_size = int(sys.argv[2])
            filename = sys.argv[3]
        except ValueError:
            print("Batch size not correctly specified.")
            exit(1)

    try:
        f = open(filename, 'r')
        f.close()
        return filename, mode, batch_size, verbose
    except FileNotFoundError:
        print("File \'" + filename + "\' not found. Exiting...")
        exit(1)


if __name__ == '__main__':
    fn, m, nb, v = handle_options(sys.argv)
    main(fn, m, nb, v)
