package se.lth.cs.nlp.mentions;

import org.apache.lucene.analysis.Analyzer;

import java.io.Externalizable;
import java.io.IOException;
import java.io.ObjectInput;
import java.io.ObjectOutput;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Created by csz-mkg on 2017-06-08.
 */
public class MentionPipeline implements Externalizable {
    private String lang;
    private Analyzer analyzer;

    public MentionPipeline(String lang) {
        this.lang = lang;
        this.analyzer = MentionAnalyzerPipelines.get(lang);
    }

    public MentionPipeline() {

    }

    public List<MentionTerm> tokenize(String text) {
        try {
            return Mentions.tokenize(analyzer, text);
        } catch (Throwable e) {
            throw new RuntimeException("Could not tokenize '" + text + "'", e);
        }
    }

    public String normalize(String text) {
        return tokenize(text).stream().map(term -> term.term).collect(Collectors.joining(" "));
    }

    public void writeExternal(ObjectOutput out) throws IOException {
        out.writeUTF(lang);
    }

    public void readExternal(ObjectInput in) throws IOException {
        this.lang = in.readUTF();
        this.analyzer = MentionAnalyzerPipelines.get(this.lang);
    }
}
