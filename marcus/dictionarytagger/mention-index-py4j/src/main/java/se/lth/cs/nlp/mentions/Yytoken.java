package se.lth.cs.nlp.mentions;

/**
 * Created by marcus on 2017-05-09.
 */
public class Yytoken {
    public final int pos;
    public int idx;
    public String data;
    public Sym sym;

    public Yytoken(Sym sym, int pos, String data) {
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
