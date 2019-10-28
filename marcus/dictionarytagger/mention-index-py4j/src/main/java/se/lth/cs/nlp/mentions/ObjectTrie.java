package se.lth.cs.nlp.mentions;

import it.unimi.dsi.fastutil.objects.Object2ObjectMap;
import it.unimi.dsi.fastutil.objects.Object2ObjectRBTreeMap;

import java.util.*;
import java.util.function.Consumer;

/**
 * Char Trie implementation
 */
public class ObjectTrie<K extends Comparable<K>,T> {
    private static class NodeLocation {
        public Node node;
        public int delta;
    }

    private static abstract class Node<K, T> {
        protected abstract Node get(K item);

        protected abstract Node find(K item);

        protected void find(NodeLocation nodeLocation, K[] data, int offset) {
            Node node = find(data[offset]);
            nodeLocation.node = node;
            nodeLocation.delta = 1;
        }

        protected abstract boolean isOutput();

        protected abstract OutputNode output();
    }

    private static class IndexedNode<K,T> extends Node<K,T> {
        public K key;
        public IndexedNode parent;
        public Object2ObjectRBTreeMap<K,IndexedNode<K,T>> index = new Object2ObjectRBTreeMap<>();

        public IndexedNode(K key, IndexedNode<K,T> parent) {
            this.key = key;
            this.parent = parent;
        }

        protected final Node get(K key) {
            IndexedNode<K,T> node = index.get(key);
            if(node == null) {
                node = new IndexedNode<>(key, this);
                index.put(key, node);
            }
            return node;
        }

        protected final Node find(K key) {
            return index.get(key);
        }

        protected boolean isOutput() {
            return false;
        }

        protected OutputNode<K,T> output() {
            IndexedOutputNode<K,T> outNode = new IndexedOutputNode<>(key, parent);
            outNode.index = index;

            for (Object2ObjectMap.Entry<K,IndexedNode<K,T>> entry : outNode.index.object2ObjectEntrySet()) {
                entry.getValue().parent = outNode;
            }

            this.parent.index.put(key, outNode);
            return outNode;
        }


        @Override
        public String toString() {
            return "IndexedNode{" +
                    "key=" + Objects.toString(key) +
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

    private interface OutputNode<K,T> {
        T value();
    }

    private static class IndexedOutputNode<K,T> extends IndexedNode<K,T> implements OutputNode<K,T> {
        public T output;

        public IndexedOutputNode(K key, IndexedNode<K,T> parent) {
            super(key, parent);
            this.output = null;
        }

        @Override
        protected boolean isOutput() {
            return true;
        }

        @Override
        protected OutputNode<K,T> output() {
            return this;
        }

        @Override
        public T value() {
            return this.output;
        }

        @Override
        public String toString() {
            return "OutputNode{" +
                    "key=" + Objects.toString(key) +
                    "output=" + output +
                    '}';
        }
    }

    private Node root;

    public static class Entry<K extends Comparable<K>,T> implements Map.Entry<K[],T>, Comparable<Entry<K,T>> {
        private K[] key;
        private T item;

        public Entry(K[] key, T item) {
            this.key = key;
            this.item = item;
        }

        public K[] getKey() {
            return key;
        }

        public T getValue() {
            return item;
        }

        public T setValue(T value) {
            T oldItem = item;
            this.item = value;
            return oldItem;
        }

        @Override
        public int hashCode() {
            return super.hashCode();
        }

        @Override
        public boolean equals(Object obj) {
            return super.equals(obj);
        }

        @Override
        public int compareTo(Entry<K,T> o) {
            Objects.requireNonNull(o);
            int res = 0;
            int i = 0;
            int cnt = Math.min(key.length, o.key.length);
            while(res == 0 && i < cnt) {
                res = key[i].compareTo(o.key[i]);
                i++;
            }

            if(res != 0) {
                return res;
            } else {
                return Integer.compare(key.length, o.key.length);
            }
        }
    }

    @SuppressWarnings("unchecked")
    private IndexedOutputNode insert(K[] key) {
        if(key.length == 0)
            throw new IllegalArgumentException("Key has zero length.");

        if(this.root == null) {
            this.root = new IndexedNode((char)0,null);
        }

        Node current = this.root;
        for(int i = 0; i < key.length; i++) {
            current = current.get(key[i]);
        }

        if(current.isOutput())
            throw new UnsupportedOperationException("Duplicate key: " + Arrays.toString(key));

        return (IndexedOutputNode)current.output();
    }

    /*
    @SuppressWarnings("unchecked")
    private void compile() {
        CompiledNode root = new CompiledNode();
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
    }*/

    public void build(List<Entry<K,T>> entries) {
        Collections.sort(entries);

        for (Entry<K,T> entry : entries) {
            IndexedOutputNode outputNode = insert(entry.getKey());
            outputNode.output = entry.item;
        }

        //compile();

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
        public OutputNode<K,T> node=null;
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
        final K[] keys;
        final int i;
        int j;
        Node currentNode;
        NodeLocation nodeLocation;

        public ForwardIterator(K[] keys, int i, NodeLocation nodeLocation) {
            this.keys = keys;
            this.i = i;
            this.j = i;
            this.currentNode = ObjectTrie.this.root;
            this.nodeLocation = nodeLocation;
        }

        public final boolean next(final NodeOutput output) {
            if(currentNode == null)
                return false;

            while(j < keys.length) {
                currentNode.find(nodeLocation, keys, j);
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

    public Consumer<Match<T>> listCollector(List<Match<T>> matches) {
        return matches::add;
    }

    public final void findLongestDominantRight(K[] objects, Consumer<Match<T>> consumer) {
        if(this.root == null)
            return;

        NodeLocation nodeLocation = new NodeLocation();
        NodeOutput longest = new NodeOutput();
        NodeOutput current = new NodeOutput();

        for (int i = 0; i < objects.length; i++) {
            final ForwardIterator iterator = new ForwardIterator(objects, i, nodeLocation);
            while(iterator.next(current)) {
                if(longest.node == null)
                    longest.copyFrom(current);
                else {
                    if(current.start >= longest.end)
                    {
                        consumer.accept(new Match<>(longest.start, longest.end, longest.node.value()));
                        longest.copyFrom(current);
                    }
                    else if(current.start <= longest.end && current.length() >= longest.length()) {
                        longest.copyFrom(current);
                    }
                }
            }
        }

        if(longest.node != null) {
            consumer.accept(new Match<>(longest.start, longest.end, longest.node.value()));
        }
    }

    public final void find(K[] objects, Consumer<Match<T>> consumer) {
        if(this.root == null)
            return;

        NodeOutput current = new NodeOutput();
        NodeLocation nodeLocation = new NodeLocation();
        for (int i = 0; i < objects.length; i++) {
            final ForwardIterator iterator = new ForwardIterator(objects, i, nodeLocation);
            while(iterator.next(current)) {
                consumer.accept(new Match<>(current.start,current.end, current.node.value()));
            }
        }
    }
}
