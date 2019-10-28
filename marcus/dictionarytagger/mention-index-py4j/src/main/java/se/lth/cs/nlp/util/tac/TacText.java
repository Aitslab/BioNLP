package se.lth.cs.nlp.util.tac;

public class TacText extends TacNode {
    public String unescaped;

    public TacText(TacDocument parent, String unescaped, int start, int end) {
        super(parent, start, end);
        this.unescaped = unescaped;
    }

    public String text() {
        return this.unescaped;
    }

    @Override
    public String toString() {
        return "TacText{" + unescaped + "}";
    }
}
