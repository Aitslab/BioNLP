# Natural Language Processing for CovidQ project

This project was created as part of the CovidQ project with the purpose of providing proof of concept and strategy development. The overarching purpose is developing NLP models for extraction of symptoms and findings in Swedish clinical charts

CovidQ aims to develop of a clinical decision tool to determine potential/not potential cases of COVID-19 at the emergency department triage. It's a collaboration between Region Skåne, Halland, KI and Lund University.

This subproject is done as my thesis for the fifth semester of the medical program at the University of Lund. 

*Aim* : Create a testcorpus to determine the feasibility of NLP and data extraction from Swedish clinical texts. Test and develop annotation strategies and application using the software INCEpTION. Research  possibilities of extending tools for Swedish NLP and using these to pre-annotate clinical texts to reduce the annotation bottleneck.



## Project Stucture

### Swedish bioNLP

Latest version of the protocol can be found here [source](https://github.com/Aitslab/BioNLP/blob/master/carl/docs/protocol.md). 

### Subproject - OpenChartSE

Spawned as an idea during project development to create free text data that can be shared and used for future NLP work in Sweden, work to create fake medical charts from the ED is ongoing and found here: [OpenChartSE](https://github.com/tracits/OpenChartSE)

A website for input of medical records is under development. It's developed with flask. 

## Timeline

Preliminary project is planned to be presented in early june of 2021 as for a "pseduo"bachelor thesis in medicine. The overarching project will go on and this repo might be utilized more.

## Data

### testcorpus

*Will be moved to openchartSE*

#### Charts 

### Swedish bioNLP 
**Aim**: Create a small test sample to determine the feasibility of NLP and data extraction. Test and devlop annotation strategies and application using the software INCEpTION.
### OpenChartSE

These include charts created by Johanna Berg; Carl Ollvik Aasa; Anton Werin. 

#### Sentences 

Simple medical sentences describing symptoms. Written by Anton Werin; Carl Ollvik Aasa. Used for corpus generation by Sonja Aits. Grouped by if they are negating.

## Documentation

All documentation for the project.

### Annotation strategy

Developed guidelines for entity symptom annotation in clinical texts. This is developed along the project. 

Many problems arising with annotation only show as one annotates; we can se a linguistic problem or logical ambiguity but they are hard to draw actively to mind. Therefore a wiki of interesting problems, sentences and situations are keeps.  These are used to inform the guidelines. 

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

## Manuscript

Documentation for bachelor thesis of Carl Ollvik Aasa
