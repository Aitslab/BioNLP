package se.lth.cs.nlp.mentions;

/**
 * Created by csz-mkg on 2017-06-08.
 */
public class MentionTerm {
    public final int start;
    public final int end;
    public final String term;
    public final String raw;
    public final Sym type;
    public final int idx;

    public MentionTerm(int start, int end, String term, String raw, Sym type) {
        this.start = start;
        this.end = end;
        this.term = term;
        this.raw = raw;
        this.type = type;
        this.idx = -1;
    }

    public MentionTerm(int start, int end, String term, String raw, Sym type, int idx) {
        this.start = start;
        this.end = end;
        this.term = term;
        this.raw = raw;
        this.type = type;
        this.idx = idx;
    }

    @Override
    public String toString() {
        return "MentionTerm{" + "start=" + start + ", end=" + end + ", term='" + term + '\'' + ", raw='" + raw + '\''
                + ", type=" + type + ", idx=" + idx + '}';
    }
}
