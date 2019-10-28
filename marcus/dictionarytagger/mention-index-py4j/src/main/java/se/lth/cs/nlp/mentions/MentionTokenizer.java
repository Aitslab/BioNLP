package se.lth.cs.nlp.mentions;

import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.apache.lucene.analysis.tokenattributes.CharTermAttributeImpl;
import org.apache.lucene.analysis.tokenattributes.OffsetAttribute;
import org.apache.lucene.analysis.tokenattributes.PositionIncrementAttribute;
import org.apache.lucene.util.AttributeFactory;

import java.io.IOException;

/**
 * Created by csz-mkg on 2017-06-07.
 */
public class MentionTokenizer extends org.apache.lucene.analysis.Tokenizer {
    private Tokenizer tokenizer;
    private CharTermAttributeImpl cta;

    /** Absolute maximum sized token */
    public static final int MAX_TOKEN_LENGTH_LIMIT = 1024 * 1024;

    private int skippedPositions;
    private int lastPosition;

    private final CharTermAttribute termAtt = addAttribute(CharTermAttribute.class);
    private final OffsetAttribute offsetAtt = addAttribute(OffsetAttribute.class);
    private final PositionIncrementAttribute posIncrAtt = addAttribute(PositionIncrementAttribute.class);
    private final MentionTypeAttribute mentionTypeAttribute = addAttribute(MentionTypeAttribute.class);
    private final boolean includeWhitespace;

    private void init() {
        this.tokenizer = new Tokenizer(input);
    }

    public MentionTokenizer(boolean includeWhitespace) {
        super();
        this.includeWhitespace = includeWhitespace;
        init();
    }

    public MentionTokenizer(AttributeFactory factory, boolean includeWhitespace) {
        super(factory);
        this.includeWhitespace = includeWhitespace;
        init();
    }

    @Override
    public final boolean incrementToken() throws IOException {
        clearAttributes();
        skippedPositions = 0;

        while(true) {
            Yytoken tokenType = tokenizer.yylex();

            if (tokenType == null) {
                return false;
            }

            switch (tokenType.sym) {
                case NEWLINE:
                case WHITESPACE:
                case CONTROL_CODES:
                    if(!includeWhitespace) {
                        continue;
                    }
                default:
                    if (tokenType.data.length() <= MAX_TOKEN_LENGTH_LIMIT) {
                        posIncrAtt.setPositionIncrement(skippedPositions + 1);
                        termAtt.append(tokenType.data);
                        final int start = tokenType.pos;
                        final int end = start + tokenType.data.length();
                        offsetAtt.setOffset(start, end);
                        lastPosition = end;
                        mentionTypeAttribute.setSym(tokenType.sym);
                        return true;
                    } else {
                        // When we skip a too-long term, we still increment the
                        // position increment
                        skippedPositions++;
                    }
                    break;
            }
        }
    }

    @Override
    public final void end() throws IOException {
        super.end();
        // set final offset
        offsetAtt.setOffset(lastPosition, lastPosition);
        // adjust any skipped tokens
        posIncrAtt.setPositionIncrement(posIncrAtt.getPositionIncrement()+skippedPositions);
    }

    @Override
    public void close() throws IOException {
        super.close();
        tokenizer.yyreset(input);
    }

    @Override
    public void reset() throws IOException {
        super.reset();
        this.clearAttributes();
        tokenizer.yyreset(input);
        skippedPositions = 0;
    }
}
