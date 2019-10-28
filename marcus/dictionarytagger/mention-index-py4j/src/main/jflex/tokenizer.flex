package se.lth.cs.nlp.mentions;

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

        private Yytoken symbol(Sym sym) {
          return new Yytoken(sym, yychar, yytext());
        }

        private Yytoken symbol_pushback(Sym sym, int cnt) {
            String text = yytext();
            text = text.substring(0,text.length()-cnt);

            Yytoken tok = new Yytoken(sym, yychar, text);
            yypushback(cnt);
            return tok;
        }

        private Yytoken symbol(Sym sym, int start, String text) {
              return new Yytoken(sym, start, text);
        }

        private Yytoken symbol_data(Sym sym) {
          return new Yytoken(sym, startchar, data.toString());
        }

        private Yytoken consume_next_pushback(Sym sym, int cnt) throws java.io.IOException  {
            String text = yytext();
            int start = yychar;
            Yytoken nxt = yylex();
            yypushback(1);

            return symbol(sym, start, text + nxt.data.substring(0,nxt.data.length()-cnt));
        }

        private Yytoken consume_next(Sym sym) throws java.io.IOException  {
            String text = yytext();
            int start = yychar;
            Yytoken nxt = yylex();

            return symbol(sym, start, text + nxt.data);
        }
%}

%class Tokenizer
%char
//%state COMMENT,PRE,NOWIKI,TAG
%unicode

NEWLINE=\r|\n|\r\n
WHITESPACE=[\ \t\b]
DIGIT=\p{N}
DIGITS=\p{N}+
NUMBER=[+-]? ( ({DIGIT}{1,3}([,\.\ ]{DIGIT}{3})* ([\.,]{DIGIT}+)?) | {DIGIT}+ | {DIGIT}* ([\.,] {DIGIT}+) ) ([eE][+-]?{DIGIT}+)?
ACRONYM=(\p{Lu}\p{Lu}\p{Lu}{0,3}) | (\p{Lu} [\p{Lu}\p{N}]{1,4})
ACRONYM_INITIAL = \p{Lu} \p{Ll}? "."
ACRONYM_DOTTED= \p{Lu} "." \p{Lu} ("." \p{Lu})* "."?
ACRONYM_LANG = (\p{L} (".") \p{L}{1,2} "." (\p{L}{1,2} ".")*) | (\p{Ll} ({WHITESPACE}) \p{Ll}{1,2} "." (\p{Ll}{1,2} ".")*) | "e.g"
DIGIT_RANGE=\p{N} \p{N}+ {WHITESPACE}? [-–] {WHITESPACE}? \p{N} \p{N}+
HTML_ENTITY="&" (("#" [0-9]+)|("#" [xX] [0-9a-fA-Z]+)|([A-Za-z0-9]+)) ";"
ISBN_DIGIT=[0-9\-]{10,15} ("-" [0-9 Xx])?
RFC_DIGIT=[0-9]{1,6}
CONTROL_CODES=[\u0000\u0001\u0002\u0003\u0004\u0005\u0006\u0007\u0008\u0009\u000A\u000B\u000C\u000D\u000E\u000F\u0010\u0011\u0012\u0013\u0014\u0015\u0016\u0017\u0018\u0019\u001A\u001B\u001C\u001D\u001E\u001F\u0020\u007F\u0080\u0081\u0082\u0083\u0084\u0085\u0086\u0087\u0088\u0089\u008A\u008B\u008C\u008D\u008E\u008F\u0090\u0091\u0092\u0093\u0094\u0095\u0096\u0097\u0098\u0099\u009A\u009B\u009C\u009D\u009E\u009F]
NOT_CONTROL_CODES=[^\u0000\u0001\u0002\u0003\u0004\u0005\u0006\u0007\u0008\u0009\u000A\u000B\u000C\u000D\u000E\u000F\u0010\u0011\u0012\u0013\u0014\u0015\u0016\u0017\u0018\u0019\u001A\u001B\u001C\u001D\u001E\u001F\u0020\u007F\u0080\u0081\u0082\u0083\u0084\u0085\u0086\u0087\u0088\u0089\u008A\u008B\u008C\u008D\u008E\u008F\u0090\u0091\u0092\u0093\u0094\u0095\u0096\u0097\u0098\u0099\u009A\u009B\u009C\u009D\u009E\u009F]
URL_START=(([hH][tT]{2,2}[pP]("s" | "S" )?) | ([fF][tT][pP]) ) "://"
URL_USER=[^:\n\r\ \t\b@]+ (":" [^\n\r\ \t\b@]+) "@"
IPV4={DIGIT}+ "." {DIGIT}+ "." {DIGIT}+ "." {DIGIT}+
IPV6=[A-Za-z0-9]+ (":" ([A-Za-z0-9]+ | ":") )+
HOSTNAME = [\p{L}\p{N}_\-]+ ("." [\p{L}\p{N}_\-]+)+
HASHTAG="#" {NOT_CONTROL_CODES}+
URL={URL_START} {URL_USER}? ({IPV4} | {IPV6} | {HOSTNAME}) ("/" [^\n\r\ \t\b\012\|\!\{\[]* )*
WEB_INLINE_URL= [wW]{3,3} "." {HOSTNAME} ("/" [^\n\r\ \t\b\012\|\!\{\[]*)*
TITLE_CASE=\p{Lu}\p{Ll}+
UPPER_CASE=\p{Lu}+
MIXED_CASE_UPPER=\p{Lu}\p{Ll}+\p{Lu}\p{L}*
MIXED_CASE_LOWER=\p{Ll}+\p{Lu}\p{L}*
WORD=\p{L}+
WORD_BOUNDARY=[:;\.,–\-－﹣֊一\"/\\”«»'’%‰\(\)\{\}\[\]!?&\p{Sc}]
WORD_TERMINAL={WHITESPACE}|{WORD_BOUNDARY}
PREPEND=\p{L}['’´‘]
PREPEND_SINGLE=\p{L}['’´‘]\p{Ll}
ATTACHMENT=['’´‘]\p{Ll}+
UPPER_TERMINAL=\p{Lu}{WORD_TERMINAL}
MONTH=(0[0-9])|(1[0-2])
DAY=([0-2][0-9])|(3[0-2])
SECOND_MIN=([0-5][0-9])|60
HOUR=([0-1][0-9])|([2][0-3])
YEAR=([0-9]{4,4})
DATE={YEAR}-{MONTH}(-{DAY})?
TIME={HOUR}:{SECOND_MIN}(:{SECOND_MIN})?
RFC_DATE={YEAR}-{MONTH}-{DAY}T{HOUR}:{SECOND_MIN}:{SECOND_MIN}(\.[0-9]+)?(Z|({WHITESPACE}*[+-]{TIME})?)
%%

<YYINITIAL> {
  ":" { return symbol(Sym.COLON); }
  [,，ʻ،⸲⸴⹁、︐︑﹐﹑，､] { return symbol(Sym.COMMA); }
  [“”\"«»‘’„“‚‘] { return symbol(Sym.CITATION); }
  [\–\-\－\﹣\一] { return symbol(Sym.HYPHEN); }
  ";" { return symbol(Sym.SEMICOLON); }
  "\"" { return symbol(Sym.CITATION); }
  "/" { return symbol(Sym.SLASH); }
  "\\" { return symbol(Sym.SLASH); }
  {ATTACHMENT} / {WORD_TERMINAL} { return symbol(Sym.ELISION_SUFFIX); }
  [’'´‘] { return symbol(Sym.APOSTROPHE); }
  "%" { return symbol(Sym.PERCENT); }
  "‰" { return symbol(Sym.PERCENT); }
  \p{Sc} { return symbol(Sym.CURRENCY); }
  "(" { return symbol(Sym.PAREN_LEFT); }
  ")" { return symbol(Sym.PAREN_RIGHT); }
  "{" { return symbol(Sym.CURLY_LEFT); }
  "}" { return symbol(Sym.CURLY_RIGHT); }
  "[" { return symbol(Sym.BRACKET_LEFT); }
  "]" { return symbol(Sym.BRACKET_RIGHT); }
  "|" { return symbol(Sym.PIPE); }
  "!" { return symbol(Sym.BANG); }
  "?" { return symbol(Sym.QUESTION); }
  {RFC_DATE} { return symbol(Sym.DATETIME); }
  {DATE} { return symbol(Sym.DATE); }
  {TIME} { return symbol(Sym.TIME); }
  {DIGIT_RANGE} { return symbol(Sym.RANGE); }
  {NUMBER} / {ACRONYM_INITIAL} { return consume_next(Sym.WORD); }
  {NUMBER} / {WORD_TERMINAL} { return symbol(Sym.NUMBER); }
  {NUMBER} / {UPPER_TERMINAL} { return consume_next(Sym.WORD); }
  {NUMBER} / {WORD} { return symbol(Sym.NUMBER); }
  {NUMBER} { return symbol(Sym.NUMBER); }

  {HASHTAG} { return symbol(Sym.HASHTAG); }
  {HTML_ENTITY} { return symbol(Sym.HTML_ENTITY); }
  "&" { return symbol(Sym.AMPERSAND); }
  {WHITESPACE}+ { return symbol(Sym.WHITESPACE); }
  {NEWLINE} {return symbol(Sym.NEWLINE); }
  "RFC" {WHITESPACE}+ {RFC_DIGIT} { return symbol(Sym.RFC); }
  "ISBN" {WHITESPACE}+ {ISBN_DIGIT} { return symbol(Sym.ISBN); }
  "PMID" {WHITESPACE}+ {DIGIT}+ { return symbol(Sym.PMID); }
  {URL} {   if(yycharat(yylength()-1) == '.') {
                yypushback(1);
            }
            return symbol(Sym.URL);
  }
  {WEB_INLINE_URL} { return symbol(Sym.URL); }
  {CONTROL_CODES} { return symbol(Sym.CONTROL_CODES); }

  {PREPEND_SINGLE} / {WORD_TERMINAL} { return symbol_pushback(Sym.WORD_UPPER_CASE, 2); }
  {PREPEND} / {WORD} { return symbol(Sym.ELISION_PREFIX); }

  {ACRONYM} { return symbol(Sym.WORD_ACRONYM); }
  {ACRONYM_DOTTED} { return symbol(Sym.WORD_ACRONYM); }
  {ACRONYM_LANG} { return symbol(Sym.WORD_ACRONYM); }
  {ACRONYM_INITIAL} { return symbol(Sym.WORD_INITIAL); }
  {UPPER_CASE} {return symbol(Sym.WORD_UPPER_CASE); }
  {MIXED_CASE_UPPER} { return symbol(Sym.WORD_MIXED_CASE_UPPER); }
  {MIXED_CASE_LOWER} { return symbol(Sym.WORD_MIXED_CASE_LOWER); }
  {TITLE_CASE} {return symbol(Sym.WORD_TITLE_CASE); }

  {UPPER_CASE} / ({DIGITS} {WHITESPACE}) { return consume_next(Sym.WORD); }
  {WORD} / ({DIGITS} {WHITESPACE}) { return consume_next(Sym.WORD); }

  {WORD} { return symbol(Sym.WORD); }
  [.。] { return symbol(Sym.PERIOD); }
  [\n\r\u000B\u000C\u0085\u2028\u2029] { return symbol(Sym.NEWLINE); }
  . { return symbol(Sym.RAW); }
}