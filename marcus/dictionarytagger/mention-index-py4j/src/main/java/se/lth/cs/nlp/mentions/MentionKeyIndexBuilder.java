package se.lth.cs.nlp.mentions;

import it.unimi.dsi.fastutil.bytes.ByteBigArrayBigList;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.store.GrowableByteArrayDataOutput;
import org.apache.lucene.store.OutputStreamDataOutput;
import org.apache.lucene.util.BytesRef;
import org.apache.lucene.util.BytesRefBuilder;
import org.apache.lucene.util.IntsRefBuilder;
import org.apache.lucene.util.fst.*;

import java.io.File;
import java.io.IOError;
import java.io.IOException;
import java.io.OutputStream;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * Lucene FST Builder
 */
public class MentionKeyIndexBuilder {
    private Analyzer analyzer;
    private FST<BytesRef> fst;
    private ByteBigArrayBigList buffer;
    private long[] idx;
    private long[] sizes;

    public MentionKeyIndexBuilder(Analyzer analyzer) {
        this.analyzer = analyzer;
    }

    public Analyzer analyzer() {
        return analyzer;
    }

    public FST<BytesRef> fst() {
        return this.fst;
    }

    public MentionKeyIndex index() {
        return new MentionKeyIndex(analyzer, fst());
    }

    public static class Entry implements Comparable<Entry> {
        public final BytesRef id;
        public final BytesRef terms;

        public Entry(BytesRef terms, BytesRef id) {
            this.id = id;
            this.terms = terms;
        }

        public static Entry from(Analyzer analyzer, String entry, String...id) {
            return new Entry(Mentions.tokenizeConcat(analyzer, entry), mergeIds(id));
        }

        @Override
        public int compareTo(Entry o) {
            return terms.compareTo(o.terms);
        }
    }

    private static BytesRef mergeIds(List<Entry> group) {
        BytesRefBuilder brb = new BytesRefBuilder();
        Iterator<Entry> iterator = group.iterator();
        brb.append(iterator.next().id);
        while(iterator.hasNext()) {
            brb.append((byte)'\t');
            brb.append(iterator.next().id);
        }

        return brb.toBytesRef();
    }

    private static BytesRef mergeIds(String[] group) {
        if(group.length == 0) {
            return new BytesRef();
        }
        else if(group.length == 1) {
            return new BytesRef(group[0].trim());
        }
        else {
            BytesRefBuilder brb = new BytesRefBuilder();
            brb.append(new BytesRef(group[0]));
            for(int i = 1; i < group.length; i++) {
                brb.append((byte)'\t');
                brb.append(new BytesRef(group[i].trim()));
            }
            return brb.toBytesRef();
        }
    }

    public long build(Stream<Entry> stream) {
        return build(stream, false);
    }

    /**
     * Low level build
     *
     * @param stream stream of entries where each entry consist of a byteref tokenized entry
     * @param sorted is the entry sorted or not
     * @return
     */
    public long build(Stream<Entry> stream, boolean sorted) {
        try {
            long numFstEntries = 0;

            ByteSequenceOutputs outputs = ByteSequenceOutputs.getSingleton();
            Builder<BytesRef> builder = new Builder<>(FST.INPUT_TYPE.BYTE1, outputs);
            IntsRefBuilder scratchInts = new IntsRefBuilder();

            if(!sorted)
                stream = stream.sorted();

            Iterator<Entry> entries = stream.iterator();
            Entry lastEntry = null;

            List<Entry> group = new ArrayList<>();
            while(entries.hasNext()) {
                Entry sortedEntry = entries.next();
                if(sorted && lastEntry != null && lastEntry.terms.compareTo(sortedEntry.terms) > 0)
                    throw new IllegalArgumentException("Stream is not sorted, found one example in which the next is not ordered.");

                // Merge duplicates
                if(lastEntry == null || group.isEmpty()) {
                    // No group
                    group.add(sortedEntry);
                }
                else if(sortedEntry.terms.bytesEquals(lastEntry.terms)) {
                    // Extends existing group
                    group.add(sortedEntry);
                }
                else {
                    // Commit group
                    if(group.size() == 1) {
                        builder.add(Util.toIntsRef(group.get(0).terms, scratchInts), group.get(0).id);
                    } else {
                        // All terms in group are identical, as they are equal to the previous one.
                        builder.add(Util.toIntsRef(group.get(0).terms, scratchInts), mergeIds(group));
                    }

                    group.clear();
                    group.add(sortedEntry);
                    numFstEntries++;
                }
                lastEntry = sortedEntry;
            }

            if(group.size() > 0) {
                if(group.size() == 1) {
                    builder.add(Util.toIntsRef(group.get(0).terms, scratchInts), group.get(0).id);
                } else {
                    // All terms in group are identical, as they are equal to the previous one.
                    builder.add(Util.toIntsRef(group.get(0).terms, scratchInts), mergeIds(group));
                }
            }

            this.fst = builder.finish();

            return numFstEntries;
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    /**
     * Build FST from list of entries
     *
     * @param entries the entries with string ids
     * @return
     */
    public long build(List<? extends Mentions.KeyEntry<?>> entries) {
        List<Mentions.KeyEntry> sortedEntries = entries.parallelStream()
                                                       .peek(entry -> entry.itemRef = Mentions.tokenizeConcat(analyzer, entry.item))
                                                       .sorted(Comparator.comparing(x -> x.itemRef))
                                                       .collect(Collectors.toList());

        return build(sortedEntries.stream().map(e -> new Entry(e.itemRef, mergeIds(e.id))), true);
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
