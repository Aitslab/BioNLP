package se.lth.cs.nlp.mentions;

import it.unimi.dsi.fastutil.ints.IntArrayList;
import it.unimi.dsi.fastutil.ints.IntIterator;
import org.apache.lucene.analysis.TokenFilter;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.apache.lucene.analysis.tokenattributes.OffsetAttribute;

import java.io.IOException;
import java.nio.CharBuffer;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by csz-mkg on 2017-08-11.
 */
public class ChineseMentionFilterExpansion  extends TokenFilter {
    public ChineseMentionFilterExpansion(TokenStream input) {
        super(input);
    }

    private final CharTermAttribute termAtt = addAttribute(CharTermAttribute.class);
    private final OffsetAttribute offsetAtt = addAttribute(OffsetAttribute.class);
    private final StringBuilder buffer = new StringBuilder();

    IntIterator posIterator = null;
    Iterator<String> tokenIterator = null;

    @Override
    public void reset() throws IOException {
        super.reset();
        posIterator = null;
        tokenIterator = null;
    }

    Pattern pattern = Pattern.compile("\\p{IsHan}");


    @Override
    public final boolean incrementToken() throws IOException {
        if(tokenIterator != null) {
            if(tokenIterator.hasNext()) {
                termAtt.setEmpty();
                termAtt.append(tokenIterator.next());
                int startOffset = posIterator.nextInt();
                int endOffset = posIterator.nextInt();
                offsetAtt.setOffset(startOffset, endOffset);
                return true;
            } else {
                tokenIterator = null;
                posIterator = null;
            }
        }

        if(this.input.incrementToken()) {
            char[] buffer = termAtt.buffer();
            if(termAtt.length() > 1 && pattern.matcher(java.nio.CharBuffer.wrap(buffer, 0, termAtt.length())).find()) {

                final int offset = offsetAtt.startOffset();

                List<String> parts = new ArrayList<>();
                IntArrayList positions = new IntArrayList();
                Matcher matcher = pattern.matcher(CharBuffer.wrap(buffer, 0, termAtt.length()));
                int last = 0;
                while(matcher.find()) {
                    if(last < matcher.start()) {
                        positions.add(offset+last);
                        positions.add(offset+matcher.start());
                        parts.add(new String(buffer, last, matcher.start()-last));
                    }

                    positions.add(offset+matcher.start());
                    positions.add(offset+matcher.end());
                    parts.add(new String(buffer, matcher.start(), matcher.end()-matcher.start()));

                    last = matcher.end();
                }

                if(last < termAtt.length()) {
                    positions.add(offset+last);
                    positions.add(offset+termAtt.length());
                    parts.add(new String(buffer, last, termAtt.length()-last));
                }

                tokenIterator = parts.iterator();
                posIterator = positions.iterator();

                termAtt.setEmpty();
                termAtt.append(tokenIterator.next());
                int startOffset = posIterator.nextInt();
                int endOffset = posIterator.nextInt();
                offsetAtt.setOffset(startOffset, endOffset);
            }
            return true;
        } else {
            return false;
        }
    }


}
