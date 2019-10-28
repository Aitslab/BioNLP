package se.lth.cs.nlp.mentions;

import org.apache.commons.lang3.StringUtils;
import org.apache.lucene.analysis.TokenFilter;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;

import java.io.IOException;
import java.text.Normalizer;
import java.util.regex.Pattern;

/**
 * Created by marcus on 2017-06-08.
 */
public class AccentRemovalFilter extends TokenFilter {
    public AccentRemovalFilter(TokenStream input) {
        super(input);
    }

    private final CharTermAttribute termAtt = addAttribute(CharTermAttribute.class);

    @Override
    public final boolean incrementToken() throws IOException {
        if(this.input.incrementToken()) {
            this.termAtt.setEmpty().append(StringUtils.stripAccents(new String(termAtt.buffer(), 0, termAtt.length())));
            return true;
        } else {
            return false;
        }
    }
}
