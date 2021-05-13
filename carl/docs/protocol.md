# PROTOCOL

Version 0.0.1
Author: Carl Ollvik Aasa

Supervisors: Sonja Aits, sonja.aits@med.lu.se; Johanna Berg, johanna@tech.se

## Background
BERT AND/OR Dictionary (we don't know which is best for medical journals, union or intersection



En enorm mängd data för symtombilder och olika medicinska tillstånd och processer finns i medicinsk dokumentation, men är skriven som fritext i journaler. Deep learning modeller av neurala nätverk för NLP (Natural language processing) har använts för allt från digitala assistenter, automatisk summering, chatbots och text-generering. En sådan modell tränad för medicinsk språk skulle ha potential att kunna hantera och strukturera den data som finns i journaltexter med specifika mål.

I den rådande covid-19 krisen behöver myndigheter och forskare utveckla behandlingar och smittskyddsstrategier i snabbast mån möjligt, men välgrundade beslut kräver genomgångar av ett växande berg information. För närvarande finns över 130,000 vetenskapliga artiklar om COVID19(1) och utöver det finns en enorm mängd av data i form av journaltexter, vilket i kombination med att denna data är fragmenterad och ostrukturerad i praktiken gör den omöjlig för människor att utnyttja till fullo. 

Ett viktigt steg i biomedicinsk natural language processing (BioNLP) är att identifiera relevanta nyckelfraser och -ord, samt deras synonymer, så kallad named entity recognition (NER). I fall som covid-pandemin är detta speciellt svårt då det inte fanns ett officiellt namn i början. Sedan kan man även leta efter kopplingar mellan nyckelfraserna, så kallad named entity linking (NEL). En del arbete för NER och NEL har redan gjorts på medicinsk engelska, men de nya teknologiska utvecklingarna har inte överförts för medicinsk svenska än. Detta begränsar möjligheten för att använda teknologin i Sverige.(2)

Målet med detta projekt är utveckla och utvärdera en verktygslåda för natural language processing för svenskt mediciniskt språk och anpassa den för att extrahera information relaterad till COVID19.

## Frågeställningar

Vilka existerande datakällor kan användas för att träna NLP modeller för svenska medicinska texter? Kan NLP verktyg som är utvecklad för engelska texter anpassas till svensk medicinsk text? Hur bra fungerar dessa NLP verktyg i upptag av COVID19 symptomdata från fritext i jämförelse med manuell läsning (gold standard)? Vilka typer av symptom nämns i journaltexter av COVID19 patienter?
## Methods

### Data Collection

#### Corpus

Insamling av stora mänger medicinska texter på svenska behövs för att träna en grundläggande språkmodell. Själva innehållet är mindre relevant så länge det kommer från medicinska områden eller närliggande teman. Inklusionskriterier är därför bara om texterna är på svenska, är tillgängliga och om dem kan utan större problem omvandlas till en maskinläsbart format. Olika källor kommer att utvärderas och om de uppfyller kriterierna kommer texterna att samlas in och formaterats till en standardiserad format: SVT hemsida, existerande samlingar i språkbanken(3), wikipedia samt journaltexter från akutvårdspatienter vid Skånes Universitetssjukhus under 2020, med mera.

#### Sources

#### Data Structuring - Annotation

Nyckelord och -fraser som beskriver symptom kommer att annoteras i en del av texterna i samlingen, med fokus på texter relaterade till COVID19, t.ex. nyhets- och journaltexter, vilket har tidigare gjorts på engelska.(4) Detta behövs för att träna ett NER modell samt för att utvärdera NER verktyg. 

#### 3. Anpassa ett existerande engelsk NER verktyg för svenska texter

Värdgruppen har verktyg som kan matcha texter mot listor (s.k. dictionaries) av medicinska termer på engelska (https://github.com/Aitslab/BioNLP) . För att göra om verktyget till svenska texter behövs motsvarande dictionaries på svenska. Det kommer att undersökas om ett dictionary med symptomfraser och -ord kan byggas genom att extraherar fraser från ICD-10 eller Snomed-CT. Dessutom kommer gruppens existerande dictonaries(5) att utvärderas och utökas manuellt. 4. Träna ett svensk medicinsk NER modell för symptom: Som komplement till NER med dictionaries, ska ett symptom NER modell tränas med annoterade textsamlingar som skapas tidigare i projektet (2.). 5. Utvärdering av verktyg i jämförelse med manuell läsning: Det slutliga målet för projektet är att använda de utvecklade verktyg för att analysera COVID19 patientjournaler för att extrahera vilka symptom nämns och hur ofta. För detta ska journaler från patienter som kom till akuten på SUS Malmö och testades positv för COVID19 analyseras. Alla verktyg som utvecklas i projektet (3. och 4.) ska därför blir jämförda mot annoteringarna av patientjournaler som gjordes genom manuell läsning (2.).

### Data
kommer sedan att testas på den annoterade delen av corpusen. Sedan kommer ett svenskt dictionary med symtom för covid-19 från ICD-10 koder och Snomed-CT att sammanställas. Detta kommer sedan att användas för att träna en svensk BERT (Kungliga Biblioteket) för symtom NER. Detta avslutar T5 arbetet, men projektet ämnar om det funkar sedan att gå vidare med att läsa och strukturera data från 100 000 akutmottagningsbesök under coronapandemin. Denna data i strukturerat format ämnas användas för att koppla ihop symptombild med positivt eller negativt test för covid-19 och ge en prediktiv sannolikhetsuppskattning för att en viss symptombild är kopplad till covid-19 positivitet.

## Ethical considerations

Alla texter som används i projektet ska behandlas enligt etiska och legala riktlinjer (patientsäkerhetslagen, GDPR). Etiskt tillstånd för användning av journaltexter från region Skåne finns.

## References

1. Semantic Scholar. COVID19 open dataset [Internet] [cited 202 Oct 4]. Available from: https://pages.semanticscholar.org/coronavirus-research
2. Bioinformatics, Volume 36, Issue 4, 15 February 2020, Pages 1234–1240, https://doi.org/10.1093/bioinformatics/btz682
3. (https://spraakbanken.gu.se/)
4. Cornell University Arxiv. English dictionaries, gold and silver standard corpora for biomedical natural language processing related to SARS-CoV-2 and COVID-19, arXiv:2003.09865 [q-bio.OT], https://arxiv.org/abs/2003.09865
5. https://github.com/Aitslab/corona/blob/master/dictionaries/corona_symptoms_SE.txt