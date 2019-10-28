package se.lth.cs.nlp.util;

import it.unimi.dsi.fastutil.ints.*;
import it.unimi.dsi.fastutil.objects.ObjectBidirectionalIterator;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.stream.Stream;
import java.util.stream.StreamSupport;

public class IntersectingSet<T> {
    public static class Entry<T> {
        protected int id = -1;
        public int group;
        public T item;
        public int start;
        public int end;

        public Entry(T item, int start, int end) {
            this.item = item;
            this.start = start;
            this.end = end;

            if(end < start)
                throw new IllegalArgumentException("end must be equal to or larger than start");
        }

        public Entry(T item, int group, int start, int end) {
            this(item, start, end);
            this.group = group;
        }

        public static <T> Entry<T> of(T value, int start, int end) {
            return new Entry<T>(value, start, end);
        }
        public static <T> Entry<T> of(T value, int group, int start, int end) {
            return new Entry<T>(value, group, start, end);
        }
    }

    private static class PositionGroup<T> {
        ArrayList<Entry<T>> startingEntries = new ArrayList<>();
        ArrayList<Entry<T>> endingEntries = new ArrayList<>();
        ArrayList<Entry<T>> startingEndingEntries = new ArrayList<>();
    }

    private Int2ObjectAVLTreeMap<PositionGroup<T>> index = new Int2ObjectAVLTreeMap<>();
    private ArrayList<Entry<T>> indexEntries = new ArrayList<>();
    private int idcnt = 0;

    public void addAll(Iterable<Entry<T>> input) {
        addAll(StreamSupport.stream(input.spliterator(), false));
    }

    public void addAll(Stream<Entry<T>> input) {
        input.forEach(e -> {
            indexEntries.add(e);

            e.id = idcnt++;
            PositionGroup<T> startpos = index.get(e.start);
            if(startpos == null) {
                startpos = new PositionGroup<>();
                index.put(e.start, startpos);
            }

            startpos.startingEntries.add(e);

            PositionGroup<T> endpos = index.get(e.end);
            if(endpos == null) {
                endpos = new PositionGroup<>();
                index.put(e.end, endpos);
            }

            endpos.endingEntries.add(e);

            if(e.start == e.end) {
                startpos.startingEndingEntries.add(e);
            }
        });
    }

    public static class Result<A,B> {
        public Entry<A> item;
        public List<Entry<B>> intersections = new ArrayList<>();

        public Int2ObjectOpenHashMap<List<Entry<B>>> grouped() {
            Int2ObjectOpenHashMap<List<Entry<B>>> groups = new Int2ObjectOpenHashMap<>();

            for (Entry<B> intersection : intersections) {
                List<Entry<B>> entries = groups.get(intersection.group);
                if(entries == null) {
                    entries = new ArrayList<>();
                    groups.put(intersection.group, entries);
                }

                entries.add(intersection);
            }

            return groups;
        }

        public Result(Entry<A> item) {
            this.item = item;
        }
    }

    public static <TPrimary,TSecondary> List<Result<TPrimary,TSecondary>> intersects(List<Entry<TPrimary>> index, List<Entry<TSecondary>> ranges, boolean includeAllRanges) {
        IntersectingSet<TPrimary> setIndex = new IntersectingSet<TPrimary>();
        setIndex.addAll(index);
        return setIndex.findIntersecting(ranges, includeAllRanges);
    }

    @SuppressWarnings("unchecked")
    public <B> List<Result<T,B>> findIntersecting(List<Entry<B>> problem, boolean alwaysIncludeAllIndexed) {
        int id = index.size();
        Result<T,B>[] items = (Result<T,B>[])new Result[idcnt];
        int itemsAllocated = 0;

        Int2ObjectAVLTreeMap<PositionGroup<B>> problemIndex = new Int2ObjectAVLTreeMap<>();
        ArrayList<Entry<B>> problemItems = new ArrayList<>();

        //1. Create searchable index in O(N log N)
        Iterator<Entry<B>> iter = problem.iterator();
        int tmpidcnt = idcnt;
        while(iter.hasNext()) {
            Entry<B> next = iter.next();
            next.id = tmpidcnt++;
            PositionGroup<B> startpos = problemIndex.get(next.start);
            if(startpos == null) {
                startpos = new PositionGroup<>();
                problemIndex.put(next.start, startpos);
            }

            startpos.startingEntries.add(next);

            PositionGroup<B> endpos = problemIndex.get(next.end);
            if(endpos == null) {
                endpos = new PositionGroup<>();
                problemIndex.put(next.end, endpos);
            }

            endpos.endingEntries.add(next);

            if(next.start == next.end) {
                startpos.startingEndingEntries.add(next);
            }

            problemItems.add(next);
        }

        //2. Merge and find phase
        ObjectBidirectionalIterator<Int2ObjectMap.Entry<PositionGroup<T>>> indexedIter = index.int2ObjectEntrySet()
                                                                                           .iterator();

        ObjectBidirectionalIterator<Int2ObjectMap.Entry<PositionGroup<B>>> problemIter = problemIndex.int2ObjectEntrySet
                ().iterator();

        if(!indexedIter.hasNext() || !problemIter.hasNext()) {
            if(alwaysIncludeAllIndexed) {
                for (int i = 0; i < items.length; i++) {
                    items[i] = new Result<>(indexEntries.get(i));
                }

                ArrayList<Result<T,B>> output = new ArrayList<>(items.length);
                Collections.addAll(output, items);
                return output;
            }
            else
                return Collections.emptyList();
        }

        IntOpenHashSet indexAlive = new IntOpenHashSet();
        IntOpenHashSet problemAlive = new IntOpenHashSet();

        Int2ObjectMap.Entry<PositionGroup<T>> indexCurrent = indexedIter.next();
        Int2ObjectMap.Entry<PositionGroup<B>> problemCurrent = problemIter.next();

        do {
            //1. Add starting and remove ending
            PositionGroup<T> indexGroup = null;
            if(indexCurrent.getIntKey() <= problemCurrent.getIntKey()) {
                indexGroup = indexCurrent.getValue();
                for (Entry<T> endingEntry : indexGroup.endingEntries) {
                    indexAlive.remove(endingEntry.id);
                }

                for (Entry<T> startingEntry : indexGroup.startingEntries) {
                    indexAlive.add(startingEntry.id);
                }
            }

            PositionGroup<B> problemGroup = null;
            if(problemCurrent.getIntKey() <= indexCurrent.getIntKey()) {
                problemGroup = problemCurrent.getValue();

                for (Entry<B> endingEntry : problemGroup.endingEntries) {
                    problemAlive.remove(endingEntry.id);
                }


                for (Entry<B> startingEntry : problemGroup.startingEntries) {
                    problemAlive.add(startingEntry.id);
                }
            }

            if(indexGroup != null && !indexGroup.startingEntries.isEmpty() && (!problemAlive.isEmpty() || alwaysIncludeAllIndexed)) {
                //Add all problems to new indexed ones
                for (Entry<T> startingEntry : indexGroup.startingEntries) {
                    int tid = startingEntry.id;
                    Result<T,B> res = items[tid];
                    if(res == null) {
                        res = items[tid] = new Result<>(indexEntries.get(tid));
                        itemsAllocated++;
                    }

                    IntIterator aliveInProblem = problemAlive.iterator();
                    while(aliveInProblem.hasNext()) {
                        res.intersections.add(problemItems.get(aliveInProblem.nextInt() - idcnt));
                    }
                }
            }

            if(problemGroup != null && problemGroup.startingEntries.size() > 0 &&
               !(indexGroup != null && !indexGroup.startingEntries.isEmpty())) {

                IntIterator aliveInIndex = indexAlive.iterator();
                while(aliveInIndex.hasNext()) {
                    int tid = aliveInIndex.nextInt();
                    Result<T,B> res = items[tid];
                    if(res == null) {
                        res = items[tid] = new Result<>(indexEntries.get(tid));
                        itemsAllocated++;
                    }

                    res.intersections.addAll(problemGroup.startingEntries);
                }
            }

            if(indexCurrent.getIntKey() == problemCurrent.getIntKey()) {
                //Move both forward
                indexCurrent = indexedIter.hasNext() ? indexedIter.next() : null;
                problemCurrent = problemIter.hasNext() ? problemIter.next() : null;
            }
            else if(indexCurrent.getIntKey() < problemCurrent.getIntKey()) {
                //Move index forward
                indexCurrent = indexedIter.hasNext() ? indexedIter.next() : null;
            }
            else {
                //Move problem index forward
                problemCurrent = problemIter.hasNext() ? problemIter.next() : null;
            }


            if(indexGroup != null) {
                for (Entry<T> entry : indexGroup.startingEndingEntries) {
                    indexAlive.remove(entry.id);
                }
            }

            if(problemGroup != null) {
                for (Entry<B> entry : problemGroup.startingEndingEntries) {
                    problemAlive.remove(entry.id);
                }
            }
        } while(indexCurrent != null && problemCurrent != null);

        ArrayList<Result<T,B>> output = new ArrayList<>(itemsAllocated);
        for (Result<T, B> item : items) {
            if(item != null) {
                output.add(item);
            }
        }

        return output;
    }
}
