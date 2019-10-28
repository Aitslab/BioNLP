package se.lth.cs.nlp.util.tac;

import it.unimi.dsi.fastutil.ints.*;
import org.apache.commons.lang3.StringEscapeUtils;

import java.io.IOError;
import java.io.IOException;
import java.io.StringReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.Stream;

public class TacDocument implements Iterable<TacNode> {
    protected String xml;
    protected TacElement rootNode;

    public TacDocument(String xml) {
        this.xml = xml;
        parse();
    }

    public int codePointLocation(int offset) {
        return xml.codePointCount(0, offset);
    }

    public IntArrayList codePointLocations(IntArrayList offsets) {
        Int2IntAVLTreeMap offset2target = new Int2IntAVLTreeMap();
        IntAVLTreeSet offsetsSorted = new IntAVLTreeSet(offsets);
        int last = 0;
        int delta = 0;
        IntBidirectionalIterator iter = offsetsSorted.iterator();
        while(iter.hasNext()) {
            int off = iter.nextInt();
            offset2target.put(off, off+delta);
            delta += xml.codePointCount(last, off) + (last-off);
            last = off;
        }

        IntArrayList output = new IntArrayList();
        IntListIterator offiter = offsets.iterator();
        while(offiter.hasNext()) {
            int srcoff = offiter.nextInt();
            output.add(offset2target.get(srcoff));
        }

        return output;
    }

    private class Parser {
        public TacElement rootNode;
        public List<Yytoken> tokens;
        public ArrayDeque<TacElement> currentNode = new ArrayDeque<>();
        public int pos;

        public Parser(List<Yytoken> tokens) {
            this.tokens = tokens;
            this.pos = 0;
            this.rootNode = new TacElement(TacDocument.this, 0, xml.length(), "__ROOT__");
            this.currentNode.add(this.rootNode);
        }

        private TacNode parseString(Yytoken str) {
            if(str.data.startsWith("\"")) {
                return new TacText(TacDocument.this, str.data.substring(1,str.data.length()-1), str.pos+1, str.pos+str.data.length()-1);
            }
            else if(str.data.startsWith("\'")) {
                return new TacText(TacDocument.this, str.data.substring(1,str.data.length()-1), str.pos+1, str.pos+str.data.length()-1);
            }
            else {
                return new TacText(TacDocument.this, str.data, str.pos, str.pos+str.data.length());
            }
        }

        private void parse_tag() {
            Yytoken current = tokens.get(pos);
            TacElement element = new TacElement(TacDocument.this, current.pos, current.pos+ current.data.length(), current.data.startsWith("<%") ? current.data.substring(2) : current.data.substring(1));

            assert currentNode.peek() != null;
            currentNode.peek().add(element);

            if(tokens.get(pos).terminated) {
                currentNode.push(element);
            }

            pos++;

            TacNode attrName = null;

            outer: while(pos < tokens.size()) {
                Yytoken yytoken = tokens.get(pos);
                switch (yytoken.sym) {
                    case ATTR_END:
                        element.end = yytoken.pos+1;
                        break outer;
                    case TAG_SINGLETON_END:
                        element.end = yytoken.pos + 2;
                        if(tokens.get(pos).terminated) {
                            this.currentNode.pop();
                        }
                        break outer;
                    case ATTR_NAME:
                        attrName = parseString(yytoken);
                        break;
                    case ATTR_VALUE:
                        element.add(new TacAttribute(attrName, parseString(yytoken)));
                        attrName = null;
                        break;
                    case COMMENT:
                        break;
                    default:
                        break outer;
                }

                pos++;
            }
        }

        private void pop_tag() {
            if(tokens.get(pos).terminated) {
                Yytoken yytoken = tokens.get(pos);
                String tagname = yytoken.data.substring(2,yytoken.data.length()-1);
                assert this.currentNode.peek() != null;
                if(this.currentNode.peek().name().equalsIgnoreCase(tagname)) {
                    this.currentNode.peek().end = yytoken.pos+yytoken.data.length();
                    this.currentNode.pop();
                } else if(this.currentNode.size() == 1) {
                    //Ignore popping
                } else {
                    //Try to find parent
                    int num = 0;
                    boolean found = false;
                    for (TacElement aCurrentNode : this.currentNode) {
                        if (aCurrentNode.name().equalsIgnoreCase(tagname)) {
                            found = true;
                            break;
                        }
                        num++;
                    }

                    if(found) {
                        for(int i = 0; i < num; i++) {
                            this.currentNode.peek().end = yytoken.pos+yytoken.data.length();
                            this.currentNode.pop();
                        }
                    }
                }
            }
        }

        private void parse_text() {
            StringBuilder sb = new StringBuilder();
            int startpos = tokens.get(pos).pos;

            outer: while(pos < tokens.size()) {
                Yytoken yytoken = tokens.get(pos);
                switch (yytoken.sym) {
                    case TEXT:
                        sb.append(yytoken.data);
                        break;
                    default:
                        pos--;
                        break outer;
                }

                pos++;
            }

            assert this.currentNode.peek() != null;
            this.currentNode.peek().add(new TacText(TacDocument.this, sb.toString(), startpos, startpos+sb.length()));
        }

        private void prepass() {
            ArrayDeque<Yytoken> start_node = new ArrayDeque<>();
            ArrayDeque<String> tagname_hiearchy = new ArrayDeque<>();
            int localpos = 0;
            while(localpos < tokens.size()) {
                Yytoken yytoken = tokens.get(localpos);
                switch (yytoken.sym) {
                    case TAG_START:
                        start_node.push(yytoken);
                        if(yytoken.data.startsWith("<%"))
                            tagname_hiearchy.push(yytoken.data.substring(2));
                        else
                            tagname_hiearchy.push(yytoken.data.substring(1));

                        break;
                    case TAG_SINGLETON_END:
                        start_node.pop().terminated = true;
                        yytoken.terminated = true;
                        tagname_hiearchy.pop();
                        break;
                    case TAG_END:
                        if(tagname_hiearchy.isEmpty()) {
                            yytoken.terminated = false;
                        } else {
                            String end_tag = yytoken.data.substring(2, yytoken.data.length() - 1);
                            if (tagname_hiearchy.peek().equalsIgnoreCase(end_tag)) {
                                //Tag ends properly!
                                start_node.pop().terminated = true;
                                tagname_hiearchy.pop();
                                yytoken.terminated = true;
                            } else {
                                //Nodes are not terminated properly
                                //Find closest
                                int depth = 0;
                                boolean found = false;
                                Iterator<String> iter = tagname_hiearchy.iterator();
                                while (iter.hasNext()) {
                                    String next = iter.next();
                                    if (next.equalsIgnoreCase(end_tag)) {
                                        found = true;
                                        break;
                                    }
                                    depth++;
                                }

                                if (!found) {
                                    yytoken.terminated = false;
                                } else {
                                    for (int i = 0; i < depth; i++) {
                                        if(start_node.isEmpty()) {
                                            System.out.print("Wot!");
                                        }
                                        tagname_hiearchy.pop();
                                        start_node.pop().terminated = false;
                                    }
                                    start_node.pop().terminated = true;
                                    tagname_hiearchy.pop();
                                    yytoken.terminated = true;
                                }
                            }
                        }
                        break;
                }
                localpos++;
            }
        }

        public void parse() {
            //1. Prepass to solve inconsistency errors
            prepass();

            //2. Building pass
            while(pos < tokens.size()) {
                Yytoken yytoken = tokens.get(pos);
                switch (yytoken.sym) {
                    case TAG_START:
                        parse_tag();
                        break;
                    case TAG_END:
                        pop_tag();
                        break;
                    case COMMENT:
                        break;
                    case ENTITY:
                        assert this.currentNode.peek() != null;
                        this.currentNode.peek().add(new TacText(TacDocument.this, StringEscapeUtils.unescapeHtml4(yytoken.data), yytoken.pos, yytoken.pos+yytoken.data.length()));
                        break;
                    case TEXT:
                        parse_text();
                        break;
                }

                pos++;
            }
        }
    }

    public void removeElements(String...tags) {
        ArrayDeque<TacElement> parent = new ArrayDeque<>();
        ArrayDeque<Iterator<TacNode>> current = new ArrayDeque<>();
        parent.push(rootNode);
        current.push(rootNode.iterator());

        HashSet<String> removals = new HashSet<>();
        for (String tag : tags) {
            removals.add(tag.toLowerCase());
        }

        while(!current.isEmpty()) {
            if(current.peek().hasNext()) {
                TacNode node = current.peek().next();
                if(node instanceof TacElement) {
                    if(removals.contains(((TacElement) node).name().toLowerCase())) {
                        parent.peek().remove(node);
                    } else {
                        parent.push((TacElement) node);
                        current.push(((TacElement) node).iterator());
                    }
                }
            }
            else {
                parent.pop();
                current.pop();
            }
        }
    }

    private void parse() {
        try {
            TacTokenizer tokenizer = new TacTokenizer(new StringReader(xml));
            Yytoken yytoken = null;

            ArrayList<Yytoken> tokens = new ArrayList<>();

            while( (yytoken = tokenizer.yylex()) != null ) {
                tokens.add(yytoken);
            }

            Parser parser = new Parser(tokens);
            parser.parse();
            this.rootNode = parser.rootNode;
        } catch (IOException e) {
            throw new IOError(e);
        }
    }

    @Override
    public Iterator<TacNode> iterator() {
        return this.rootNode.iterator();
    }

    public TextMapping text() {
        TextMapping mapping = new TextMapping();
        ArrayDeque<Iterator<TacNode>> current = new ArrayDeque<>();
        current.push(iterator());

        while(!current.isEmpty()) {
            if(current.peek().hasNext()) {
                TacNode node = current.peek().next();
                if(node instanceof TacElement) {
                    current.push(((TacElement) node).iterator());
                }
                else if(node instanceof TacText) {
                    mapping.append(node.start, node.text());
                }
            }
            else {
                current.pop();
            }
        }

        return mapping;
    }

    public Stream<TacNode> nodes() {
        ArrayList<TacNode> nodes = new ArrayList<>();

        ArrayDeque<Iterator<TacNode>> current = new ArrayDeque<>();
        current.push(iterator());

        while(!current.isEmpty()) {
            if(current.peek().hasNext()) {
                TacNode node = current.peek().next();
                if(node instanceof TacElement) {
                    current.push(((TacElement) node).iterator());

                }
                nodes.add(node);
            }
            else {
                current.pop();
            }
        }

        return nodes.stream();
    }

    public Stream<TacElement> elements() {
        ArrayList<TacElement> elements = new ArrayList<>();

        ArrayDeque<Iterator<TacNode>> current = new ArrayDeque<>();
        current.push(iterator());

        while(!current.isEmpty()) {
            if(current.peek().hasNext()) {
                TacNode node = current.peek().next();
                if(node instanceof TacElement) {
                    current.push(((TacElement) node).iterator());
                    elements.add((TacElement)node);
                }
            }
            else {
                current.pop();
            }
        }

        return elements.stream();
    }

    public static void main(String[] args) throws IOException {
        byte[] tacdata = Files.readAllBytes(Paths.get(args[0]));

        String tacxml = new String(tacdata, StandardCharsets.UTF_8);
        TacDocument tacDocument = new TacDocument(tacxml);
        TextMapping text = tacDocument.text();

        String rawtext = text.text();
        System.out.print(rawtext);
        //int pos = rawtext.indexOf("而且从廊开往曼谷修建，以防泰国政局变化！！");

        //int rawpos = text.translate(pos);
        //System.out.println(rawpos);
        //System.out.println(tacDocument.codePointLocation(rawpos));

        System.out.println("Total len = " + tacxml.codePoints().count());
        System.out.println("Real len = " + tacxml.length());

        //System.out.println(tacxml.substring(rawpos, rawpos+"而且从廊开往曼谷修建，以防泰国政局变化！！".length()));

    }
}
