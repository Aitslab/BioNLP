package se.lth.cs.nlp.util.tac;

/**
 * Created by marcus on 2017-05-09.
 */
public class Yytoken {
    public final int pos;
    public String data;
    public TacSym sym;
    public boolean terminated=false;

    public Yytoken(TacSym sym, int pos, String data) {
        this.sym = sym;
        this.pos = pos;
        this.data = data;
    }

    @Override
    public String toString() {
        return "Yytoken{" +
                "pos=" + pos +
                ", data='" + data + '\'' +
                ", sym=" + sym +
                '}';
    }
}
