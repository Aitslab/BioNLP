package se.lth.cs.nlp.util.tac;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.Objects;
import java.util.stream.Stream;

public class TacElement extends TacNode implements Iterable<TacNode> {
    private String name;
    public ArrayList<TacAttribute> attributes = new ArrayList<>();
    protected ArrayList<TacNode> children = new ArrayList<>();

    public TacElement(TacDocument parent, int start, int end, String name) {
        super(parent, start, end);
        this.name = name;
    }

    @Override
    public String text() {
        StringBuilder sb = new StringBuilder();

        for (TacNode child : children) {
            if(child != null) {
                sb.append(child.text());
            }
        }

        return sb.toString();
    }

    public void add(TacNode node) {
        node.index = this.children.size();
        this.children.add(node);
    }

    public void remove(TacNode node) {
        children.set(node.index, null);
    }

    public String name() {
        return name;
    }

    public void add(TacAttribute attr) {
        this.attributes.add(attr);
    }

    public Stream<TacAttribute> attributes() {
        return attributes.stream();
    }

    @Override
    public Iterator<TacNode> iterator() {
        return children.stream().filter(Objects::nonNull).iterator();
    }

    @Override
    public String toString() {
        return "TacElement{" + "name='" + name + '\'' + ", attributes=" + attributes + ", children=" + children + '}';
    }
}
