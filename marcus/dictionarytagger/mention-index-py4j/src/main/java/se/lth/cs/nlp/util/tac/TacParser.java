package se.lth.cs.nlp.util.tac;

import it.unimi.dsi.fastutil.ints.IntArrayList;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

public class TacParser {

    public TacParser(Reader reader) {

    }

    public static void main(String[] args) throws IOException {
        byte[] tacdata = Files.readAllBytes(Paths.get(args[0]));

        String tacxml = new String(tacdata, StandardCharsets.UTF_8);
        StringReader reader = new StringReader(tacxml);

        TacTokenizer tacTokenizer = new TacTokenizer(reader);
        Yytoken yytoken = null;

        while( (yytoken = tacTokenizer.yylex()) != null ) {
            System.out.println(yytoken.toString());
        }
    }
}
