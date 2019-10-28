package se.lth.cs.nlp.util.tac;

import java.util.Objects;

public class TacAttribute {
    private TacNode name;
    private TacNode value;

    public TacAttribute(TacNode name, TacNode value) {
        this.name = name;
        this.value = value;
    }

    public TacNode getName() {
        return name;
    }

    public TacNode getValue() {
        return value;
    }

    @Override
    public String toString() {
        return "TacAttribute{" + "name=" + Objects.toString(name) + ", value=" + Objects.toString(value) + '}';
    }
}
