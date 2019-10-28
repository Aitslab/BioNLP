package se.lth.cs.nlp.util.tac;

%%

%{
    StringBuilder data = new StringBuilder();
            private int startchar;

            private void begin_symbol() {
                this.data.setLength(0);
                startchar = yychar;
                data.append(yytext());
            }

            private void end_symbol() {
                data.append(yytext());
            }

            private Yytoken symbol(TacSym sym) {
              return new Yytoken(sym, yychar, yytext());
            }

            private Yytoken symbol(TacSym sym, int delta) {
              return new Yytoken(sym, yychar + delta, yytext().substring(delta));
            }

            private Yytoken symbol_pushback(TacSym sym, int cnt) {
                String text = yytext();
                text = text.substring(0,text.length()-cnt);

                Yytoken tok = new Yytoken(sym, yychar, text);
                yypushback(cnt);
                return tok;
            }

            private Yytoken symbol(TacSym sym, int start, String text) {
                  return new Yytoken(sym, start, text);
            }

            private Yytoken symbol_data(TacSym sym) {
              return new Yytoken(sym, startchar, data.toString());
            }

            private Yytoken consume_next_pushback(TacSym sym, int cnt) throws java.io.IOException  {
                String text = yytext();
                int start = yychar;
                Yytoken nxt = yylex();
                yypushback(1);

                return symbol(sym, start, text + nxt.data.substring(0,nxt.data.length()-cnt));
            }

            private Yytoken consume_next(TacSym sym)  throws java.io.IOException {
                String text = yytext();
                int start = yychar;
                Yytoken nxt = yylex();

                return symbol(sym, start, text + nxt.data);
            }
%}

%class TacTokenizer
%char

%state TAG

%unicode

//NEWLINE=\r|\n|\r\n
WHITESPACE=[\ \t\b\u000C]
//DIGIT=\p{N}
//DIGITS=\p{N}+
//NUMBER=[+-]? ( ({DIGIT}{1,3}([,\.\ ]{DIGIT}{3})* ([\.,]{DIGIT}+)?) | {DIGIT}+ | {DIGIT}* ([\.,] {DIGIT}+) ) ([eE][+-]?{DIGIT}+)?
HTML_ENTITY="&" ( ("#" [0-9]+) | ("#" [xX] [0-9a-fA-F]+) | ([a-zA-Z0-9]+)) ";"
//CONTROL_CODES=[\u0000\u0001\u0002\u0003\u0004\u0005\u0006\u0007\u0008\u0009\u000A\u000B\u000C\u000D\u000E\u000F\u0010\u0011\u0012\u0013\u0014\u0015\u0016\u0017\u0018\u0019\u001A\u001B\u001C\u001D\u001E\u001F\u0020\u007F\u0080\u0081\u0082\u0083\u0084\u0085\u0086\u0087\u0088\u0089\u008A\u008B\u008C\u008D\u008E\u008F\u0090\u0091\u0092\u0093\u0094\u0095\u0096\u0097\u0098\u0099\u009A\u009B\u009C\u009D\u009E\u009F]
//NOT_CONTROL_CODES=[^\u0000\u0001\u0002\u0003\u0004\u0005\u0006\u0007\u0008\u0009\u000A\u000B\u000C\u000D\u000E\u000F\u0010\u0011\u0012\u0013\u0014\u0015\u0016\u0017\u0018\u0019\u001A\u001B\u001C\u001D\u001E\u001F\u0020\u007F\u0080\u0081\u0082\u0083\u0084\u0085\u0086\u0087\u0088\u0089\u008A\u008B\u008C\u008D\u008E\u008F\u0090\u0091\u0092\u0093\u0094\u0095\u0096\u0097\u0098\u0099\u009A\u009B\u009C\u009D\u009E\u009F]
//URL_START=(([hH][tT]{2,2}[pP]("s" | "S" )?) | ([fF][tT][pP]) ) "://"
//URL_USER=[^:\n\r\ \t\b@]+ (":" [^\n\r\ \t\b@]+) "@"
//IPV4={DIGIT}+ "." {DIGIT}+ "." {DIGIT}+ "." {DIGIT}+
//IPV6=[A-Za-z0-9]+ (":" ([A-Za-z0-9]+ | ":") )+
//HOSTNAME = [\p{L}\p{N}_\-]+ ("." [\p{L}\p{N}_\-]+)+
//HASHTAG="#" {NOT_CONTROL_CODES}+
//URL={URL_START} {URL_USER}? ({IPV4} | {IPV6} | {HOSTNAME}) ("/" [^\n\r\ \t\b\012\|\!\{\[]* )*

TAG_START = ("<?" [a-zA-Z0-9_]+) | ("<" [a-zA-Z0-9_]+)
TAG_ATTRS = {WHITESPACE}* ({ATTR_NAME} ({WHITESPACE}* "=" {WHITESPACE}* {ATTR_VALUE})? {WHITESPACE}* )* ">"
TAG_END = "</" [a-zA-Z0-9_]+ {WHITESPACE}* ">"
ATTR_SET = {WHITESPACE}* "="
ATTR_NAME = [^\u0000\u0022\u0027\u003E\u002F\u003D\ \t\b\u000C]+
ATTR_VALUE = ("\"" [^\"]* "\"") | ("'" [^']* "'") | [^\u0000\u0022\u0027\u003E\u002F\u003D\ \t\b\u000C]+
TAG_SINGLETON_END = "/>" | "?>"
ATTR_END = ">"

HTML_COMMENT = "<!--" ([^-] | "-") "-->"

%%

<TAG> {
    {TAG_SINGLETON_END} {
        Yytoken tok = symbol(TacSym.TAG_SINGLETON_END);
        yybegin(YYINITIAL);
        return tok;
    }
    {ATTR_END} {
        Yytoken tok = symbol(TacSym.ATTR_END);
        yybegin(YYINITIAL);
        return tok;
    }
    {WHITESPACE}+ {}
    {ATTR_NAME} / {ATTR_SET} { return symbol(TacSym.ATTR_NAME); }
    {ATTR_NAME} { return symbol(TacSym.ATTR_VALUE); }
    "=" {}
    {HTML_COMMENT} { return symbol(TacSym.COMMENT); }
    {ATTR_VALUE} { return symbol(TacSym.ATTR_VALUE); }
    . {}
}

<YYINITIAL> {
  {TAG_START} {
    Yytoken sym = symbol(TacSym.TAG_START);
    yybegin(TAG);
    return sym;
  }

  {TAG_END} {
    return symbol(TacSym.TAG_END);
  }

  {HTML_COMMENT} { return symbol(TacSym.COMMENT); }
  {HTML_ENTITY} { return symbol(TacSym.ENTITY); }

  [^<&#]+ { return symbol(TacSym.TEXT); }

  "<" { return symbol(TacSym.TEXT); }
  "#" { return symbol(TacSym.TEXT); }
  "&" { return symbol(TacSym.TEXT); }
}