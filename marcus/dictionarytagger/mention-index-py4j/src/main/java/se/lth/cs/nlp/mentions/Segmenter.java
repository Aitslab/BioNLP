package se.lth.cs.nlp.mentions;

import it.unimi.dsi.fastutil.ints.IntArrayList;

import java.io.IOError;
import java.io.IOException;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * Created by marcus on 2017-05-09.
 */
public class Segmenter {
    private IntArrayList segments = new IntArrayList();
    private ArrayList<Yytoken> tokens = new ArrayList<>();
    private String text;

    public Segmenter(String text) {
        this.text = text;
        segment(false);
    }

    public Segmenter(String text, boolean disableWordLimit) {
        this.text = text;
        segment(disableWordLimit);
    }

    public static List<Yytoken> withWhitespace(String text) {
        try {
            Tokenizer tokenizer = new Tokenizer(new StringReader(text));
            ArrayList<Yytoken> tokens = new ArrayList<>();

            Yytoken current;
            while((current = tokenizer.yylex()) != null) {
                tokens.add(current);
            }

            return tokens;
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    public static List<Yytoken> withoutWhitespace(String text) {
        try {
            Tokenizer tokenizer = new Tokenizer(new StringReader(text));
            ArrayList<Yytoken> tokens = new ArrayList<>();

            Yytoken current;
            while((current = tokenizer.yylex()) != null) {
                switch (current.sym) {
                    case NEWLINE:
                    case WHITESPACE:
                    case CONTROL_CODES:
                        break;
                    default:
                        tokens.add(current);
                        break;
                }
            }

            return tokens;
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    private Yytoken sym(int k) {
        if(k < 0)
            return new Yytoken(Sym.WHITESPACE, -1, "");

        if(k >= tokens.size())
            return new Yytoken(Sym.WHITESPACE, -1, "");

        return tokens.get(k);
    }

    private static class RuleContext {
        public int k;
        public boolean star;
    }

    private interface Rule {
        boolean test(RuleContext ctx, Yytoken yytoken);
    }

    private Rule matches(Sym...syms) {
        return (ctx, token) -> {
            if(Arrays.stream(syms).anyMatch(sym -> token.sym == sym)) {
                ctx.k += 1;
                return true;
            } else {
                return false;
            }
        };
    }

    private Rule optional(Sym...syms) {
        return (ctx, token) -> {
            if(Arrays.stream(syms).anyMatch(sym -> token.sym == sym)) {
                ctx.k += 1;
            }

            return  true;
        };
    }

    private Rule optional_star(Sym...syms) {
        return (ctx, token) -> {
            if(Arrays.stream(syms).anyMatch(sym -> token.sym == sym)) {
                ctx.k += 1;
                ctx.star = true;
            }
            else
                return !ctx.star;

            return  true;
        };
    }

    private boolean rule(int k, Rule...rules) {
        RuleContext ctx = new RuleContext();
        ctx.k = k;
        int i = 0;
        while(i < rules.length && k < tokens.size()) {
            if(!rules[i].test(ctx, sym(ctx.k))) {
                return false;
            }
            else {
                 while(ctx.star && ctx.k < tokens.size() && rules[i].test(ctx, sym(ctx.k)));

                 ctx.star = false;
            }
            i += 1;
        }

        return true;
    }

    public List<Yytoken> rawTokenStream() {
        return tokens;
    }

    private void segment(boolean disableWordLimit) {
        Tokenizer tokenizer = new Tokenizer(new StringReader(text));
        Sym lastLastSym = Sym.NEWLINE;
        Sym lastSym = Sym.NEWLINE;

        Yytoken current;
        try {
            while((current = tokenizer.yylex()) != null) {
                current.idx = tokens.size();
                tokens.add(current);
            }
        } catch (IOException e) {
            throw new IOError(e);
        }

        int last = 0;
        int i = 0;
        int numwords = 0;

        for (int k = 0; k < tokens.size(); k++) {
            Sym sym = sym(k).sym;
            switch (sym) {
                case BANG:
                case SEMICOLON:
                case QUESTION:
                    if((disableWordLimit || numwords >= 4)
                            && rule(k+1,
                                   optional_star(Sym.WHITESPACE, Sym.NEWLINE),
                                   matches(Sym.WORD,
                                           Sym.WORD_TITLE_CASE,
                                           Sym.WORD_UPPER_CASE,
                                           Sym.WORD_MIXED_CASE_UPPER,
                                           Sym.WORD_ACRONYM,
                                           Sym.CITATION,
                                           Sym.NUMBER,
                                           Sym.ELISION_PREFIX,
                                           Sym.URL) )
                    ) {
                        segments.add(last);
                        segments.add(k+1);
                        last = k+1;
                        numwords = 0;
                    }
                    break;
                case PERIOD:
                    if(sym(k).data.equals("。")) {
                        segments.add(last);
                        segments.add(k+1);
                        last = k+1;
                        numwords = 0;
                    }
                    else {
                        if((disableWordLimit || numwords >= 4)
                                && rule(k+1, optional_star(Sym.WHITESPACE, Sym.NEWLINE),
                                        matches(Sym.WORD,
                                          Sym.WORD_TITLE_CASE,
                                          Sym.WORD_UPPER_CASE,
                                          Sym.WORD_MIXED_CASE_UPPER,
                                          Sym.WORD_ACRONYM,
                                          Sym.CITATION,
                                          Sym.NUMBER,
                                          Sym.ELISION_PREFIX,
                                          Sym.URL) ) ) {
                            segments.add(last);
                            segments.add(k+1);
                            last = k+1;
                            numwords = 0;
                        } else if((disableWordLimit || numwords >= 4) && rule(k+1, optional(Sym.WHITESPACE), matches(Sym.NEWLINE, Sym.NUMBER, Sym.URL)) ) {
                            segments.add(last);
                            segments.add(k+1);
                            last = k+1;
                            numwords = 0;
                        } else if((disableWordLimit || numwords >= 4) && rule(k+1, matches(Sym.NEWLINE, Sym.NUMBER, Sym.URL)) ) {
                            segments.add(last);
                            segments.add(k+1);
                            last = k+1;
                            numwords = 0;
                        }
                    }

                    break;
                case WORD:
                case WORD_ACRONYM:
                case WORD_INITIAL:
                case WORD_UPPER_CASE:
                case WORD_MIXED_CASE_LOWER:
                case WORD_MIXED_CASE_UPPER:
                case WORD_TITLE_CASE:
                case NUMBER:
                    numwords += 1;
                    break;
            }
        }

        if(last != tokens.size()) {
            segments.add(last);
            segments.add(tokens.size());
        }
    }

    public ArrayList<Segment> segments() {
        ArrayList<Segment> outsegments = new ArrayList<>();

        for (int i = 0; i < segments.size(); i += 2) {
            int start = segments.getInt(i);
            int end = segments.getInt(i+1);
            if(end-start == 0)
                continue;

            outsegments.add(new Segment(tokens, start, end));
        }

        return outsegments;
    }
}
