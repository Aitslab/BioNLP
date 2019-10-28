package se.lth.cs.nlp.mentions;

import java.util.List;

/**
 * Found segments.
 */
public class MentionSegment {
    public int start;
    public int end;
    public long value;
    public List<MentionTerm> terms;

    public MentionSegment(int start, int end, long value) {
        this.start = start;
        this.end = end;
        this.value = value;
    }

    @Override
    public String toString() {
        return "Segment{" +
                "start=" + start +
                ", end=" + end +
                ", value=" + value +
                '}';
    }
}
