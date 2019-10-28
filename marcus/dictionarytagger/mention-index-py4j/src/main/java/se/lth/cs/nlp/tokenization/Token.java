package se.lth.cs.nlp.tokenization;

import se.lth.cs.nlp.mentions.Sym;

import java.util.Objects;

public class Token {
    public final Segment segment;
    public int index;
    public final int start;
    public final int end;
    public final String value;
    public final String raw;
    public final Sym rawtype;

    public Token(Segment segment, int start, int end, String value, String raw, Sym rawtype) {
        this.segment = segment;
        this.start = start;
        this.end = end;
        this.value = value;
        this.raw = raw;
        this.rawtype = rawtype;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (o == null || getClass() != o.getClass())
            return false;

        Token token = (Token) o;

        if (index != token.index)
            return false;
        if (start != token.start)
            return false;
        if (end != token.end)
            return false;
        if (!Objects.equals(segment, token.segment))
            return false;
        if (!value.equals(token.value))
            return false;
        if (!rawtype.equals(token.rawtype))
            return false;
        return raw.equals(token.raw);
    }

    @Override
    public int hashCode() {
        int result = Objects.hashCode(segment);
        result = 31 * result + index;
        result = 31 * result + start;
        result = 31 * result + end;
        result = 31 * result + value.hashCode();
        result = 31 * result + raw.hashCode();
        result = 31 * result + rawtype.hashCode();
        return result;
    }

    @Override
    public String toString() {
        return "Token{" + "segment=" + segment + ", index=" + index + ", start=" + start + ", end=" + end + ", " +
                "value='" + value + '\'' + ", raw='" + raw + '\'' + ", rawtype=" + rawtype + '}';
    }
}
