import pathlib, os

parentpath = str(pathlib.Path(__file__).parent.absolute())
gold_papers_path = parentpath + "/gold_papers"

filenames = []
for f in os.listdir(gold_papers_path):
    print(f[:-5])
    filenames.append(f[:-5])

out = open("meta_gold.csv","w+")

for line in open("metadata.csv", "r"):
    for f in filenames:
        if(f in line):
            print(f)
            out.write(line)
