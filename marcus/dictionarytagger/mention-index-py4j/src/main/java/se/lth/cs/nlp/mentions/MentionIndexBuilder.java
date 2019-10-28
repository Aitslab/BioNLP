package se.lth.cs.nlp.mentions;

import it.unimi.dsi.fastutil.bytes.ByteBigArrayBigList;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.store.GrowableByteArrayDataOutput;
import org.apache.lucene.store.OutputStreamDataOutput;
import org.apache.lucene.util.BytesRef;
import org.apache.lucene.util.BytesRefBuilder;
import org.apache.lucene.util.IntsRefBuilder;
import org.apache.lucene.util.fst.Builder;
import org.apache.lucene.util.fst.FST;
import org.apache.lucene.util.fst.PositiveIntOutputs;
import org.apache.lucene.util.fst.Util;

import java.io.File;
import java.io.IOError;
import java.io.IOException;
import java.io.OutputStream;
import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * Lucene FST Builder
 */
public class MentionIndexBuilder {
    private Analyzer analyzer;
    private FST<Long> fst;
    private ByteBigArrayBigList buffer;
    private long[] idx;
    private long[] sizes;

    public MentionIndexBuilder(Analyzer analyzer) {
        this.analyzer = analyzer;
    }

    public Analyzer analyzer() {
        return analyzer;
    }

    public FST<Long> fst() {
        return this.fst;
    }

    public MentionIndex index() {
        return new MentionIndex(analyzer, fst());
    }

    private Function<ArrayList<Mentions.Entry>,Void> clusterfn;

    public void setClusterfn(Function<ArrayList<Mentions.Entry>, Void> clusterfn) {
        this.clusterfn = clusterfn;
    }

    public long build(List<? extends Mentions.Entry<?>> entries) {
        return build(entries, false);
    }

    public long buildRaw(List<? extends Mentions.Entry<?>> entries) {
        return buildRaw(entries, false);
    }

    public static class Entry implements Comparable<Entry> {
        public final long id;
        public final BytesRef terms;

        public Entry(BytesRef terms, long id) {
            this.id = id;
            this.terms = terms;
        }

        public static Entry from(Analyzer analyzer, long id, String entry) {
            return new Entry(Mentions.tokenizeConcat(analyzer, entry), id);
        }

        @Override
        public int compareTo(Entry o) {
            return terms.compareTo(o.terms);
        }
    }

    public long build(Stream<Entry> stream, boolean isSorted) {
        try {
            long numFstEntries = 0;

            PositiveIntOutputs outputs = PositiveIntOutputs.getSingleton();
            Builder<Long> builder = new Builder<Long>(FST.INPUT_TYPE.BYTE1, outputs);
            BytesRef scratchBytes = new BytesRef();
            IntsRefBuilder scratchInts = new IntsRefBuilder();
            BytesRefBuilder brb = new BytesRefBuilder();

            long fstid=0;

            if(!isSorted)
                stream = stream.sorted();

            Iterator<Entry> entries = stream.iterator();
            Entry lastEntry = null;
            while(entries.hasNext()) {
                Entry sortedEntry = entries.next();
                if(isSorted && lastEntry != null && lastEntry.terms.compareTo(sortedEntry.terms) > 0)
                    throw new IllegalArgumentException("Stream is not sorted, found one example in which the next is not ordered.");

                // Ignore duplicates
                if(!(lastEntry != null && sortedEntry.terms.bytesEquals(lastEntry.terms))) {
                    builder.add(Util.toIntsRef(sortedEntry.terms, scratchInts), Long.valueOf(sortedEntry.id));
                    numFstEntries++;
                }
                lastEntry = sortedEntry;
            }

            this.fst = builder.finish();

            return numFstEntries;
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    /**
     * Builds the FST from a list of entries (assuming they are normalized)
     * @param entries the entries
     * @return number of added entries, might be less than entries due to duplicates.
     */
    public long buildRaw(List<? extends Mentions.Entry<?>> entries, final boolean reassignId) {
        // Input values (keys). These must be provided to Builder in Unicode sorted order!

        int maxid = 0;

        try {
            long numFstEntries = 0;
            List<Mentions.Entry> sortedEntries = entries.parallelStream().map(entry -> {
                entry.itemRef = new BytesRef(entry.item);
                return entry;
            }).sorted(Comparator.comparing(x -> x.itemRef)).collect(Collectors.toList());

            PositiveIntOutputs outputs = PositiveIntOutputs.getSingleton();
            Builder<Long> builder = new Builder<Long>(FST.INPUT_TYPE.BYTE1, outputs);
            BytesRef scratchBytes = new BytesRef();
            IntsRefBuilder scratchInts = new IntsRefBuilder();
            BytesRefBuilder brb = new BytesRefBuilder();

            long fstid=0;

            ArrayList<Mentions.Entry> cluster = new ArrayList<>();

            Mentions.Entry lastEntry = null;
            for (Mentions.Entry sortedEntry : sortedEntries) {
                if(lastEntry != null && sortedEntry.itemRef.bytesEquals(lastEntry.itemRef)) {
                    if(cluster.size() == 0) {
                        cluster.add(lastEntry);
                    }

                    cluster.add(sortedEntry);

                    if(reassignId) {
                        sortedEntry.id = -1;
                    }
                } else {
                    if(cluster.size() > 0 && clusterfn != null) {
                        clusterfn.apply(cluster);
                        cluster.clear();
                    }

                    if(reassignId) {
                        sortedEntry.id = maxid++;
                    } else {
                        maxid = Math.max(maxid, sortedEntry.id);
                    }

                    builder.add(Util.toIntsRef(sortedEntry.itemRef, scratchInts), Long.valueOf(sortedEntry.id));
                    lastEntry = sortedEntry;
                    numFstEntries++;
                }
            }

            if(cluster.size() > 0 && clusterfn != null) {
                clusterfn.apply(cluster);
                cluster.clear();
            }

            this.fst = builder.finish();

            return numFstEntries;
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    /**
     * Builds the FST from a list of entries
     * @param entries the entries
     * @return number of added entries, might be less than entries due to duplicates.
     */
    public long build(List<? extends Mentions.Entry<?>> entries, final boolean reassignId) {
        // Input values (keys). These must be provided to Builder in Unicode sorted order!

        int maxid = 0;

        try {
            long numFstEntries = 0;
            List<Mentions.Entry> sortedEntries = entries.parallelStream().map(entry -> {
                entry.itemRef = Mentions.tokenizeConcat(analyzer, entry.item);
                return entry;
            }).sorted(Comparator.comparing(x -> x.itemRef)).collect(Collectors.toList());

            PositiveIntOutputs outputs = PositiveIntOutputs.getSingleton();
            Builder<Long> builder = new Builder<Long>(FST.INPUT_TYPE.BYTE1, outputs);
            BytesRef scratchBytes = new BytesRef();
            IntsRefBuilder scratchInts = new IntsRefBuilder();
            BytesRefBuilder brb = new BytesRefBuilder();

            long fstid=0;

            ArrayList<Mentions.Entry> cluster = new ArrayList<>();

            Mentions.Entry lastEntry = null;
            for (Mentions.Entry sortedEntry : sortedEntries) {
                if(lastEntry != null && sortedEntry.itemRef.bytesEquals(lastEntry.itemRef)) {
                    if(cluster.size() == 0) {
                        cluster.add(lastEntry);
                    }

                    cluster.add(sortedEntry);

                    if(reassignId) {
                        sortedEntry.id = -1;
                    }
                } else {
                    if(cluster.size() > 0 && clusterfn != null) {
                        clusterfn.apply(cluster);
                        cluster.clear();
                    }

                    if(reassignId) {
                        sortedEntry.id = maxid++;
                    } else {
                        maxid = Math.max(maxid, sortedEntry.id);
                    }

                    builder.add(Util.toIntsRef(sortedEntry.itemRef, scratchInts), Long.valueOf(sortedEntry.id));
                    lastEntry = sortedEntry;
                    numFstEntries++;
                }
            }

            if(cluster.size() > 0 && clusterfn != null) {
                clusterfn.apply(cluster);
                cluster.clear();
            }

            this.fst = builder.finish();

            return numFstEntries;
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
