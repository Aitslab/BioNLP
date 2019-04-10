#include <list>
#include <string>
#include <sstream>

using namespace std;

static void
replace(string & s, const string & s1, const string & s2, const char skip = 0);

void
tokenize(const string & s1, list<string> & lt)
{
  lt.clear();
    
  string s(s1);
  
  if (s[0] == '"') s.replace(0, 1, "`` ");
  replace(s, " \"", "  `` ");
  replace(s, "(\"", "( `` ");
  replace(s, "[\"", "[ `` ");
  replace(s, "{\"", "{ `` ");
  replace(s, "<\"", "< `` ");

  replace(s, "...", " ... ");

  replace(s, ",", " , ");
  replace(s, ";", " ; ");
  replace(s, ":", " : ");
  replace(s, "@", " @ ");
  replace(s, "#", " # ");
  replace(s, "$", " $ ");
  replace(s, "%", " % ");
  replace(s, "&", " & ");

  int pos = s.size() - 1;
  while (pos > 0 && s[pos] == ' ') pos--;
  while (pos > 0) {
    char c = s[pos];
    if (c == '[' || c == ']' || c == ')' || c == '}' || c == '>' ||
        c == '"' || c == '\'') {
      pos--; continue;
    }
    break;
  }
  if (pos >= 0 && s[pos] == '.' && !(pos > 0 && s[pos-1] == '.')) s.replace(pos, 1, " .");
  
  replace(s, "?", " ? ");
  replace(s, "!", " ! ");
    
  replace(s, "[", " [ ");
  replace(s, "]", " ] ");
  replace(s, "(", " ( ");
  replace(s, ")", " ) ");
  replace(s, "{", " { ");
  replace(s, "}", " } ");
  replace(s, "<", " < ");
  replace(s, ">", " > ");

  replace(s, "--", " -- ");

  s.replace(string::size_type(0), 0, " ");
  s.replace(s.size(), 0, " ");
  
  replace(s, "\"", " '' ");

  replace(s, "' ", " ' ", '\'');
  replace(s, "'s ", " 's ");
  replace(s, "'S ", " 'S ");
  replace(s, "'m ", " 'm ");
  replace(s, "'M ", " 'M ");
  replace(s, "'d ", " 'd ");
  replace(s, "'D ", " 'D ");
  replace(s, "'ll ", " 'll ");
  replace(s, "'re ", " 're ");
  replace(s, "'ve ", " 've ");
  replace(s, "n't ", " n't ");
  replace(s, "'LL ", " 'LL ");
  replace(s, "'RE ", " 'RE ");
  replace(s, "'VE ", " 'VE ");
  replace(s, "N'T ", " N'T ");

  replace(s, " Cannot ", " Can not ");
  replace(s, " cannot ", " can not ");
  replace(s, " D'ye ", " D' ye ");
  replace(s, " d'ye ", " d' ye ");
  replace(s, " Gimme ", " Gim me ");
  replace(s, " gimme ", " gim me ");
  replace(s, " Gonna ", " Gon na ");
  replace(s, " gonna ", " gon na ");
  replace(s, " Gotta ", " Got ta ");
  replace(s, " gotta ", " got ta ");
  replace(s, " Lemme ", " Lem me ");
  replace(s, " lemme ", " lem me ");
  replace(s, " More'n ", " More 'n ");
  replace(s, " more'n ", " more 'n ");
  replace(s, "'Tis ", " 'T is ");
  replace(s, "'tis ", " 't is ");
  replace(s, "'Twas ", " 'T was ");
  replace(s, "'twas ", " 't was ");
  replace(s, " Wanna ", " Wan na ");
  replace(s, " wanna ", " wanna ");

  istringstream is(s);
  string t;
  while (is >> t) {
    lt.push_back(t);
  }

}

static void
replace(string & s, const string & s1, const string & s2, const char skip)
{
  string::size_type pos = 0;
  while (1) {
    string::size_type i = s.find(s1, pos);
    if (i == string::npos) break;
    if (i > 0 && s[i-1] == skip) {
      pos = i + 1;
      continue;
    }
    s.replace(i, s1.size(), s2);
    pos = i + s2.size();
  }

}

