package se.lth.cs.nlp.mentions;

import it.unimi.dsi.fastutil.chars.*;
import it.unimi.dsi.fastutil.ints.IntArrayList;
import it.unimi.dsi.fastutil.ints.IntStack;

import java.util.*;
import java.util.function.Consumer;

/**
 * Char Trie implementation
 */
public class CharTrie<T> {
    private static class NodeLocation {
        public Node node;
        public int delta;
    }

    private static abstract class Node<T> {
        protected abstract Node get(char ch);

        protected abstract Node find(char ch);

        protected void find(NodeLocation nodeLocation, char[] data, int offset) {
            nodeLocation.node = find(data[offset]);
            nodeLocation.delta = 1;
        }

        protected abstract boolean isOutput();

        protected abstract OutputNode output();
    }

    private static class IndexedNode<T> extends Node<T> {
        public char ch;
        public IndexedNode parent;
        public Char2ObjectRBTreeMap<IndexedNode<T>> index = new Char2ObjectRBTreeMap<>();

        public IndexedNode(char ch, IndexedNode<T> parent) {
            this.ch = ch;
            this.parent = parent;
        }

        protected final Node get(char ch) {
            IndexedNode<T> node = index.get(ch);
            if(node == null) {
                node = new IndexedNode<>(ch, this);
                index.put(ch, node);
            }
            return node;
        }

        protected final Node find(char ch) {
            return index.get(ch);
        }

        protected boolean isOutput() {
            return false;
        }

        protected OutputNode<T> output() {
            IndexedOutputNode<T> outNode = new IndexedOutputNode<>(ch, parent);
            outNode.index = index;

            for (Char2ObjectMap.Entry<IndexedNode<T>> entry : outNode.index.char2ObjectEntrySet()) {
                entry.getValue().parent = outNode;
            }

            this.parent.index.put(ch, outNode);
            return outNode;
        }


        @Override
        public String toString() {
            return "IndexedNode{" +
                    "ch=" + ch +
                    '}';
        }
    }

    private interface PathCompressionNode {
        char[] path();
        default boolean pathFound(char[] text, int offset) {
            char[] path = path();
            if(text.length-offset < path.length)
                return false;
            else {
                return false;
            }
        }
    }

    private interface OutputNode<T> {
        T value();
    }

    private static class IndexedOutputNode<T> extends IndexedNode<T> implements OutputNode<T> {
        public T output;

        public IndexedOutputNode(char ch, IndexedNode parent) {
            super(ch, parent);
            this.output = null;
        }

        @Override
        protected boolean isOutput() {
            return true;
        }

        @Override
        protected OutputNode<T> output() {
            return this;
        }

        @Override
        public T value() {
            return this.output;
        }

        @Override
        public String toString() {
            return "OutputNode{" +
                    "ch=" + ch +
                    "output=" + output +
                    '}';
        }
    }

    private static class CompiledNode<T> extends Node<T> implements PathCompressionNode {
        public char[] path;
        public char[] items;
        public CompiledNode[] nodes;

        @Override
        public char[] path() {
            return new char[0];
        }

        @Override
        protected Node get(char ch) {
            throw new UnsupportedOperationException();
        }

        @Override
        protected final Node find(char ch) {
            if(this.items == null)
                return null;

            int i = Arrays.binarySearch(items, ch);
            if(i >= 0)
                return nodes[i];
            else
                return null;
        }

        @Override
        protected final void find(final NodeLocation nodeLocation, final char[] data, int offset) {
            final int k;

            if(this.items == null || (k = Arrays.binarySearch(items, data[offset])) < 0) {
                nodeLocation.node = null;
                return;
            }

            final CompiledNode<T> entrynode = this.nodes[k];

            if(entrynode != null && entrynode.path != null) {
                if(offset+entrynode.path.length < data.length) {
                    int i = 0;

                    offset+= 1;

                    for(; i < entrynode.path.length && data[offset+i] == entrynode.path[i]; i++) {}

                    if(i != entrynode.path.length) {
                        nodeLocation.node = null;
                        nodeLocation.delta = 1;
                    }
                    else {
                        nodeLocation.node = entrynode;
                        nodeLocation.delta = 1 + entrynode.path.length;
                    }

                    return;
                }
            } else if(entrynode != null) {
                nodeLocation.node = entrynode;
                nodeLocation.delta = 1;
                return;
            }

            nodeLocation.node = null;
        }

        @Override
        protected boolean isOutput() {
            return false;
        }

        @Override
        protected OutputNode<T> output() {
            throw new UnsupportedOperationException();
        }
    }

    private static class CompiledOutputNode<T> extends CompiledNode<T> implements OutputNode<T> {
        private T item;

        public CompiledOutputNode(T item) {
            this.item = item;
        }

        @Override
        protected boolean isOutput() {
            return true;
        }

        @Override
        protected OutputNode<T> output() {
            return this;
        }

        @Override
        public T value() {
            return item;
        }
    }

    private Node root;

    public static class Entry<T> implements Map.Entry<String,T>, Comparable<Entry> {
        private String str;
        private T item;

        public Entry(String str, T item) {
            this.str = str;
            this.item = item;
        }

        public String getKey() {
            return str;
        }

        public T getValue() {
            return item;
        }

        public T setValue(T value) {
            T oldItem = item;
            this.item = value;
            return oldItem;
        }

        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;

            Entry entry = (Entry) o;

            if (!str.equals(entry.str)) return false;
            return item != null ? item.equals(entry.item) : entry.item == null;
        }

        public int hashCode() {
            int result = str.hashCode();
            result = 31 * result + (item != null ? item.hashCode() : 0);
            return result;
        }

        public int compareTo(Entry o) {
            return str.compareTo(o.str);
        }
    }

    @SuppressWarnings("unchecked")
    private IndexedOutputNode insert(String key) {
        if(key.length() == 0)
            throw new IllegalArgumentException("Key has zero length.");

        if(this.root == null) {
            this.root = new IndexedNode((char)0,null);
        }

        Node current = this.root;
        for(int i = 0; i < key.length(); i++) {
            current = current.get(key.charAt(i));
        }

        if(current.isOutput())
            throw new UnsupportedOperationException("Duplicate key: " + key);

        return (IndexedOutputNode)current.output();
    }

    @SuppressWarnings("unchecked")
    private void compile() {
        CompiledNode root = new CompiledNode();
        if(this.root == null)
            return;

        root.items = new char[((IndexedNode)this.root).index.size()];
        root.nodes = new CompiledNode[root.items.length];

        int i = 0;
        for (Char2ObjectMap.Entry<IndexedNode<T>> entry : ((IndexedNode<T>) this.root).index.char2ObjectEntrySet()) {
            IntStack position = new IntArrayList();
            ArrayDeque<Iterator<Char2ObjectMap.Entry<IndexedNode<T>>>> items = new ArrayDeque<>();
            ArrayDeque<CompiledNode> currentNode = new ArrayDeque<>();

            root.items[i] = entry.getCharKey();

            IndexedNode childNode = entry.getValue();
            CompiledNode workNode;

            if(childNode.isOutput()) {
                workNode = new CompiledOutputNode(childNode.output().value());
            } else {
                workNode = new CompiledNode();
            }

            root.nodes[i] = workNode;

            if(!childNode.index.isEmpty()) {
                workNode.items = new char[childNode.index.size()];
                workNode.nodes = new CompiledNode[childNode.index.size()];

                position.push(0);
                currentNode.push(workNode);
                items.push(childNode.index.char2ObjectEntrySet().iterator());

                while(!position.isEmpty()) {
                    Iterator<Char2ObjectMap.Entry<IndexedNode<T>>> peek = items.peek();
                    CompiledNode cnode = currentNode.peek();
                    int k = position.topInt();

                    if (peek.hasNext()) {
                        //Has something
                        Char2ObjectMap.Entry<IndexedNode<T>> next = peek.next();
                        cnode.items[k] = next.getCharKey();

                        if(next.getValue().isOutput()) {
                            cnode.nodes[k] = new CompiledOutputNode(next.getValue().output().value());
                        } else {
                            cnode.nodes[k] = new CompiledNode();
                        }

                        //Update position
                        position.popInt();
                        position.push(k+1);

                        //Go down a level
                        IndexedNode<T> inode = next.getValue();
                        if(!inode.index.isEmpty()) {
                            position.push(0);
                            currentNode.push(cnode.nodes[k]);
                            items.push(inode.index.char2ObjectEntrySet().iterator());

                            cnode.nodes[k].items = new char[inode.index.size()];
                            cnode.nodes[k].nodes = new CompiledNode[inode.index.size()];
                        }
                    } else {
                        //Node is completed.
                        items.pop();
                        position.popInt();
                        currentNode.pop();
                    }
                }
            }

            i++;
        }

        this.root = root;

        //Path compress - dfs search and when nb branches == 1 then path compress
        ArrayDeque<CompiledNode> path = new ArrayDeque<>();
        ArrayDeque<CompiledNode> partialpath = new ArrayDeque<>();

        IntStack branchidx = new IntArrayList();
        ArrayDeque<CompiledNode> branchpoint = new ArrayDeque<>();

        IntStack position = new IntArrayList();

        if(root.nodes.length > 0) {
            branchpoint.push(root);
            branchidx.push(0);

            path.push(root);

            while(!branchpoint.isEmpty()) {
                CompiledNode topNode = path.pop();

                if(topNode == branchpoint.peek()) {
                    int pos = branchidx.topInt();
                    if(pos >= topNode.items.length) {
                        branchidx.popInt();
                        branchpoint.pop();
                    } else {
                        path.push(topNode);
                        path.push(topNode.nodes[pos]);
                        branchidx.push(branchidx.popInt()+1);
                    }
                } else {
                    if(topNode.isOutput()) {
                        //Compile partial path
                        if(partialpath.size() > 0) {
                            char[] cpath = new char[partialpath.size()];
                            int q = 0;

                            Iterator<CompiledNode> iter = partialpath.descendingIterator();
                            while(iter.hasNext()) {
                                cpath[q++] = iter.next().items[0];
                            }

                            branchpoint.peek().nodes[branchidx.topInt()-1] = topNode;
                            topNode.path = cpath;

                            partialpath.clear();
                        }

                        if(topNode.nodes != null) {
                            branchpoint.push(topNode);
                            branchidx.push(0);
                            path.push(topNode);
                        }
                    } else {
                        if(topNode.nodes.length > 1) {
                            //Compile partial path
                            if(partialpath.size() > 0) {
                                char[] cpath = new char[partialpath.size()];
                                int q = 0;

                                Iterator<CompiledNode> iter = partialpath.descendingIterator();
                                while(iter.hasNext()) {
                                    cpath[q++] = iter.next().items[0];
                                }

                                branchpoint.peek().nodes[branchidx.topInt()-1] = topNode;
                                topNode.path = cpath;

                                partialpath.clear();
                            }

                            branchpoint.push(topNode);
                            branchidx.push(0);
                            path.push(topNode);
                        } else {
                            partialpath.push(topNode);
                            path.push(topNode.nodes[0]);
                        }
                    }
                }
            }
        }


    }

    public void build(List<Entry<T>> entries) {
        Collections.sort(entries);

        for (Entry<T> entry : entries) {
            IndexedOutputNode outputNode = insert(entry.getKey());
            outputNode.output = entry.item;
        }

        if(!entries.isEmpty()) {
            compile();
        }

        /*ArrayDeque<Node> current = new ArrayDeque<Node>();
        root = new Node();*/
    }

    public static class Match<T> {
        public final int start;
        public final int end;
        public final T item;

        public Match(int start, int end, T item) {
            this.start = start;
            this.end = end;
            this.item = item;
        }

        @Override
        public String toString() {
            return "Match{" +
                    "start=" + start +
                    ", end=" + end +
                    ", item=" + item +
                    '}';
        }
    }

    private class NodeOutput {
        public OutputNode<T> node=null;
        public int start=-1;
        public int end=-1;

        public void copyFrom(NodeOutput output) {
            this.node = output.node;
            this.start = output.start;
            this.end = output.end;
        }

        public int length() {
            return end-start;
        }
    }

    private class ForwardIterator {
        final char[] chars;
        final int i;
        int j;
        Node currentNode;
        NodeLocation nodeLocation;

        public ForwardIterator(char[] chars, int i, NodeLocation nodeLocation) {
            this.chars = chars;
            this.i = i;
            this.j = i;
            this.currentNode = CharTrie.this.root;
            this.nodeLocation = nodeLocation;
        }

        public final boolean next(final NodeOutput output) {
            if(currentNode == null)
                return false;

            while(j < chars.length) {
                currentNode.find(nodeLocation, chars, j);
                currentNode = nodeLocation.node;

                if(currentNode == null)
                    return false;

                if(currentNode.isOutput()) {
                    output.node = currentNode.output();
                    output.start = i;
                    output.end = j + nodeLocation.delta;
                    j += nodeLocation.delta;
                    return true;
                }

                j += nodeLocation.delta;
            }

            return false;
        }
    }

    public Consumer<CharTrie.Match<T>> listCollector(List<CharTrie.Match<T>> matches) {
        return matches::add;
    }

    public final void findLongestDominantRight(String text, Consumer<Match<T>> consumer) {
        final char[] chars = text.toCharArray();
        if(this.root == null)
            return;

        NodeLocation nodeLocation = new NodeLocation();
        NodeOutput longest = new NodeOutput();
        NodeOutput current = new NodeOutput();

        for (int i = 0; i < chars.length; i++) {
            final ForwardIterator iterator = new ForwardIterator(chars, i, nodeLocation);
            while(iterator.next(current)) {
                if(longest.node == null)
                    longest.copyFrom(current);
                else {
                    if(current.start >= longest.end)
                    {
                        consumer.accept(new Match<>(longest.start, longest.end, longest.node.value()));
                        longest.copyFrom(current);
                    }
                    else if(current.length() >= longest.length()) {
                        longest.copyFrom(current);
                    }
                }
            }
        }

        if(longest.node != null) {
            consumer.accept(new Match<>(longest.start, longest.end, longest.node.value()));
        }
    }

    public final void find(String text, Consumer<Match<T>> consumer) {
        final char[] chars = text.toCharArray();
        if(this.root == null)
            return;

        NodeOutput current = new NodeOutput();
        NodeLocation nodeLocation = new NodeLocation();
        for (int i = 0; i < chars.length; i++) {
            final ForwardIterator iterator = new ForwardIterator(chars, i, nodeLocation);
            while(iterator.next(current)) {
                consumer.accept(new Match<>(current.start,current.end, current.node.value()));
            }
        }
    }
}
