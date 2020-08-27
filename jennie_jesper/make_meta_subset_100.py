import pathlib, os

parentpath = str(pathlib.Path(__file__).parent.absolute())
comm_use_subset_100 = parentpath + "/comm_use_subset_100"

filenames = []
for f in os.listdir(comm_use_subset_100):
    print(f[:-5])
    filenames.append(f[:-5])

out = open("meta_subset_100.csv","w+")

for line in open("metadata.csv", "r"):
    for f in filenames:
        if(f in line):
            print(f)
            out.write(line)
