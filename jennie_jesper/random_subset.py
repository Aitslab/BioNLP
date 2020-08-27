import os, random, shutil

comm_use_subset_100 = random.sample(os.listdir("/Users/jesperlaurell/EDAN70/comm_use_subset"), 100)

for filename in comm_use_subset_100:
    shutil.copy("/Users/jesperlaurell/EDAN70/comm_use_subset/" + filename, '/Users/jesperlaurell/EDAN70/comm_use_subset_100')

