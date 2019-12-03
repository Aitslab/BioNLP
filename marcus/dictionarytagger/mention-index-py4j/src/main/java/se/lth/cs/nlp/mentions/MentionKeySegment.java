package se.lth.cs.nlp.mentions;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Found segments.
 */
public class MentionKeySegment {
    public int start;
    public int end;
    public String[] ids;
    public List<MentionTerm> terms;

    public MentionKeySegment(int start, int end, String[] ids) {
        this.start = start;
        this.end = end;
        this.ids = ids;
    }

    @Override
    public String toString() {
        return "Segment{" +
                "start=" + start +
                ", end=" + end +
                ", ids=[" + Arrays.stream(ids).collect(Collectors.joining(", ")) + "] " +
                '}';
    }
}
