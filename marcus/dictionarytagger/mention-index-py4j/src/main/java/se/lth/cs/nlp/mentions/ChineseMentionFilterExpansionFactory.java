package se.lth.cs.nlp.mentions;

import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.util.TokenFilterFactory;

import java.util.Map;

/**
 * Created by marcus on 2017-06-08.
 */
public class ChineseMentionFilterExpansionFactory extends TokenFilterFactory {
    public ChineseMentionFilterExpansionFactory(Map<String, String> args) {
        super(args);
    }

    @Override
    public TokenStream create(TokenStream tokenStream) {
        return new ChineseMentionFilterExpansion(tokenStream);
    }

}
