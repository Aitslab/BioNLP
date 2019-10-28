package se.lth.cs.nlp.mentions;

import org.apache.lucene.util.AttributeImpl;
import org.apache.lucene.util.AttributeReflector;

/**
 * Created by csz-mkg on 2017-06-07.
 */
public class MentionTypeAttributeImpl extends AttributeImpl implements MentionTypeAttribute {
    private Sym sym;

    public Sym getSym() {
        return sym;
    }

    public void setSym(Sym sym) {
        this.sym = sym;
    }

    @Override
    public void clear() {
        sym = Sym.UNKNOWN;
    }

    @Override
    public void reflectWith(AttributeReflector reflector) {
        reflector.reflect(MentionTypeAttribute.class, "sym", sym);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        MentionTypeAttributeImpl that = (MentionTypeAttributeImpl) o;

        return sym == that.sym;
    }

    @Override
    public int hashCode() {
        return sym != null ? sym.hashCode() : 0;
    }

    @Override
    public void copyTo(AttributeImpl target) {
        ((MentionTypeAttributeImpl)target).sym = sym;
    }
}
