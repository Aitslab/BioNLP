package se.lth.cs.nlp.mentions;

import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.util.TokenFilterFactory;

import java.util.Map;

/**
 * Created by marcus on 2017-06-13.
 */
public class AccentRemovalFilterFactory extends TokenFilterFactory {
    public AccentRemovalFilterFactory(Map<String, String> args) {
        super(args);
    }

    @Override
    public TokenStream create(TokenStream tokenStream) {
        return new AccentRemovalFilter(tokenStream);
    }

}
