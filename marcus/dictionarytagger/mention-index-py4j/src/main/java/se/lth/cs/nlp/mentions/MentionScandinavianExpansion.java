package se.lth.cs.nlp.mentions;

import org.apache.lucene.analysis.TokenFilter;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.icu.ICUFoldingFilter;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;

import java.io.IOException;

/**
 * Created by marcus on 2017-06-08.
 */
public class MentionScandinavianExpansion extends TokenFilter {
    public MentionScandinavianExpansion(TokenStream input) {
        super(input);
    }

    private final CharTermAttribute termAtt = addAttribute(CharTermAttribute.class);
    private final StringBuilder buffer = new StringBuilder();

    private boolean quickCheck(char[] buffer, final int ln) {
        for(int i = 0; i < ln; i++) {
            switch (buffer[i]) {
                case 'å':
                case 'ä':
                case 'ö':
                case 'Å':
                case 'Ä':
                case 'Ö':
                case 'ø':
                case 'Ø':
                case 'æ':
                case 'Æ':
                    return true;
                default:
                    break;
            }
        }
        return false;
    }

    private void transform(char[] buffer, final int ln) {
        for(int i = 0; i < ln; i++) {
            switch (buffer[i]) {
                case 'å':
                    this.buffer.append("aa");
                    break;
                case 'ä':
                    this.buffer.append("ae");
                    break;
                case 'ö':
                    this.buffer.append("oe");
                    break;
                case 'Å':
                    this.buffer.append("AA");
                    break;
                case 'Ä':
                    this.buffer.append("AE");
                    break;
                case 'Ö':
                    this.buffer.append("OE");
                    break;
                case 'ø':
                    this.buffer.append("oe");
                    break;
                case 'Ø':
                    this.buffer.append("OE");
                    break;
                case 'æ':
                    this.buffer.append("ae");
                    break;
                case 'Æ':
                    this.buffer.append("AE");
                    break;
                default:
                    this.buffer.append(buffer[i]);
                    break;
            }
        }
    }

    @Override
    public final boolean incrementToken() throws IOException {
        if(this.input.incrementToken()) {
            char[] buffer = termAtt.buffer();
            if(quickCheck(buffer, termAtt.length())) {
                this.buffer.setLength(0);
                transform(buffer, termAtt.length());
                this.termAtt.setEmpty().append(this.buffer);
            }
            return true;
        } else {
            return false;
        }
    }
}
