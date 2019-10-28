package se.lth.cs.nlp.mentions;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.apache.lucene.analysis.tokenattributes.OffsetAttribute;
import org.apache.lucene.util.BytesRef;

import java.io.IOError;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by csz-mkg on 2017-06-07.
 */
public class Mentions {
    public static List<MentionTerm> tokenize(Analyzer analyzer, String text) {
        try {
            ArrayList<MentionTerm> terms = new ArrayList<>();

            TokenStream tokenStream = analyzer.tokenStream("text", text);
            OffsetAttribute offsetAttribute = tokenStream.addAttribute(OffsetAttribute.class);
            CharTermAttribute charTermAttribute = tokenStream.addAttribute(CharTermAttribute.class);
            MentionTypeAttribute mentionTypeAttribute = tokenStream.addAttribute(MentionTypeAttribute.class);

            tokenStream.reset();

            int i = 0;

            try {
                while (tokenStream.incrementToken()) {
                    final int start = offsetAttribute.startOffset();
                    final int end = offsetAttribute.endOffset();
                    String term = charTermAttribute.toString();
                    Sym sym = mentionTypeAttribute.getSym();
                    terms.add(new MentionTerm(start, end, term, text.substring(start, end), sym, i++));
                }
            } finally {
                tokenStream.close();
            }

            return terms;
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    public static List<String> terms(Analyzer analyzer, String text) {
        try {
            ArrayList<String> terms = new ArrayList<>();

            TokenStream tokenStream = analyzer.tokenStream("text", text);
            OffsetAttribute offsetAttribute = tokenStream.addAttribute(OffsetAttribute.class);
            CharTermAttribute charTermAttribute = tokenStream.addAttribute(CharTermAttribute.class);
            MentionTypeAttribute mentionTypeAttribute = tokenStream.addAttribute(MentionTypeAttribute.class);

            tokenStream.reset();

            int i = 0;

            try {
                while (tokenStream.incrementToken()) {
                    final int start = offsetAttribute.startOffset();
                    final int end = offsetAttribute.endOffset();
                    String term = charTermAttribute.toString();
                    Sym sym = mentionTypeAttribute.getSym();
                    terms.add(term);
                }
            } finally {
                tokenStream.close();
            }

            return terms;
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    public static List<MentionTerm> tokenize(Analyzer analyzer, String text, int offset) {
        try {
            ArrayList<MentionTerm> terms = new ArrayList<>();

            TokenStream tokenStream = analyzer.tokenStream("text", text);
            OffsetAttribute offsetAttribute = tokenStream.addAttribute(OffsetAttribute.class);
            CharTermAttribute charTermAttribute = tokenStream.addAttribute(CharTermAttribute.class);
            MentionTypeAttribute mentionTypeAttribute = tokenStream.addAttribute(MentionTypeAttribute.class);

            tokenStream.reset();

            int i = 0;

            try {
                while (tokenStream.incrementToken()) {
                    final int start = offsetAttribute.startOffset();
                    final int end = offsetAttribute.endOffset();
                    String term = charTermAttribute.toString();
                    Sym sym = mentionTypeAttribute.getSym();
                    terms.add(new MentionTerm(start+offset, end+offset, term, text.substring(start, end), sym, i++));
                }
            } finally {
                tokenStream.close();
            }

            return terms;
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    public static List<List<MentionTerm>> segment(Analyzer analyzer, String text) {
        return segment(analyzer, text, false);
    }

    public static List<List<MentionTerm>> segment(Analyzer analyzer, String text, boolean disableWordLimit) {
        Segmenter segmenter = new Segmenter(text, disableWordLimit);
        ArrayList<List<MentionTerm>> segments = new ArrayList<>();
        for (Segment segment : segmenter.segments()) {
            List<MentionTerm> tokenized = tokenize(analyzer, text.substring(segment.start(), segment.end()), segment.start());

            if(!tokenized.isEmpty()) {
                segments.add(tokenized);
            }
        }

        return segments;
    }

    public static String tokenizeConcatString(Analyzer analyzer, String text) {
        try {
            StringBuilder sb = new StringBuilder();

            TokenStream tokenStream = analyzer.tokenStream("text", text);
            CharTermAttribute charTermAttribute = tokenStream.addAttribute(CharTermAttribute.class);

            tokenStream.reset();

            try {
                if(tokenStream.incrementToken()) {
                    String term = charTermAttribute.toString();
                    sb.append(term);
                }

                while (tokenStream.incrementToken()) {
                    String term = charTermAttribute.toString();
                    sb.append(' ');
                    sb.append(term);
                }
            } finally {
                tokenStream.close();
            }

            return sb.toString();
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    public static String[] tokenizeStringType(Analyzer analyzer, String text) {
        try {
            ArrayList<String> tokens = new ArrayList<>();
            //StringBuilder sb = new StringBuilder();

            TokenStream tokenStream = analyzer.tokenStream("text", text);
            CharTermAttribute charTermAttribute = tokenStream.addAttribute(CharTermAttribute.class);
            MentionTypeAttribute mentionAttribute = tokenStream.addAttribute(MentionTypeAttribute.class);

            tokenStream.reset();
            try {
                if (tokenStream.incrementToken()) {
                    String term = charTermAttribute.toString();
                    tokens.add(term + " " + mentionAttribute.getSym());
                }

                while (tokenStream.incrementToken()) {
                    String term = charTermAttribute.toString();
                    tokens.add(term + " " + mentionAttribute.getSym());
                }

            }
            finally {
                tokenStream.close();
            }

            return tokens.toArray(new String[tokens.size()]);
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    static BytesRef tokenizeConcat(Analyzer analyzer, String text) {
        return new BytesRef(tokenizeConcatString(analyzer, text));
    }

    public static class Entry<T> {
        public int id;
        public final String item;
        protected BytesRef itemRef;
        public final T payload;

        public Entry(String item) {
            this.item = item;
            this.id = -1;
            this.payload = null;
        }

        public Entry(String item, int id) {
            this.item = item;
            this.id = id;
            this.payload = null;
        }

        public Entry(String item, int id, T payload) {
            this.item = item;
            this.id = id;
            this.payload = payload;
        }
    }

}
