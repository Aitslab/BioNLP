#include <stdio.h>
#include <fstream>
#include <map>
#include <list>
#include <iostream>
#include "maxent.h"
#include <sstream>
#include "common.h"

using namespace std;

const double BIAS_FOR_RECALL = 0.6;

int max_term_length = 0;

/*
struct Token
{
  string str;
  string pos;
  string chunk;
  string label;
  Token(string s, string p, string l) : str(s), pos(p), label(l) {}
};
*/

struct WordInfo
{
  string str;
  int inside_ne;
  int edge_ne;
  int total;
  WordInfo() : str(""), inside_ne(0), total(0), edge_ne(0) {};
  WordInfo(const string & s, int i, int e, int t) : str(s), inside_ne(i), total(t), edge_ne(e) {};
  double out_prob() const {
    return ( (total - inside_ne) + 1.0 ) / ( total + 2.0 );
  }
  double in_prob() const {
    return ( inside_ne + 1.0 ) / ( total + 2.0 );
  }
  double edge_prob() const {
    return ( edge_ne + 1.0 ) / ( total + 2.0 );
  }
  bool operator<(const WordInfo & x) const {
    //    return this->out_prob() > x.out_prob();
    return this->edge_prob() > x.edge_prob();
  }
};


map<string, WordInfo> word_info;
map<string, WordInfo> pos_info;


typedef vector<Token> Sentence;

static string normalize(const string & s)
{
  string tmp;
  for (int i = 0; i < s.size(); i++) {
    char c = tolower(s[i]);
    if (isdigit(c)) c = '#';
    if (c == '-' || c == ' ') continue;
    tmp += c;
  }
  /*
  if (tmp == "is") tmp = "be";
  if (tmp == "was") tmp = "be";
  if (tmp == "are") tmp = "be";
  if (tmp == "were") tmp = "be";
  if (tmp == "an") tmp = "a";
  if (tmp == "the") tmp = "a";
  */
  if (tmp[tmp.size()-1] == 's') return tmp.substr(0, tmp.size()-1);
  return tmp;
}

static string wordshape(const string & s, bool fine)
{
  string tmp;
  char pre_c = 0;
  for (int i = 0; i < s.size(); i++) {
    char c = s[i];
    if (isdigit(c)) c = '#';
    else if (isupper(c)) c = 'A';
    else if (islower(c)) c = 'a';
    else if (c == ' ' || c == '-') c = '-';
    else continue;
    if (fine || c != pre_c) 
      tmp += c;
    pre_c = c;
  }
  return tmp;
}

static ME_Sample mesample(const string & label, const vector<Token> &vt, int begin, int end)
{
  ME_Sample mes;

  mes.label = label;

  string s;

  // contextual feature
  string s_1, s_2, s1, s2;
  //  if (begin >= 1) s_1 = vt[begin-1].str;
  if (begin >= 1) s_1 = normalize(vt[begin-1].str);
  else            s_1 = "BOS";
  mes.features.push_back("C-1_" + s_1);

  //  if (end < vt.size()) s1 = vt[end].str;
  if (end < vt.size()) s1 = normalize(vt[end].str);
  else                 s1 = "EOS";
  mes.features.push_back("C+1_" + s1);

  //  if (begin >= 2) s_2 = vt[begin-2].str;
  if (begin >= 2) s_2 = normalize(vt[begin-2].str);
  else            s_2 = "BOS";

  //  if (end < vt.size()-1) s2 = vt[end+1].str;
  if (end < vt.size()-1) s2 = normalize(vt[end+1].str);
  else                   s2 = "EOS";

  mes.features.push_back("C-2-1_" + s_2 + "_" + s_1);
  mes.features.push_back("C-1+1_" + s_1 + "_" + s1);
  mes.features.push_back("C+1+2_" + s1  + "_" + s2);

  // term feature
  char firstletter = vt[begin].str[0];
  char lastletter = vt[end-1].str[vt[end-1].str.size()-1];
  //  if (begin != 0 && isupper(firstletter))
  //  if (isupper(firstletter) && isupper(lastletter)) 
  //    mes.features.push_back("IS_UPPER");

  //  if (end - begin == 1) {
  //    mes.features.push_back("EXACT_" + vt[begin].str);
  //  }
  
  string tb = normalize(vt[begin].str);
  mes.features.push_back("TB_" + tb);
  
  for (int i = begin + 1; i < end-1; i++) {
  //for (int i = begin; i < end; i++) {
    s = normalize(vt[i].str);
    mes.features.push_back("TM_" + s);
  }

  string te = normalize(vt[end-1].str);
  mes.features.push_back("TE_" + te);

  
  // combination
  mes.features.push_back("C-1_TB_" + s_1 + "_" + tb);
  mes.features.push_back("C-1_TE_" + s_1 + "_" + te);
  mes.features.push_back("TB_TE_" + tb + "-" + te);
  mes.features.push_back("TB_C+1_" + tb + "_" + s1);
  mes.features.push_back("TE_C+1_" + te + "-" + s1);

  //  mes.features.push_back("C-2-1_TE_" + s_2 + "_" + s_1 + "_" + te);
  //  mes.features.push_back("TE_C+1+2_" + te + "_" + s1 + "_" + s2);
  
  

  s = "";
  string whole = "";
  bool contain_comma = false;
  for (int i = begin; i < end; i++) {
    s += normalize(vt[i].str);
    whole += vt[i].str;
  }
  //if (label > 0) mes.features.push_back(buf);
  mes.features.push_back("WHOLE_" + s);
  mes.features.push_back("WS1_" + wordshape(whole, true));
  mes.features.push_back("WS2_" + wordshape(whole, false));

  //  mes.features.push_back("WHOLE_C+1_" + whole + "-" + s1);
  

  // preffix and suffix
  for (int j = 1; j <= 10; j++) {
    stringstream buf;
    if (s.size() >= j) {
      buf << "SUF" << j << "_" << s.substr(s.size() - j);
      mes.add_feature(buf.str());
      buf.str("");
    }
    if (s.size() >= j) {
      buf << "PRE" << j << "_" << s.substr(0, j);
      mes.add_feature(buf.str());
      buf.str("");
    }
  }

  
  //  if (contain_comma)
  //    mes.features.push_back("CONTAIN_COMMA");

  //  cout << fb.Id(string(buf)) << " " << string(buf) << endl;


  // POS feature
  string p_2 = "BOS", p_1 = "BOS";
  string pb, pe;
  string p1 = "EOS", p2 = "EOS";
  if (begin >= 2) p_2 = vt[begin-2].pos;
  if (begin >= 1) p_1 = vt[begin-1].pos;
  pb = vt[begin].pos;
  pe = vt[end-1].pos;
  if (end < vt.size())   p1 = vt[end].pos;
  if (end < vt.size()-1) p2 = vt[end+1].pos;

  mes.features.push_back("PoS-1_" + p_1);
  mes.features.push_back("PoS-B_" + pb);
  mes.features.push_back("PoS-E_" + pe);
  mes.features.push_back("PoS+1_" + p1);
  //  string posseq;
  //  for (int i = begin; i < end; i++) {
  //    posseq += vt[i].pos + "_";
  //  }
  //  mes.features.push_back("PosSeq_" + posseq);
  
  
  return mes;
}


static bool is_candidate(const Sentence & s, const int begin, const int end)
{
  if (word_info[s[begin].str].edge_prob() < 0.01) return false;
  if (word_info[s[end-1].str].edge_prob() < 0.01) return false;
  //  if (end - begin > 10) return false;
  if (end - begin > 30) return false;

  int penalty = 0;
  int kakko = 0;
  for (int x = begin; x < end; x++) {
    if (s[x].str == string("(")) kakko++;
    if (s[x].str == string(")")) {
      if (kakko % 2 == 0) return false;
      kakko--;
    }
    double out_prob = word_info[s[x].str].out_prob();
    //    if (out_prob >= 0.99) penalty++;
    //    if (out_prob >= 0.90) penalty++;
    //    if (out_prob >= 0.98) penalty++;
    //    if (out_prob >= 0.94) penalty++;
    if (out_prob >= 0.99) penalty++;
    if (out_prob >= 0.98) penalty++;
    if (out_prob >= 0.97) penalty++;
    if (s[x].pos == "VBZ") return false;
    if (s[x].pos == "VB")  return false;
    if (s[x].pos == "VBP") return false;
    if (s[x].pos == "MD")  return false;
    if (s[x].pos == "RB") penalty += 1;
  
    if (penalty >= 5) return false;
  }

  if (s[end-1].pos == "JJ") penalty += 2;
  if (s[end-1].pos == "IN") penalty += 3;

  if (penalty >= 5) return false;

  if (kakko % 2 != 0) return false;
  
  //    for (int x = begin; x < end; x++) {
  //      cout << s[x].str << "/" << s[x].pos << " ";
  //    }
  //    cout << endl;

  return true;
}

void load_word_info(const string & filename)
{
  ifstream ifile(filename.c_str());
  if (!ifile) { cerr << "error: cannot open " << filename << endl; exit(1); }

  word_info.clear();
  string line;
  while (getline(ifile, line)) {
    istringstream is(line.c_str());
    string s;
    int i, e, t;
    is >> s >> i >> e >> t;
    WordInfo wi(s, i, e, t);
    word_info.insert(make_pair(s, wi));
  }
}



struct Annotation 
{
  int label;
  int begin;
  int end;
  double prob;
  bool operator<(const Annotation & x) const { return prob > x.prob; }
  Annotation(const int l, const int b, const int e, const double p) :
    label(l), begin(b), end(e), prob(p) {}
};


void find_NEs(const ME_Model & me,
              Sentence & s)
{
  const int other_class = me.get_class_id("O");
  
  vector<double> label_p(s.size());
  for (int j = 0; j < s.size(); j++) {
    s[j].ne = string("O");
    label_p[j] = 0;
  }
  list<Annotation> la;
  for (int j = 0; j < s.size(); j++) {
    //      for (int k = s.size(); k > j; k--) {
    for (int k = j + 1; k <= s.size(); k++) {
      if (!is_candidate(s, j, k)) {
        //        if (isterm(s_org, j, k)) num_candidate_false_negatives++;
        continue;
      }
      ME_Sample nbs = mesample("?", s, j, k);
      vector<double> membp(me.num_classes());
      //        int label = nb.classify(nbs, NULL, &membp);
      //        me.classify(nbs, &membp);
      membp = me.classify(nbs);
      int label = 0;
      membp[other_class] -= BIAS_FOR_RECALL;
      for (int l = 0; l < me.num_classes(); l++) {
        if (membp[l] > membp[label]) label = l;
      }
      double prob = membp[label];
      /*
        print_features(fb, nbs);
        cout << endl << "------- ";
        for (int l = 0; l < me.num_classes(); l++) cout << membp[l] << " ";
        cout << endl;
      */
      if (label != other_class) {
        la.push_back(Annotation(label, j, k, prob));
      }
    }
  }
  la.sort();
  //    for (int j = 0; j < s.size(); j++) cout << j << ":" << s[j].str << " ";
  //    cout << endl;
  for (list<Annotation>::const_iterator j = la.begin(); j != la.end(); j++) {
    //      cout << j->label << " begin = " << j->begin << " end = " << j->end << " prob = " << j->prob << endl;
    bool override = true;
    for (int l = j->begin; l < j->end; l++) {
      if (label_p[l] >= j->prob) { override = false; break; }
      if (s[l].ne != string("O")) {
        // erase the old label
        int lbegin = l;
        while (s[lbegin].ne[0] != 'B') lbegin--;
        int lend = l;
        while (s[lend].ne[0] != 'O' && lend < s.size()) lend++;
        for (int t = lbegin; t < lend; t++) {
          s[t].ne = string("O");
          label_p[t] = 0;
        }
      }
    }
    if (!override) continue;
    for (int l = j->begin; l < j->end; l++) {
      label_p[l] = j->prob;
      if (l == j->begin)  s[l].ne = "B-" + me.get_class_label(j->label);
      else                s[l].ne = "I-" + me.get_class_label(j->label);
    }
  }
}


ME_Model ne_model;

void load_ne_models()
{
  string model_file = "./models_named_entity/model001";
  string wordinfo_file = "./models_named_entity/word_info";

  cerr << "loading named_entity_models.";
  ne_model.load_from_file(model_file);
  cerr << ".";
  load_word_info(wordinfo_file);
  cerr << "done." << endl;
}


int netagging(vector<Token> & vt)
{

  find_NEs(ne_model, vt);

  
  return 0;
}

