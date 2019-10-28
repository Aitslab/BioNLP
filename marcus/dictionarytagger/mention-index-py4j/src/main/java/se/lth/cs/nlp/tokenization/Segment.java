package se.lth.cs.nlp.tokenization;

import org.apache.lucene.analysis.Analyzer;
import se.lth.cs.nlp.mentions.MentionAnalyzerPipelines;
import se.lth.cs.nlp.mentions.MentionTerm;
import se.lth.cs.nlp.mentions.Mentions;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;

public class Segment extends ArrayList<Token> implements Comparable<Segment> {

    /**
     * Segment text
     * @param lang the language to use (uses internally MentionAnalyzerPipelines.get method to get the analyzer)
     * @param text the text to segment
     * @return list of segments
     */
    public static List<Segment> segment(String lang, String text) {
        return segment(MentionAnalyzerPipelines.get(lang), text, lang.startsWith("zh"));
    }

    /**
     * Segment text
     * @param analyzer the analyzer to use for segmentation
     * @param text the text to segment
     * @return list of segments
     */
    public static List<Segment> segment(Analyzer analyzer, boolean logographic, String text) {
        return segment(analyzer, text, logographic);
    }

    private static Token token(Segment segment, MentionTerm mt, String value) {
        return new Token(segment, mt.start, mt.end, value, mt.raw, mt.type);
    }

    private static Stream<Token> tokens(Segment segment, List<MentionTerm> terms, boolean logographic) {
        return terms.stream().map(mt -> {
            switch (mt.type) {
                case WORD:
                case WORD_INITIAL:
                case WORD_MIXED_CASE_LOWER:
                case WORD_MIXED_CASE_UPPER:
                case WORD_TITLE_CASE:
                case WORD_UPPER_CASE:
                    /*if(logographic || mt.raw.matches("\\p{L}[\\p{L}\\.]*"))
                        return token(segment, mt, mt.raw);
                    else
                        return token(segment, mt, "");*/
                case WORD_ACRONYM:
                    return token(segment, mt, mt.term);
                case BANG:
                case QUESTION:
                case COLON:
                case SEMICOLON:
                case AMPERSAND:
                case BRACKET_LEFT:
                case BRACKET_RIGHT:
                case CURLY_LEFT:
                case CURLY_RIGHT:
                case DATE:
                case DATETIME:
                case PIPE:
                case HASHTAG:
                case RANGE:
                case SLASH:
                case PAREN_LEFT:
                case PAREN_RIGHT:
                case TIME:
                    return token(segment, mt, mt.raw);
                case PERCENT: return token(segment, mt, "%");
                case APOSTROPHE: return token(segment, mt, "'");
                case ELISION_PREFIX:
                    if(mt.raw.substring(0,mt.raw.length()-1).matches("\\p{L}+"))
                        return token(segment, mt, mt.raw);
                    else
                        return token(segment, mt, "");
                case ELISION_SUFFIX:
                    if(mt.raw.substring(1).matches("\\p{L}+"))
                        return token(segment, mt, mt.raw);
                    else
                        return token(segment, mt, "");
                case PERIOD: return token(segment, mt, ".");
                case COMMA: return token(segment, mt, ",");
                case CITATION: return token(segment, mt, "\"");
                case HYPHEN: return token(segment, mt, "-");
                case CURRENCY: return token(segment, mt, "{CURRENCY}");
                case URL: return token(segment, mt, "{URL}");
                case ISBN: return token(segment, mt, "{ISBN}");
                case RFC: return token(segment, mt, "{RFC}");
                case PMID: return token(segment, mt, "{PMID}");
                case NUMBER: return token(segment, mt, "{NUMBER}");
                default:
                    return token(segment, mt, "");
            }
        }).filter(t -> !t.value.isEmpty());
    }

    /**
     * Get a single segment from terms
     * @param terms       terms
     * @param logogrpahic is logographic input?
     * @return single segment
     */
    public static Segment tokens(List<MentionTerm> terms, boolean logogrpahic) {
        Segment segment = new Segment();
        tokens(segment, terms, logogrpahic).forEach(segment::add);
        return segment;
    }

    /**
     * Segments text given a analyzer
     * @param analyzer    the Lucene Analyzer pipeline to use
     * @param text        the text to segment
     * @param logographic special rules applies to logographic languages regarding minimum token lengths.
     * @return list of segments
     */
    public static List<Segment> segment(Analyzer analyzer, String text, boolean logographic) {
        List<List<MentionTerm>> mentionSegments = Mentions.segment(analyzer, text, logographic);

        ArrayList<Segment> segments = new ArrayList<>();

        for (List<MentionTerm> mentionSegment : mentionSegments) {
            Segment segment = new Segment();
            tokens(segment, mentionSegment, logographic).forEach(segment::add);

            for (int i = 0; i < segment.size(); i++) {
                segment.get(i).index = i;
            }

            if(!segment.isEmpty())
                segments.add(segment);
        }

        return segments;
    }

    @Override
    public int compareTo(Segment o) {
        return Integer.compare(get(0).start, o.get(0).start);
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (Token token : this) {
            sb.append(token.index).append('\t')
              .append(token.start).append('\t')
              .append(token.end).append('\t')
              .append(token.raw).append('\t')
              .append(token.value)
              .append('\n');
        }

        return sb.toString();
    }
}
