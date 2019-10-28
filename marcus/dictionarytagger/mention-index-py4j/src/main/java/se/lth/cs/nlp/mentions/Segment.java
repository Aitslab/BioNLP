package se.lth.cs.nlp.mentions;

import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

/**
 * Created by csz-mkg on 2017-05-09.
 */
public class Segment extends AbstractList<Yytoken> implements RandomAccess {
    private List<Yytoken> tokens;
    private int start;
    private int end;

    public Segment(List<Yytoken> tokens) {
        this.tokens = tokens;
        this.start = 0;
        this.end = tokens.size();
    }

    public Segment(List<Yytoken> tokens, int start, int end) {
        this.tokens = tokens;
        this.start = start;
        this.end = end;
    }

    public List<List<Yytoken>> titleCaseSequence() {
        PrimitiveIterator.OfInt iterator = IntStream.range(start, end).filter(idx -> {
            Yytoken tok = tokens.get(idx);
            return tok.sym != Sym.WHITESPACE;
        }).iterator();

        ArrayList<List<Yytoken>> output = new ArrayList<>();
        ArrayList<Yytoken> nameSequence = new ArrayList<>();

        while(iterator.hasNext()) {
            int pos = iterator.nextInt();
            Yytoken next = tokens.get(pos);

            if(next.sym == Sym.WORD_INITIAL || next.sym == Sym.WORD_TITLE_CASE || next.sym == Sym.WORD_MIXED_CASE_UPPER || next.sym == Sym.WORD_ACRONYM) {
                nameSequence.add(next);
            } else if(!nameSequence.isEmpty()) {
                output.add(nameSequence);
                nameSequence = new ArrayList<>();
            }
        }

        if(!nameSequence.isEmpty()) {
            output.add(nameSequence);
        }

        return output;
    }

    public String wordinitials() {
        return IntStream.range(start, end).filter(idx -> {
            switch (tokens.get(idx).sym) {
                case WORD_TITLE_CASE:
                case WORD:
                case WORD_MIXED_CASE_UPPER:
                case WORD_MIXED_CASE_LOWER:
                    return true;
                default:
                    return false;
            }
        }).mapToObj(idx -> String.valueOf(tokens.get(idx).data.charAt(0))).collect(Collectors.joining(""));
    }

    public List<List<Yytoken>> nameSequence() {
        PrimitiveIterator.OfInt iterator = IntStream.range(start, end).filter(idx -> {
            Yytoken tok = tokens.get(idx);
            return tok.sym != Sym.WHITESPACE;
        }).iterator();

        ArrayList<List<Yytoken>> output = new ArrayList<>();
        ArrayList<Yytoken> nameSequence = new ArrayList<>();

        while(iterator.hasNext()) {
            int pos = iterator.nextInt();
            Yytoken next = tokens.get(pos);

            if(next.sym == Sym.WORD_INITIAL || next.sym == Sym.WORD_TITLE_CASE || next.sym == Sym.WORD_MIXED_CASE_UPPER || next.sym == Sym.WORD_ACRONYM) {
                nameSequence.add(next);
            } else if(!nameSequence.isEmpty()) {
                if(nameSequence.size() == 1) {
                    Yytoken yytoken = nameSequence.get(0);
                    if(yytoken.idx != 0 && tokens.get(yytoken.idx-1).sym != Sym.PERIOD) {
                        if(tokens.get(yytoken.idx-1).sym == Sym.WHITESPACE) {

                            if(yytoken.idx > 1) {
                                if(tokens.get(yytoken.idx-2).sym != Sym.PERIOD) {
                                    output.add(nameSequence);
                                }
                            } else {
                                output.add(nameSequence);
                            }

                        }
                    }
                } else {
                    output.add(nameSequence);
                }

                nameSequence = new ArrayList<>();
            }
        }

        if(!nameSequence.isEmpty()) {
            output.add(nameSequence);
        }

        return output;
    }

    public List<Yytoken> tokenSequence() {
        return tokens.subList(start,end).stream()
                     .filter(tok -> tok.sym != Sym.WHITESPACE && tok.sym != Sym.CONTROL_CODES && tok.sym != Sym.NEWLINE)
                     .collect(Collectors.toList());
    }

    public String segmentText() {
        return tokens.subList(start,end).stream().map(tok -> tok.data).collect(Collectors.joining(""));
    }

    public int start() {
        return tokens.get(start).pos;
    }

    public int end() {
        Yytoken last = tokens.get(end-1);
        return last.pos+last.data.length();
    }

    @Override
    public Yytoken get(int index) {
        return tokens.get(index);
    }

    @Override
    public int size() {
        return tokens.size();
    }
}
