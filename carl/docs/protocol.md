---
title: Implementing a multicentre data bank for trauma surveillance and research
subtitle: Institutional review board application
---

## Supervisors

Johanna Berg, johanna@tech.se

Sonja Aits, sonja.aits@med.lu.se


# Background

En enorm mängd data för symtombilder och olika medicinska tillstånd och processer finns redan, men är skriven som fritext i journaler. Denna data har för praktiskt syfte varit otillgänglig för bredare forskning, men i med utvecklingen av olika artificiell intelligens och språkmodeller som gör det möjligt att med datorer att läsa och strukturera fritext börjar modeller för att hantera patientjournaler att bli möjliga att skapa.

Deep learning modeller av neurala nätverk för NLP (Natural language processing) har använts för allt från digitala assistenter, automatisk summering, chatbots och text-generering. En sådan modell tränad för medicinsk språk skulle kunna användas för att läsa och strukturera den data som finns i journaltexter med specifika mål.

# Methods

## Design

Methos testing

## Setting

Emergency room triage

## Data
kommer sedan att testas på den annoterade delen av corpusen. Sedan kommer ett svenskt dictionary med symtom för covid-19 från ICD-10 koder och Snomed-CT att sammanställas. Detta kommer sedan att användas för att träna en svensk BERT (Kungliga Biblioteket) för symtom NER. Detta avslutar T5 arbetet, men projektet ämnar om det funkar sedan att gå vidare med att läsa och strukturera data från 100 000 akutmottagningsbesök under coronapandemin. Denna data i strukturerat format ämnas användas för att koppla ihop symptombild med positivt eller negativt test för covid-19 och ge en prediktiv sannolikhetsuppskattning för att en viss symptombild är kopplad till covid-19 positivitet.

## Design
Data bank implementation.