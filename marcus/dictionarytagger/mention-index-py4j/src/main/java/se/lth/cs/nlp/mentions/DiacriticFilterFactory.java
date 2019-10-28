package se.lth.cs.nlp.mentions;

import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.util.TokenFilterFactory;

import java.util.Map;

/**
 * Created by csz-mkg on 2017-06-13.
 */
public class DiacriticFilterFactory extends TokenFilterFactory {
    public DiacriticFilterFactory(Map<String, String> args) {
        super(args);
    }

    @Override
    public TokenStream create(TokenStream tokenStream) {
        return new DiacriticFilter(tokenStream);
    }

}