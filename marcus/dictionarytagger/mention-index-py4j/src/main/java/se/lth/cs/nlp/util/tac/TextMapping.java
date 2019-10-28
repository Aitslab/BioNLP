package se.lth.cs.nlp.util.tac;

import it.unimi.dsi.fastutil.ints.Int2IntAVLTreeMap;
import it.unimi.dsi.fastutil.ints.IntArrayList;
import it.unimi.dsi.fastutil.ints.IntListIterator;

import java.util.ArrayList;

public class TextMapping {
    private final Int2IntAVLTreeMap offsets = new Int2IntAVLTreeMap();
    private final StringBuilder sb = new StringBuilder();

    public String text(int start, int end) {
        return sb.substring(start, end);
    }

    public String text() {
        return sb.toString();
    }

    public void append(int offset, String text) {
        if(sb.length() == 0) {
            offsets.put(0, offset);
        }

        int targetoffset = sb.length();
        offsets.put(targetoffset, offset);
        sb.append(text);
    }

    public int translate(int offset) {
        if(this.offsets.containsKey(offset)) {
            return this.offsets.get(offset);
        } else {
            int lastkey = this.offsets.headMap(offset).lastIntKey();
            int rel = this.offsets.get(lastkey);
            return rel + offset-lastkey;
        }
    }

    public IntArrayList translate(IntArrayList offsets) {
        if(offsets.isEmpty()) {
            return offsets;
        }

        IntArrayList output = new IntArrayList(offsets.size());

        IntListIterator iter = offsets.iterator();
        while(iter.hasNext()) {
            int offset = iter.nextInt();
            output.add(translate(offset));
        }

        return output;
    }
}
