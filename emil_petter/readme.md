This is the repository for a student project at LU in Fall term 2019

Folders and content
=======

# databaseraw

contains raw data from bioinformatics databases; subfolders named Databasename_downloaddate

# databaseprocessed

contains cleaned files named Databasename_downloaddate_processeddate and a database_summary file describing the databases and extracted information

# dictionaries

contains joint dictionaries made from files in databaseprocessed

Format of proteins/genes dictionary

column 1: self-created unique identifier: LUGEspeciesidentifierrandomnumber (speciesidentifer = 8 digits (from NCBI taxonomy database), all 0 if species not defined; randomnumber = 8 digits, start with 00000001)

column 2: UniProtId

column 3-x: names


Format of compound dictionary

column 1: self-created unique identifier: LUCOrandomnumber (16 digits)

column 2-x: names


Format of disease dictionary:

column 1: self-created unique identifier: LUDIrandomnumber (16 digits)

column 2-x: names


