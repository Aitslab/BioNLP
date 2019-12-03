package se.lth.cs.nlp.mentions;

import it.unimi.dsi.fastutil.ints.Int2ObjectOpenHashMap;
import org.apache.lucene.analysis.custom.CustomAnalyzer;
import org.apache.lucene.analysis.icu.ICUNormalizer2FilterFactory;
import org.apache.lucene.analysis.pattern.PatternTokenizerFactory;
import py4j.GatewayServer;

import java.io.File;
import java.io.IOError;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;

import org.apache.lucene.analysis.Analyzer;
import se.lth.cs.docria.*;
import se.lth.cs.docria.algorithms.DominantRight;

public class App
{

    public Analyzer addAnalyzerFilters(CustomAnalyzer.Builder builder) {
        try {
            return builder.addTokenFilter(ICUNormalizer2FilterFactory.class, "name", "nfkc", "mode", "decompose")
                          .addTokenFilter(DiacriticFilterFactory.class)
                          .build();

        } catch (IOException e) {
            throw new IOError(e);
        }
    }
    /**
     * Get the lucene analyzer
     *
     * The task of the analyzer is to divide the incomming text into terms,
     * and might go through multiple levels of filtering and splitting.
     */
    public Analyzer getAnalyzer() {
        try {
            return addAnalyzerFilters(
                    CustomAnalyzer.builder()
                                  .withTokenizer(MentionTokenizerFactory.class));

        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    /**
     * Get the tab tokenized analyzer, tokenization is a split by tab
     *
     * The task of the analyzer is to divide the incomming text into terms,
     * and might go through multiple levels of filtering and splitting.
     */
    public Analyzer getTabTokenizedAnalyzer() {
        try {
            return addAnalyzerFilters(
                    CustomAnalyzer.builder()
                                  .withTokenizer(PatternTokenizerFactory.class, "pattern", "\t"));

        } catch (IOException e) {
            throw new IOError(e);
        }
    }


    /**
     * Return terms given text
     * @param analyzer the analyzer to use
     * @param text the text it self
     * @return
     */
    public List<String> terms(Analyzer analyzer, String text) {
        return Mentions.terms(analyzer, text);
    }

    /**
     * Construct the index
     *
     * <b>Remarks:</b> This function uses getAnalyzer() for its analyzer.
     * @param dictionary one line per entry, id is equal to zero based line number
     * @param output where to store the index
     */
    public void buildIndex(File dictionary, File output) {
        Analyzer analyzer = getAnalyzer();

        try {
            List<String> words = Files.readAllLines(dictionary.toPath(), StandardCharsets.UTF_8);
            Stream<MentionIndexBuilder.Entry> entryStream =
                    IntStream.range(0, words.size()).mapToObj(i -> MentionIndexBuilder.Entry.from(analyzer, i,
                                                                                                  words.get(i)));

            MentionIndexBuilder mentionIndexBuilder = new MentionIndexBuilder(analyzer);
            long numEntries = mentionIndexBuilder.build(entryStream.distinct(), false);
            System.out.println(String.format("Found %d entries", numEntries));
            mentionIndexBuilder.save(output);
            System.out.println("Mention Index saved to " + output.getName());
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    /**
     * Construct the keyed index (mention is mapped to a list of IDs as strings)
     *
     * <b>Remarks:</b> This function uses getAnalyzer() for its analyzer.
     * @param dictionary one line per entry, tab separation for the key, more than one is allowed.
     * @param output where to store the index
     */
    public void buildKeyedIndex(File dictionary, File output) {
        Analyzer analyzer = getAnalyzer();

        try {
            List<String> lines = Files.readAllLines(dictionary.toPath(), StandardCharsets.UTF_8);
            /*Stream<MentionKeyIndexBuilder.Entry> entryStream =
                    IntStream.range(0, words.size()).mapToObj(i -> MentionKeyIndexBuilder.Entry.from(analyzer, i,
                                                                                                  words.get(i)));*/

            MentionKeyIndexBuilder mentionIndexBuilder = new MentionKeyIndexBuilder(analyzer);
            long numEntries = mentionIndexBuilder.build(lines.stream().filter(ln -> ln.trim().length() > 0).map(ln -> {
                String[] parts = ln.split("\t", 2);
                if(parts.length == 0) {
                    // Keyless
                    System.out.println("WARNING, line: " + parts[0] + " lacks key, will assume no empty key");
                    return MentionKeyIndexBuilder.Entry.from(analyzer, parts[0]);
                } else {
                    return MentionKeyIndexBuilder.Entry.from(analyzer, parts[0], parts[1]);
                }
            }));

            System.out.println(String.format("Found %d entries", numEntries));
            mentionIndexBuilder.save(output);
            System.out.println("Mention Index saved to " + output.getName());
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    /**
     * Load index from disk
     *
     * <b>Remarks:</b> This function uses getAnalyzer() for its analyzer.
     * @param index path to index
     */
    public MentionIndex loadIndex(File index) {
        return new MentionIndex(getAnalyzer(), index);
    }

    /**
     * Load index from disk
     *
     * <b>Remarks:</b> This function uses getAnalyzer() for its analyzer.
     * @param index path to index
     */
    public MentionKeyIndex loadKeyedIndex(File index) {
        return new MentionKeyIndex(getAnalyzer(), index);
    }

    /**
     * Search docria document
     *
     * @param index
     * @param docria
     * @return
     */
    public byte[] search(MentionIndex index, byte[] docria) {
        Document decode = MsgpackCodec.decode(docria);
        Text main = decode.text("main");

        decode.remove(decode.layer("terms"));
        decode.remove(decode.layer("matches"));

        Layer terms = decode.add(Layer.create("terms")
                                      .addField("term", DataTypes.STRING)
                                      .addField("type", DataTypes.STRING)
                                      .addField("text", main.spanType())
                                      .build());

        Layer matches = decode.add(Layer.create("matches")
                                        .addField("text", main.spanType())
                                        .addField("id", DataTypes.INT_64)
                                        .addField("terms", DataTypes.noderef_array(terms.name()))
                                        .build());

        List<MentionTerm> termlist = index.terms(main.toString());

        Int2ObjectOpenHashMap<Node> termid2term = new Int2ObjectOpenHashMap<>();
        termlist.forEach(mt -> {
            Node termnode = terms.create()
                 .put("term", mt.term)
                 .put("type", mt.type.toString())
                 .put("text", main.span(mt.start, mt.end))
                 .insert();
            termid2term.put(mt.idx, termnode);
        });

        index.search(main.toString()).forEach(ms -> {
            matches.create()
                   .put("text", main.span(ms.start, ms.end))
                   .put("id", ms.value)
                   .put("terms", ms.terms.stream().map(mt -> termid2term.get(mt.idx)).collect(Collectors.toList()))
                   .insert();
        });

        matches.retainAll(DominantRight.resolve(matches, "text"));
        return MsgpackCodec.encode(decode).toByteArray();
    }

    /**
     * Search docria document
     *
     * @param index
     * @param docria
     * @return
     */
    public byte[] search(MentionKeyIndex index, byte[] docria) {
        Document decode = MsgpackCodec.decode(docria);
        Text main = decode.text("main");

        decode.remove(decode.layer("terms"));
        decode.remove(decode.layer("matches"));

        Layer terms = decode.add(Layer.create("terms")
                                      .addField("term", DataTypes.STRING)
                                      .addField("type", DataTypes.STRING)
                                      .addField("text", main.spanType())
                                      .build());

        Layer matches = decode.add(Layer.create("matches")
                                        .addField("text", main.spanType())
                                        .addField("ids", DataTypes.STRING)
                                        .addField("terms", DataTypes.noderef_array(terms.name()))
                                        .build());

        List<MentionTerm> termlist = index.terms(main.toString());

        Int2ObjectOpenHashMap<Node> termid2term = new Int2ObjectOpenHashMap<>();
        termlist.forEach(mt -> {
            Node termnode = terms.create()
                                 .put("term", mt.term)
                                 .put("type", mt.type.toString())
                                 .put("text", main.span(mt.start, mt.end))
                                 .insert();
            termid2term.put(mt.idx, termnode);
        });

        index.search(main.toString()).segments.forEach(ms -> {
            matches.create()
                   .put("text", main.span(ms.start, ms.end))
                   .put("ids", String.join("\t", ms.ids))
                   .put("terms", ms.terms.stream().map(mt -> termid2term.get(mt.idx)).collect(Collectors.toList()))
                   .insert();
        });

        matches.retainAll(DominantRight.resolve(matches, "text"));
        return MsgpackCodec.encode(decode).toByteArray();
    }

    /**
     * Search pretokenized docria document
     *
     * @param index the index to use
     * @param inputSentences the sentences to annotate
     * @return
     */
    public byte[] searchPreTokenized(MentionKeyIndex index, List<List<String>> inputSentences) {
        Document document = new Document();
        Layer tokens = document.add(Layer.builder("tokens")
                                         .addField("term", DataTypes.STRING)
                                         .addField("text", DataTypes.STRING)
                                         .build());

        Layer sentences = document.add(Layer.builder("sentence")
                                            .addField("tokens", DataTypes.nodespan("tokens"))
                                            .build());


        Layer matches = document.add(Layer.builder("matches")
                                          .addField("id", DataTypes.STRING)
                                          .addField("tokens", DataTypes.nodespan("tokens"))
                                          .build());

        for (List<String> inputSentence : inputSentences) {
            // 1. Add tokens
            String tokenized = String.join("\t", inputSentence);
            List<MentionTerm> terms = Mentions.tokenize(getTabTokenizedAnalyzer(), tokenized);

            // 2. Add terms
            List<Node> sentenceTokens = new ArrayList<>();
            terms.forEach(t -> {
                Node token = Node.builder(tokens)
                                   .put("id", t.idx)
                                   .put("term", t.term)
                                   .put("text", t.raw)
                                   .build();

                sentenceTokens.add(token);
            });

            tokens.addAll(sentenceTokens);

            Node sentence = Node.builder(sentences)
                     .put("tokens", new NodeSpan(sentenceTokens.get(0), sentenceTokens.get(sentenceTokens.size()-1)))
                     .build();

            sentences.add(sentence);

            // 3. Run Search
            MentionKeyIndex.SearchResult search = index.search(terms);
            for (MentionKeySegment segment : search.segments) {
                Node left = sentenceTokens.get(segment.start);
                Node right = sentenceTokens.get(segment.end-1);
                Node match = Node.builder(matches)
                    .put("id", String.join("\t", segment.ids))
                    .put("tokens", new NodeSpan(left, right))
                    .build();

                matches.add(match);
            }
        }

        matches.retainAll(DominantRight.resolveNodespans(matches, "tokens"));
        return MsgpackCodec.encode(document).toByteArray();
    }

    public static void main(String[] args) {
        Map<String, String> arguments = new TreeMap<>();
        for (int i = 0; i < args.length; i++) {
            if(args[i].startsWith("--")) {
                String option = args[i].substring(2);
                if(i + 1 < args.length) {
                    String value = args[i+1];
                    i++;
                    arguments.put(option, value);
                }
                else {
                    System.out.println("Invalid argument: " + args[i] + ", no options is following it!");
                }
            }
        }


        int port = Integer.parseInt(arguments.getOrDefault("port", "6006"));
        GatewayServer gatewayServer = new GatewayServer(new App(), port);
        gatewayServer.start();
        System.out.println(String.format("Mention Index Py4j Gateway Server Started at port %d", port));
    }
}
