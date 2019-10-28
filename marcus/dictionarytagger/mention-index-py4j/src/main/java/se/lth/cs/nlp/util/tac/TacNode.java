package se.lth.cs.nlp.util.tac;

import it.unimi.dsi.fastutil.ints.IntArrayList;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Iterator;

public abstract class TacNode {
    protected int index;
    protected TacDocument parent;
    protected int start;
    protected int end;

    public TacNode(TacDocument parent, int start, int end) {
        this.parent = parent;
        this.start = start;
        this.end = end;
    }

    public int getStart() {
        return start;
    }

    public int getEnd() {
        return end;
    }

    public abstract String text();

    @Override
    public String toString() {
        return "TacNode{text=" + text() + "}";
    }
}
