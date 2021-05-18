# Natural Language Processing for CovidQ project

This project was created as part of the CovidQ project with the purpose of providing proof of concept and strategy development. The main purpouse is developing extraction of symptoms and findings from Swedish clinical charts using a BioBERT model.

CovidQ aims to develop of a clinical decision tool to determine potential/not potential cases of COVID-19 at the emergency department triage. It's a collaboration between Region Skåne, Halland, KI and Lund University.

*The project is done as part of semester five of the medical program at the University of Lund*

## Project Stucture

Lates version of the protocol can be found here [source](https://github.com/Aitslab/BioNLP/blob/master/carl/docs/protocol.md)

### Swedish bioNLP 
**Aim**: Create a small test sample to determine the feasibility of NLP and data extraction. Test and devlop annotation strategies and application using the software INCEpTION.
### OpenChartSE

Spawned as an idea during project development to create free text data that can be shared and used for future NLP work in Sweden, work to create fake medical charts from the ED is ongoing and found here: [OpenChartSE](https://github.com/tracits/OpenChartSE)

## Timeline

Preliminary project is planned to be presented in early june of 2021 as for a "pseduo"bachelor degree in medicine. The overarching project will go on and this repo might be utilised more.

### Data

### testcorpus

*Will be moved to openchartSE*

Fabricated charts of typical patients that receive care in the emergency room for testing and development of NLP algorithms.
### Annotationstrategy

Developed guidlines for entity symptom annotation in clinical texts

Devloped on the base of 
### INCEpTION

Documentation and configuration for the usage of the annotation software INCEpTION with the purpouse of NER-annotation of clinical texts

* [INCEpTION_project_guide:](INCEpTION_project_guide) Documentation on security, backup and continuity plan and best practices.

* [INCEpTION_workflow_structure:](INCEpTION_workflow_structure) Defined workflow and steps for project continuity and clear comparison and testing.

* [INCEpTION-project Source Repo](https://inception-project.github.io/)

* Main version of INCEpTION used: 0.17.2

### Testcorpus

Fabricated charts of typical patients that receive care in the emergency room for testing and development of NLP algorithms.



## Documentation

Issues in this project is used for tasks and to-dos.

All documents are in `docs`.

Generic variable list is found [here](https://docs.google.com/spreadsheets/d/1IFDix9-LtwO1iKycumoEDqi2fSPaKNY9p7EyEFV3Qr8/edit#gid=1908521054). (Swedish)