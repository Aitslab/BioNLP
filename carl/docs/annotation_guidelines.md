# Guidelines for annotation

Annotation of medical text do usually come with the requirement of some expertise, and they are intended to be used primarily by clinicians with experience in reading and writing patient records.

Some explanations may therefore seem arcane when it comes to medical issues as they are keep short for brevity assuming medical knowledge.

Patient records are highly structured with headings such as Subjective, Objective, Assessment and Plan, but this is not always followed by individual physicians, or between different professions. The writing under the correct heading and also the names of the headings may differ in different clinical units or hospitals. The same for different electronic patient record systems. The patient records are written under time pressure; the patient record systems do not contain any spelling correction (or grammar checking) system due to the difficulties of building such a function because of the complicated non-standard vocabulary used within healthcare (Dalianis 2018)



*These guidelines are to a large part based on *

#### Abbreviations

NE = Named Entity; Pat. = Patient

## Main principles

#### Continuity

- All instances of a NE which has the same function shall be labeled in the same manner across the corpus
  - E.g. negations should be categorized as such not only at symptoms but across the document.

#### Named Entities used

- Words and expressions that are NE are to be marked as belonging to one of the following. These have been describes as classes such as in OOP

  - *Symptom*: Subjective experience by the patient

  - *Signs*: A sign may be observed by another than the pat. or may be detected during anamnesis or medical examination. They are to some degree objective indications of a disease, injury, or abnormal physiological state.

    - In Swedish: classically written under the heading of "akutellt"

    symptom;*fynd som skulle kunna göras på akuten genom undersökning och anamnestagning. Klassiskt det som skulle skrivs

  - Finding: Observation

### Negated symptoms

The lack of a symptom is not a symptom

## Named Entities used in project

* SYM
* NEG



under akutellt vid journalföring ; *avsaknad av symptom är ej symptom*

NEG;*negation;*negerande enskilda ord såsom inte och ej + förled så som o i t.ex.

### Example useage & common problems

*Status: AT: opåverkat i vila*
"påverkad i vila" = SYM
"o" = NEG

Here transforming all "opåverkad" to "ej påverkad" helps with automatically tagging the negations usings string matchers.

## Annotation problems

: definition