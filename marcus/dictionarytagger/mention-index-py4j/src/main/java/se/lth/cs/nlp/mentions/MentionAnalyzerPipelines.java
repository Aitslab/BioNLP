package se.lth.cs.nlp.mentions;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.cjk.CJKWidthFilterFactory;
import org.apache.lucene.analysis.custom.CustomAnalyzer;
import org.apache.lucene.analysis.icu.ICUFoldingFilterFactory;
import org.apache.lucene.analysis.icu.ICUNormalizer2FilterFactory;
import org.apache.lucene.analysis.pattern.PatternTokenizerFactory;
import org.apache.lucene.analysis.snowball.SnowballPorterFilterFactory;
import org.apache.lucene.analysis.util.TokenizerFactory;

import java.io.IOError;
import java.io.IOException;

/**
 * Created by csz-mkg on 2017-06-07.
 */
public class MentionAnalyzerPipelines {
    public static Analyzer get(String lang) {
        return get(lang, MentionTokenizerFactory.class);
    }

    public static Analyzer getTabTokenized(String lang) {
        return get(lang, PatternTokenizerFactory.class, "pattern", "\\t");
    }

    public static Analyzer get(String lang, Class<? extends TokenizerFactory> tokenizer, String...params) {
        try {
            switch (lang) {
                case "null":
                    return CustomAnalyzer.builder()
                            .withTokenizer(PatternTokenizerFactory.class, "pattern", "\t")
                            .build();
                case "en":
                    return CustomAnalyzer.builder()
                                        .withTokenizer(tokenizer, params)
                                        .addTokenFilter(MentionScandinavianExpansionFactory.class)
                                        .addTokenFilter(SnowballPorterFilterFactory.class, "language", "English")
                                        .addTokenFilter(ICUFoldingFilterFactory.class)
                                        .build();
                case "en_exact":
                    return CustomAnalyzer.builder()
                                         .withTokenizer(tokenizer, params)
                                         .addTokenFilter(MentionScandinavianExpansionFactory.class)
                                         .addTokenFilter(ICUNormalizer2FilterFactory.class, "name", "nfkc", "mode", "decompose")
                                         .addTokenFilter(DiacriticFilterFactory.class)
                                         .addTokenFilter(SnowballPorterFilterFactory.class, "language", "English")
                                         .build();
                case "sv":
                    return CustomAnalyzer.builder()
                                         .withTokenizer(tokenizer, params)
                                         .addTokenFilter(MentionScandinavianExpansionFactory.class)
                                         .addTokenFilter(SnowballPorterFilterFactory.class, "language", "Swedish")
                                         .addTokenFilter(ICUFoldingFilterFactory.class)
                                         .build();
                case "sv_exact":
                    return CustomAnalyzer.builder()
                                         .withTokenizer(tokenizer, params)
                                         .addTokenFilter(MentionScandinavianExpansionFactory.class)
                                         .addTokenFilter(ICUNormalizer2FilterFactory.class, "name", "nfkc", "mode", "decompose")
                                         .addTokenFilter(DiacriticFilterFactory.class)
                                         .addTokenFilter(SnowballPorterFilterFactory.class, "language", "Swedish")
                                         .build();
                case "da":
                    return CustomAnalyzer.builder()
                                         .withTokenizer(tokenizer, params)
                                         .addTokenFilter(MentionScandinavianExpansionFactory.class)
                                         .addTokenFilter(SnowballPorterFilterFactory.class, "language", "Danish")
                                         .addTokenFilter(ICUFoldingFilterFactory.class)
                                         .build();
                case "da_exact":
                    return CustomAnalyzer.builder()
                                         .withTokenizer(tokenizer, params)
                                         .addTokenFilter(MentionScandinavianExpansionFactory.class)
                                         .addTokenFilter(ICUNormalizer2FilterFactory.class, "name", "nfkc", "mode", "decompose")
                                         .addTokenFilter(DiacriticFilterFactory.class)
                                         .addTokenFilter(SnowballPorterFilterFactory.class, "language", "Danish")
                                         .build();
                case "no":
                    return CustomAnalyzer.builder()
                                         .withTokenizer(tokenizer, params)
                                         .addTokenFilter(MentionScandinavianExpansionFactory.class)
                                         .addTokenFilter(SnowballPorterFilterFactory.class, "language", "Norwegian")
                                         .addTokenFilter(ICUFoldingFilterFactory.class)
                                         .build();
                case "no_exact":
                    return CustomAnalyzer.builder()
                                         .withTokenizer(tokenizer, params)
                                         .addTokenFilter(MentionScandinavianExpansionFactory.class)
                                         .addTokenFilter(ICUNormalizer2FilterFactory.class, "name", "nfkc", "mode", "decompose")
                                         .addTokenFilter(DiacriticFilterFactory.class)
                                         .addTokenFilter(SnowballPorterFilterFactory.class, "language", "Norwegian")
                                         .build();
                case "de":
                    return CustomAnalyzer.builder()
                                         .withTokenizer(tokenizer, params)
                                         .addTokenFilter(MentionScandinavianExpansionFactory.class)
                                         .addTokenFilter(SnowballPorterFilterFactory.class, "language", "German")
                                         .addTokenFilter(ICUFoldingFilterFactory.class)
                                         .build();
                case "de_exact":
                    return CustomAnalyzer.builder()
                                         .withTokenizer(tokenizer, params)
                                         .addTokenFilter(MentionScandinavianExpansionFactory.class)
                                         .addTokenFilter(ICUNormalizer2FilterFactory.class, "name", "nfkc", "mode", "decompose")
                                         .addTokenFilter(DiacriticFilterFactory.class)
                                         .addTokenFilter(SnowballPorterFilterFactory.class, "language", "German")
                                         .build();
                case "fr":
                    return CustomAnalyzer.builder()
                                         .withTokenizer(tokenizer, params)
                                         .addTokenFilter(MentionScandinavianExpansionFactory.class)
                                         .addTokenFilter(SnowballPorterFilterFactory.class, "language", "French")
                                         .addTokenFilter(ICUFoldingFilterFactory.class)
                                         .build();
                case "fr_exact":
                    return CustomAnalyzer.builder()
                                         .withTokenizer(tokenizer, params)
                                         .addTokenFilter(MentionScandinavianExpansionFactory.class)
                                         .addTokenFilter(ICUNormalizer2FilterFactory.class, "name", "nfkc", "mode", "decompose")
                                         .addTokenFilter(DiacriticFilterFactory.class)
                                         .addTokenFilter(SnowballPorterFilterFactory.class, "language", "French")
                                         .build();
                case "es":
                    return CustomAnalyzer.builder()
                                         .withTokenizer(tokenizer, params)
                                         .addTokenFilter(MentionScandinavianExpansionFactory.class)
                                         .addTokenFilter(SnowballPorterFilterFactory.class, "language", "Spanish")
                                         .addTokenFilter(ICUFoldingFilterFactory.class)
                                         .build();
                case "es_exact":
                    return CustomAnalyzer.builder()
                                         .withTokenizer(tokenizer, params)
                                         .addTokenFilter(MentionScandinavianExpansionFactory.class)
                                         .addTokenFilter(ICUNormalizer2FilterFactory.class, "name", "nfkc", "mode", "decompose")
                                         .addTokenFilter(DiacriticFilterFactory.class)
                                         .addTokenFilter(SnowballPorterFilterFactory.class, "language", "Spanish")
                                         .build();
                case "ru":
                    return CustomAnalyzer.builder()
                                         .withTokenizer(tokenizer, params)
                                         .addTokenFilter(MentionScandinavianExpansionFactory.class)
                                         .addTokenFilter(SnowballPorterFilterFactory.class, "language", "Russian")
                                         .addTokenFilter(ICUFoldingFilterFactory.class)
                                         .build();
                case "ru_exact":
                    return CustomAnalyzer.builder()
                                         .withTokenizer(tokenizer, params)
                                         .addTokenFilter(MentionScandinavianExpansionFactory.class)
                                         .addTokenFilter(ICUNormalizer2FilterFactory.class, "name", "nfkc", "mode", "decompose")
                                         .addTokenFilter(DiacriticFilterFactory.class)
                                         .addTokenFilter(SnowballPorterFilterFactory.class, "language", "Russian")
                                         .build();
                case "zh":
                    return CustomAnalyzer.builder()
                                         .withTokenizer(tokenizer, params)
                                         .addTokenFilter(CJKWidthFilterFactory.class)
                                         .addTokenFilter(ChineseMentionFilterExpansionFactory.class)
                                         .addTokenFilter(ICUFoldingFilterFactory.class)
                                         .build();
                case "zh_exact":
                    return CustomAnalyzer.builder()
                            .withTokenizer(tokenizer, params)
                            .addTokenFilter(ChineseMentionFilterExpansionFactory.class)
                            .addTokenFilter(ICUNormalizer2FilterFactory.class, "name", "nfkc", "mode", "decompose")
                            .build();
                default:
                    return CustomAnalyzer.builder()
                                         .withTokenizer(tokenizer, params)
                                         .addTokenFilter(ICUFoldingFilterFactory.class)
                                         .build();
            }
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

}
