import regex as re

lineformat = re.compile(r"(.+) ([BIO])(?:\-([A-Za-z]+))? [\+\-]")
import sys

if __name__ == '__main__':
    nline = 0
    for line in sys.stdin: 
        if line.strip() == '':
            if nline == 0:
                print("")
            nline += 1
        else:
            nline = 0
            m = lineformat.match(line)
            if m is None:
                sys.stderr.write("Line '%s' failed to match" % line)
            else:
                print("{}\t{}".format(m[1], m[2]))
    