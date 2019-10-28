package se.lth.cs.nlp.mentions;

import org.apache.lucene.util.Attribute;

/**
 * Created by csz-mkg on 2017-06-07.
 */
public interface MentionTypeAttribute extends Attribute {
    Sym getSym();

    void setSym(Sym sym);
}
