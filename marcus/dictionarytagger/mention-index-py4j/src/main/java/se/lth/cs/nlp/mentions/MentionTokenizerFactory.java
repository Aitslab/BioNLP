package se.lth.cs.nlp.mentions;

import org.apache.lucene.analysis.Tokenizer;
import org.apache.lucene.analysis.util.TokenizerFactory;
import org.apache.lucene.util.AttributeFactory;

import java.util.Map;

/**
 * Created by csz-mkg on 2017-06-07.
 */
public class MentionTokenizerFactory extends TokenizerFactory {

    private final boolean includeWhitespace;

    public MentionTokenizerFactory(Map<String, String> args) {
        super(args);
        includeWhitespace = Boolean.valueOf(args.getOrDefault("include-whitespace", "false"));
    }

    @Override
    public Tokenizer create(AttributeFactory factory) {
        return new MentionTokenizer(factory, includeWhitespace);
    }
}
