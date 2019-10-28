package se.lth.cs.nlp.mentions;

import org.apache.lucene.analysis.TokenFilter;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;

import java.io.IOException;
import java.util.stream.IntStream;

/**
 * Created by csz-mkg on 2017-06-13.
 */
public class DiacriticFilter extends TokenFilter {
    private final CharTermAttribute termAtt = addAttribute(CharTermAttribute.class);
    private final StringBuilder buffer = new StringBuilder();

    public DiacriticFilter(TokenStream input) {
        super(input);
    }

    @Override
    public final boolean incrementToken() throws IOException {
        if(this.input.incrementToken()) {
            final char[] buffer = termAtt.buffer();
            final int length = termAtt.length();
            this.buffer.setLength(0);
            int i = 0;
            while(i < length) {
                Character.UnicodeBlock block;
                if(Character.isSurrogate(buffer[i])) {
                    int cp = Character.codePointAt(buffer, i, length);
                    block = Character.UnicodeBlock.of(cp);
                    if(!(block == null
                            || block.equals(Character.UnicodeBlock.COMBINING_DIACRITICAL_MARKS)
                            || block.equals(Character.UnicodeBlock.COMBINING_DIACRITICAL_MARKS_SUPPLEMENT)
                            || block.equals(Character.UnicodeBlock.CONTROL_PICTURES))) {
                        this.buffer.append(buffer, i, 2);
                    }
                    i += 2;
                } else {
                    block = Character.UnicodeBlock.of(buffer[i]);
                    if(!(block == null
                            || block.equals(Character.UnicodeBlock.COMBINING_DIACRITICAL_MARKS)
                            || block.equals(Character.UnicodeBlock.COMBINING_DIACRITICAL_MARKS_SUPPLEMENT)
                            || block.equals(Character.UnicodeBlock.CONTROL_PICTURES))) {
                        this.buffer.append(buffer[i]);
                    }
                    i++;
                }
            }

            this.termAtt.setEmpty().append(this.buffer);
            return true;
        } else {
            return false;
        }
    }
}
