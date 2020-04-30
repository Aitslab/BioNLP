dictionarytagger
================

This project is meant to serve as a template to be modified as needed.

But if you just need to run it as is, with no modifications to use the default processing pipeline, run the following command:

```sh
./gradlew run
```

This will download all dependencies, compile the sources and start the server at port 6006.

The py4j python version can then be used.

Dictionarytagger structure
--------------------------

The main class is `se.lth.cs.nlp.mentions.App`

In this class the analyzer pipeline is defined in getAnalyzer()


Maven and JFlex tokenizer
-------------------------
The tokenizers has been generated and included in the source, but if you wish to modify the included tokenizer from its JFlex definition:

Install maven, the provided pom.xml includes a plugin that can generate the required files, and can be accessed by running:

```sh
mvn generate-sources
```

The generated sources will then be available in:

```
target/generated-soruces/jflex/[package path]
```