package se.lth.cs.nlp.mentions;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.apache.lucene.analysis.tokenattributes.OffsetAttribute;
import org.apache.lucene.store.ByteArrayDataInput;
import org.apache.lucene.store.GrowableByteArrayDataOutput;
import org.apache.lucene.store.InputStreamDataInput;
import org.apache.lucene.store.OutputStreamDataOutput;
import org.apache.lucene.util.BytesRef;
import org.apache.lucene.util.BytesRefBuilder;
import org.apache.lucene.util.fst.ByteSequenceOutputs;
import org.apache.lucene.util.fst.FST;
import org.apache.lucene.util.fst.Util;

import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Lucene FST Index
 */
public class MentionKeyIndex {
    private Analyzer analyzer;
    private FST<BytesRef> fst;

    public Analyzer analyzer() {
        return analyzer;
    }

    public MentionKeyIndex(Analyzer analyzer, InputStream rawdata) {
        this.analyzer = analyzer;
        try {
            this.fst = new FST<>(new InputStreamDataInput(rawdata), ByteSequenceOutputs.getSingleton());
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    public MentionKeyIndex(Analyzer analyzer, byte[] rawdata) {
        this.analyzer = analyzer;
        try {
            this.fst = new FST<>(new ByteArrayDataInput(rawdata), ByteSequenceOutputs.getSingleton());
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    public MentionKeyIndex(Analyzer analyzer, File input) {
        this.analyzer = analyzer;
        try {
            this.fst = new FST<>(new InputStreamDataInput(new BufferedInputStream(new FileInputStream(input), 16*1024*1024)), ByteSequenceOutputs.getSingleton());
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    public MentionKeyIndex(Analyzer analyzer, FST<BytesRef> fst) {
        this.analyzer = analyzer;
        this.fst = fst;
    }

    private static String[] bytesRefToIds(BytesRef ref) {
        return ref.utf8ToString().split("\t");
    }

    /**
     * Utility function to find the closest matches given a list of tokens.
     * @throws IOException FST index might throw IOException
     */
    public static List<MentionKeySegment> closest(FST<BytesRef> fst, List<BytesRef> inputs) throws IOException {
        if(inputs.isEmpty())
            return Collections.emptyList();

        final ArrayList<MentionKeySegment> segments = new ArrayList<>();
        ArrayList<Integer> positionMapping = new ArrayList<Integer>();

        BytesRefBuilder brf = new BytesRefBuilder();
        positionMapping.add(brf.length());
        brf.append(inputs.get(0));

        if(inputs.size() > 1) {
            for (BytesRef input : inputs.subList(1, inputs.size())) {
                brf.append((byte)(' ' & 0xFF));
                positionMapping.add(brf.length());
                brf.append(input);
            }
        }

        final FST.BytesReader fstReader = fst.getBytesReader();

        int start = 0;
        int k = 0;
        while(k < positionMapping.size()) {
            final FST.Arc<BytesRef> arc = fst.getFirstArc(new FST.Arc<>());

            start = positionMapping.get(k);
            //System.out.println(start);

            BytesRef output = fst.outputs.getNoOutput();
            int read = 0;
            outer: for(int n = k; n < inputs.size(); n++) {
                BytesRef input = inputs.get(n);
                // Accumulate output as we go
                for(int i=0;i<input.length;i++) {
                    if (fst.findTargetArc(input.bytes[i+input.offset] & 0xFF, arc, arc, fstReader) == null) {
                        //Did not find anything more, reset to next.
                        break outer;
                    }

                    output = fst.outputs.add(output, arc.output);
                    read++;
                }

                if(arc.isFinal()) {
                    segments.add(new MentionKeySegment(k, n+1, bytesRefToIds(fst.outputs.add(output, arc.nextFinalOutput))));
                }

                //Find the space, to continue
                if(fst.findTargetArc((byte)(' ' & 0xFF), arc, arc, fstReader) == null) {
                    //it is no longer.
                    break;
                }

                output = fst.outputs.add(output, arc.output);
                read++;
            }
            k += 1;
        }

        return segments;
    }

    private static class ByteRefSegment {
        public String term;
        public BytesRef ref;
        public int start;
        public int end;

        public ByteRefSegment(String term, BytesRef ref, int start, int end) {
            this.term = term;
            this.ref = ref;
            this.start = start;
            this.end = end;
        }
    }

    /**
     * Run the analyzer and return the space seperated normalized string
     * @param text input text
     * @return normalized text
     */
    public String normalize(String text) {
        try {
            TokenStream tokenStream = analyzer.tokenStream("text", text);
            CharTermAttribute charTermAttribute = tokenStream.addAttribute(CharTermAttribute.class);

            tokenStream.reset();
            StringBuilder sb = new StringBuilder();

            if(tokenStream.incrementToken()) {
                String term = charTermAttribute.toString();
                sb.append(term);
            }

            while (tokenStream.incrementToken()) {
                String term = charTermAttribute.toString();

                sb.append(' ');
                sb.append(term);
            }

            tokenStream.close();

            return sb.toString();
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    /**
     * Get id
     * @param text unnormalized text
     * @return id or null if not found.
     */
    public String[] get(String text) {
        try {
            BytesRef retval = Util.get(this.fst, new BytesRef(normalize(text)));
            if(retval == null)
                return null;
            else
                return bytesRefToIds(retval);
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    /**
     * Get id
     * @param terms list of terms
     * @return id or null if not found.
     */
    public String[] get(List<String> terms) {
        try {
            BytesRef retval = Util.get(this.fst, new BytesRef(String.join(" ", terms)));
            if(retval == null)
                return null;
            else
                return bytesRefToIds(retval);
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    public List<MentionTerm> terms(String text) {
        try {
            List<MentionTerm> termlist = new ArrayList<>();

            TokenStream tokenStream = analyzer.tokenStream("text", text);
            OffsetAttribute offsetAttribute = tokenStream.addAttribute(OffsetAttribute.class);
            CharTermAttribute charTermAttribute = tokenStream.addAttribute(CharTermAttribute.class);
            MentionTypeAttribute mentionTypeAttribute = tokenStream.addAttribute(MentionTypeAttribute.class);

            tokenStream.reset();
            int i = 0;
            while (tokenStream.incrementToken()) {
                int startOffset = offsetAttribute.startOffset();
                int endOffset = offsetAttribute.endOffset();
                String term = charTermAttribute.toString();

                termlist.add(new MentionTerm(startOffset, endOffset, term, text.substring(startOffset,endOffset), mentionTypeAttribute.getSym(),i));
                i += 1;
            }

            tokenStream.close();
            return termlist;
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    /**
     * Search for all sequences that exist in the index
     *
     * @param text the text to find sequences in
     * @return
     */
    public SearchResult search(String text) {
        return search(analyzer, text);
    }

    /**
     * Search for all sequences that exists in the index
     *
     * @param text the text to find sequences in
     * @return list of all matches and its id.
     */
    public SearchResult search(Analyzer analyzer, String text) {
        try {

            ArrayList<ByteRefSegment> segments = new ArrayList<>();
            ArrayList<MentionTerm> terms = new ArrayList<>();

            TokenStream tokenStream = analyzer.tokenStream("text", text);
            OffsetAttribute offsetAttribute = tokenStream.addAttribute(OffsetAttribute.class);
            CharTermAttribute charTermAttribute = tokenStream.addAttribute(CharTermAttribute.class);
            MentionTypeAttribute mentionTypeAttribute = tokenStream.addAttribute(MentionTypeAttribute.class);

            int i = 0;

            tokenStream.reset();
            while (tokenStream.incrementToken()) {
                int startOffset = offsetAttribute.startOffset();
                int endOffset = offsetAttribute.endOffset();
                String term = charTermAttribute.toString();

                terms.add(new MentionTerm(startOffset, endOffset, term, text.substring(startOffset,endOffset), mentionTypeAttribute.getSym(), i));
                segments.add(new ByteRefSegment(term, new BytesRef(term), startOffset, endOffset));
                i += 1;
            }

            List<MentionKeySegment> closest = closest(this.fst, segments.stream().map(seg -> seg.ref).collect(Collectors.toList()));

            for (MentionKeySegment segment : closest) {
                segment.terms = terms.subList(segment.start, segment.end);
                segment.start = segments.get(segment.start).start;
                segment.end = segments.get(segment.end-1).end;
            }

            tokenStream.close();

            return new SearchResult(terms, closest);
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    public static class SearchResult {
        public final List<MentionTerm> terms;
        public final List<MentionKeySegment> segments;

        public SearchResult(List<MentionTerm> terms, List<MentionKeySegment> segments) {
            this.terms = terms;
            this.segments = segments;
        }

        public int start(MentionSegment segment) {
            return segment.terms.get(0).start;
        }

        public int end(MentionSegment segment) {
            return segment.terms.get(segment.terms.size()-1).end;
        }
    }

    /**
     * Search for all sequences that exits in the index
     *
     * @param terms the list of terms produced by the analyzer
     * @return
     */
    public SearchResult search(List<MentionTerm> terms) {
        try {
            if(terms.isEmpty())
                return new SearchResult(terms, Collections.emptyList());

            ArrayList<ByteRefSegment> segments = new ArrayList<>();
            for (MentionTerm term : terms) {
                segments.add(new ByteRefSegment(term.term, new BytesRef(term.term), term.start, term.end));
            }

            List<MentionKeySegment> closest = closest(this.fst, segments.stream().map(seg -> seg.ref).collect(Collectors.toList()));

            for (MentionKeySegment segment : closest) {
                segment.terms = terms.subList(segment.start, segment.end);
            }

            return new SearchResult(terms, closest);
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    /**
     * Save the FST to file.
     * @param file
     */
    public void save(File file) {
        try {
            fst.save(file.toPath());
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    public void save(OutputStream stream) {
        try {
            fst.save(new OutputStreamDataOutput(stream));
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    public byte[] save() {
        try {
            GrowableByteArrayDataOutput binaryBuffer = new GrowableByteArrayDataOutput(1024 * 1024);
            fst.save(binaryBuffer);

            return Arrays.copyOfRange(binaryBuffer.getBytes(), 0, binaryBuffer.getPosition());
        } catch (IOException e) {
            throw new IOError(e);
        }
    }
}
