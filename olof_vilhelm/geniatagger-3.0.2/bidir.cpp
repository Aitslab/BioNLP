/*
 * $Id: bidir.cpp,v 1.9 2005/09/01 14:16:30 tsuruoka Exp $
 */

#include <sys/time.h>
#include <stdio.h>
#include <fstream>
#include <map>
#include <list>
#include <iostream>
#include <sstream>
#include <cmath>
#include <set>
#include "maxent.h"
#include "common.h"

using namespace std;

const int UPDATE_WINDOW_SIZE = 2;
//const int BEAM_NUM = 10;
const int BEAM_NUM = 1;
const double BEAM_WINDOW = 0.01;
//const double BEAM_WINDOW = 0.9;
const bool ONLY_VERTICAL_FEATURES = false;

//extern string normalize(const string & s);
void tokenize(const string & s1, list<string> & lt);
string base_form(const string & s, const string & pos);

void bidir_chuning_decode_beam(vector<Token> & vt, const vector<ME_Model> & vme);

static ME_Sample
mesample(const vector<Token> &vt, int i,
         const string & pos_left2, const string & pos_left1, 
         const string & pos_right1, const string & pos_right2)
{
  ME_Sample sample;

  string str = vt[i].str;

  sample.label = vt[i].pos;

  sample.features.push_back("W0_" + str);
  string prestr = "BOS";
  if (i > 0) prestr = vt[i-1].str;
  //  string prestr2 = "BOS2";
  //  if (i > 1) prestr2 = normalize(vt[i-2].str);
  string poststr = "EOS";
  if (i < (int)vt.size()-1) poststr = vt[i+1].str;
  //  string poststr2 = "EOS2";
  //  if (i < (int)vt.size()-2) poststr2 = normalize(vt[i+2].str);

  if (!ONLY_VERTICAL_FEATURES) {
    sample.features.push_back("W-1_" + prestr);
    sample.features.push_back("W+1_" + poststr);

    sample.features.push_back("W-10_" + prestr + "_" + str);
    sample.features.push_back("W0+1_" + str  + "_" + poststr);
  }

  stringstream buf;
  for (int j = 1; j <= 10; j++) {
    //    char buf[1000];
    if (str.size() >= j) {
      //      sprintf(buf, "suf%d_%s", j, str.substr(str.size() - j).c_str());
      //      sample.features.push_back(buf);
      buf << "suf" << j << "_" << str.substr(str.size() - j);
      sample.features.push_back(buf.str());
      buf.str("");
    }
    if (str.size() >= j) {
      //      sprintf(buf, "pre%d_%s", j, str.substr(0, j).c_str());
      //      sample.features.push_back(buf);
      buf << "pre" << j << "_" << str.substr(0, j);
      sample.features.push_back(buf.str());
      buf.str("");
    }
  }
  // L
  if (pos_left1 != "") {
    sample.features.push_back("P-1_" + pos_left1);
    sample.features.push_back("P-1W0_"  + pos_left1 + "_" + str);
  }
  // L2
  if (pos_left2 != "") {
    sample.features.push_back("P-2_" + pos_left2);
  }
  // R
  if (pos_right1 != "") {
    sample.features.push_back("P+1_" + pos_right1);
    sample.features.push_back("P+1W0_"  + pos_right1 + "_" + str);
  }
  // R2
  if (pos_right2 != "") {
    sample.features.push_back("P+2_" + pos_right2);
  }
  // LR
  if (pos_left1 != "" && pos_right1 != "") {
    sample.features.push_back("P-1+1_" + pos_left1 + "_" + pos_right1);
    sample.features.push_back("P-1W0P+1_"  + pos_left1 + "_" + str + "_" + pos_right1);
  }
  // LL
  if (pos_left1 != "" && pos_left2 != "") {
    sample.features.push_back("P-2-1_" + pos_left2 + "_" + pos_left1);
    //    sample.features.push_back("P-1W0_"  + pos_left + "_" + str);
  }
  // RR
  if (pos_right1 != "" && pos_right2 != "") {
    sample.features.push_back("P+1+2_" + pos_right1 + "_" + pos_right2);
    //    sample.features.push_back("P-1W0_"  + pos_left + "_" + str);
  }
  // LLR
  if (pos_left1 != "" && pos_left2 != "" && pos_right1 != "") {
    sample.features.push_back("P-2-1+1_" + pos_left2 + "_" + pos_left1 + "_" + pos_right1);
    //    sample.features.push_back("P-1W0_"  + pos_left + "_" + str);
  }
  // LRR
  if (pos_left1 != "" && pos_right1 != "" && pos_right2 != "") {
    sample.features.push_back("P-1+1+2_" + pos_left1 + "_" + pos_right1 + "_" + pos_right2);
    //    sample.features.push_back("P-1W0_"  + pos_left + "_" + str);
  }
  // LLRR
  if (pos_left2 != "" && pos_left1 != "" && pos_right1 != "" && pos_right2 != "") {
    sample.features.push_back("P-2-1+1+2_" + pos_left2 + "_" + pos_left1 + "_" + pos_right1 + "_" + pos_right2);
    //    sample.features.push_back("P-1W0_"  + pos_left + "_" + str);
  }

  for (int j = 0; j < str.size(); j++) {
    if (isdigit(str[j])) {
      sample.features.push_back("CONTAIN_NUMBER");
      break;
    }
  }
  for (int j = 0; j < str.size(); j++) {
    if (isupper(str[j])) {
      sample.features.push_back("CONTAIN_UPPER");
      break;
    }
  }
  for (int j = 0; j < str.size(); j++) {
    if (str[j] == '-') {
      sample.features.push_back("CONTAIN_HYPHEN");
      break;
    }
  }

  bool allupper = true;
  for (int j = 0; j < str.size(); j++) {
    if (!isupper(str[j])) {
      allupper = false;
      break;
    }
  }
  if (allupper)
    sample.features.push_back("ALL_UPPER");


  //  for (int j = 0; j < vt.size(); j++)
  //    cout << vt[j].str << " ";
  //  cout << endl;
  //  cout << i << endl;
  //  for (list<string>::const_iterator j = sample.features.begin(); j != sample.features.end(); j++) {
  //    cout << *j << " ";
  //  }
  //  cout << endl << endl;
  
  return sample;
}

/*****************************
////////////////////////////////////////////////////////////////////
//// Toutanova feature
////////////////////////////////////////////////////////////////////
static ME_Sample
mesample(const vector<Token> &vt, int i,
         const string & pos_left2, const string & pos_left1, 
         const string & pos_right1, const string & pos_right2)
{
  ME_Sample sample;

  string str = vt[i].str;

  sample.label = vt[i].pos;

  sample.features.push_back("W0_" + str);
  string prestr = "BOS";
  if (i > 0) prestr = vt[i-1].str;
  //  string prestr2 = "BOS2";
  //  if (i > 1) prestr2 = normalize(vt[i-2].str);
  string poststr = "EOS";
  if (i < (int)vt.size()-1) poststr = vt[i+1].str;
  //  string poststr2 = "EOS2";
  //  if (i < (int)vt.size()-2) poststr2 = normalize(vt[i+2].str);

  if (!ONLY_VERTICAL_FEATURES) {
    sample.features.push_back("W-1_" + prestr);
    sample.features.push_back("W+1_" + poststr);

    sample.features.push_back("W-10_" + prestr + "_" + str);
    sample.features.push_back("W0+1_" + str  + "_" + poststr);
  }

  for (int j = 1; j <= 10; j++) {
    char buf[1000];
    if (str.size() >= j) {
      sprintf(buf, "suf%d_%s", j, str.substr(str.size() - j).c_str());
      sample.features.push_back(buf);
    }
    if (str.size() >= j) {
      sprintf(buf, "pre%d_%s", j, str.substr(0, j).c_str());
      sample.features.push_back(buf);
    }
  }
  // L
  if (pos_left1 != "") {
    sample.features.push_back("P-1_" + pos_left1);
    sample.features.push_back("P-1W0_"  + pos_left1 + "_" + str);
  }

  // L2
  //  if (pos_left2 != "") {
  //    sample.features.push_back("P-2_" + pos_left2);
  //  }

  // R
  if (pos_right1 != "") {
    sample.features.push_back("P+1_" + pos_right1);
    sample.features.push_back("P+1W0_"  + pos_right1 + "_" + str);
  }

  // R2
  //  if (pos_right2 != "") {
  //    sample.features.push_back("P+2_" + pos_right2);
  //  }

  // LR
  if (pos_left1 != "" && pos_right1 != "") {
    sample.features.push_back("P-1+1_" + pos_left1 + "_" + pos_right1);
    //    sample.features.push_back("P-1W0P+1_"  + pos_left1 + "_" + str + "_" + pos_right1);
  }
  // LL
  if (pos_left1 != "" && pos_left2 != "") {
    sample.features.push_back("P-2-1_" + pos_left2 + "_" + pos_left1);
    //    sample.features.push_back("P-1W0_"  + pos_left + "_" + str);
  }
  // RR
  if (pos_right1 != "" && pos_right2 != "") {
    sample.features.push_back("P+1+2_" + pos_right1 + "_" + pos_right2);
    //    sample.features.push_back("P-1W0_"  + pos_left + "_" + str);
  }

  // LLR
  //  if (pos_left1 != "" && pos_left2 != "" && pos_right1 != "") {
  //    sample.features.push_back("P-2-1+1_" + pos_left2 + "_" + pos_left1 + "_" + pos_right1);
  //    //    sample.features.push_back("P-1W0_"  + pos_left + "_" + str);
  //  }
  // LRR
  //  if (pos_left1 != "" && pos_right1 != "" && pos_right2 != "") {
  //    sample.features.push_back("P-1+1+2_" + pos_left1 + "_" + pos_right1 + "_" + pos_right2);
  //    //    sample.features.push_back("P-1W0_"  + pos_left + "_" + str);
  //  }
  // LLRR
  //  if (pos_left2 != "" && pos_left1 != "" && pos_right1 != "" && pos_right2 != "") {
  //    sample.features.push_back("P-2-1+1+2_" + pos_left2 + "_" + pos_left1 + "_" + pos_right1 + "_" + pos_right2);
  //    //    sample.features.push_back("P-1W0_"  + pos_left + "_" + str);
  //  }

  bool contain_number = false;
  for (int j = 0; j < str.size(); j++) {
    if (isdigit(str[j])) {
      sample.features.push_back("CONTAIN_NUMBER");
      contain_number = true;
      break;
    }
  }
  bool contain_upper = false;
  for (int j = 0; j < str.size(); j++) {
    if (isupper(str[j])) {
      sample.features.push_back("CONTAIN_UPPER");
      contain_upper = true;
      break;
    }
  }
  bool contain_hyphen = false;
  for (int j = 0; j < str.size(); j++) {
    if (str[j] == '-') {
      sample.features.push_back("CONTAIN_HYPHEN");
      contain_hyphen = true;
      break;
    }
  }
  if (contain_number && contain_upper && contain_hyphen) {
    sample.features.push_back("CONTAIN_NUMBER_UPPER_HYPHEN");
  }
  if (contain_upper) {
    bool company = false;
    for (int j = i + 1; j <= i + 3; j++) {
      if (j >= vt.size()) continue;
      if (vt[j].str == "Co.") company = true;
      if (vt[j].str == "Inc.") company = true;
      if (vt[j].str == "Corp.") company = true;
    }
    if (company)
      sample.features.push_back("CRUDE_COMPANY_NAME");
  }

  bool allupper = true;
  for (int j = 0; j < str.size(); j++) {
    if (!isupper(str[j])) {
      allupper = false;
      break;
    }
  }
  if (allupper)
    sample.features.push_back("ALL_UPPER");

  //  for (int j = 0; j < vt.size(); j++)
  //    cout << vt[j].str << " ";
  //  cout << endl;
  //  cout << i << endl;
  //  for (list<string>::const_iterator j = sample.features.begin(); j != sample.features.end(); j++) {
  //    cout << *j << " ";
  //  }
  //  cout << endl << endl;
    
  return sample;
}
*****************************/


static double entropy(const vector<double>& v)
{
  double sum = 0, maxp = 0;
  for (int i = 0; i < v.size(); i++) {
    if (v[i] == 0) continue;
    sum += v[i] * log(v[i]);
    maxp = max(maxp, v[i]);
  }
  return -maxp;
    return -sum;
}

int
bidir_train(const vector<Sentence> & vs, int para)
{
  //  vme.clear();
  //  vme.resize(16);

  for (int t = 0; t < 16; t++) {
    if (t != 15 && t != 0) continue;
  //  for (int t = 15; t >= 0; t--) {
    vector<ME_Sample> train;

    if (para != -1 && t % 4 != para) continue;
    //    if (t % 2 == 1) continue;
    cerr << "type = " << t << endl;
    cerr << "extracting features...";
    int n = 0;
    for (vector<Sentence>::const_iterator i = vs.begin(); i != vs.end(); i++) {
      const Sentence & s = *i;
      for (int j = 0; j < s.size(); j++) {

        string pos_left1 = "BOS", pos_left2 = "BOS2";
        if (j >= 1) pos_left1 = s[j-1].pos;
        if (j >= 2) pos_left2 = s[j-2].pos;
        string pos_right1 = "EOS", pos_right2 = "EOS2";
        if (j <= int(s.size()) - 2) pos_right1 = s[j+1].pos;
        if (j <= int(s.size()) - 3) pos_right2 = s[j+2].pos;
        if ( (t & 0x8) == 0 ) pos_left2 = "";
        if ( (t & 0x4) == 0 ) pos_left1 = "";
        if ( (t & 0x2) == 0 ) pos_right1 = "";
        if ( (t & 0x1) == 0 ) pos_right2 = "";

        train.push_back(mesample(s, j, pos_left2, pos_left1, pos_right1, pos_right2));
      }
      //      if (n++ > 1000) break;
    }
    cerr << "done" << endl;

    ME_Model m;
    //    m.set_heldout(1000,0);
    //    m.train(train, 2, 1000, 0);
    m.train(train, 2, 0, 1);
    char buf[1000];
    sprintf(buf, "model.bidir.%d", t);
    m.save_to_file(buf);
    
  }

}

struct Hypothesis
{
  vector<Token> vt;
  vector<double> vent;
  vector<int> order;
  vector< vector<pair<string, double> > > vvp;
  double prob;
  bool operator<(const Hypothesis & h) const {
    return prob < h.prob;
  }
  Hypothesis(const vector<Token> & vt_,
             const multimap<string, string> & tagdic,
             const vector<ME_Model> & vme)
  {
    prob = 1.0;
    vt = vt_;
    int n = vt.size();
    vent.resize(n);
    vvp.resize(n);
    order.resize(n);
    for (size_t i = 0; i < n; i++) {
      vt[i].prd = "";
      Update(i, tagdic, vme);
    }
  }
  void Print()
  {
    for (size_t k = 0; k < vt.size(); k++) {
      cout << vt[k].str << "/";
      if (vt[k].prd == "") cout << "?";
      else cout << vt[k].prd;
      cout << " ";
    }
    cout << endl;
  }
  void Update(const int j,
              const multimap<string, string> & tagdic,
              const vector<ME_Model> & vme)
  {
    string pos_left1 = "BOS", pos_left2 = "BOS2";
    if (j >= 1) pos_left1 = vt[j-1].prd; // maybe bug??
    //    if (j >= 1 && vt[j-1] != "") pos_left1 = vt[j-1].prd; // this should be correct
    if (j >= 2) pos_left2 = vt[j-2].prd;
    string pos_right1 = "EOS", pos_right2 = "EOS2";
    if (j <= int(vt.size()) - 2) pos_right1 = vt[j+1].prd;
    if (j <= int(vt.size()) - 3) pos_right2 = vt[j+2].prd;
    ME_Sample mes = mesample(vt, j, pos_left2, pos_left1, pos_right1, pos_right2);
    
    vector<double> membp;
    const ME_Model * mep = NULL;
    int bits = 0;
    if (pos_left2  != "") bits += 8;
    if (pos_left1  != "") bits += 4;
    if (pos_right1 != "") bits += 2;
    if (pos_right2 != "") bits += 1;
    assert(bits >= 0 && bits < 16);
    mep = &(vme[bits]);
    membp = mep->classify(mes);
    assert(mes.label != "");
    vent[j] = entropy(membp);
    //    vent[j] = -j;

    vvp[j].clear();
    double maxp = membp[mep->get_class_id(mes.label)];
    //    vp[j] = mes.label;
    for (int i = 0; i < mep->num_classes(); i++) {
      double p = membp[i];
      if (p > maxp * BEAM_WINDOW)
        vvp[j].push_back(pair<string, double>(mep->get_class_label(i), p));
    }
    /*
      if (tagdic.find(vt[j].str) != tagdic.end()) {
      // known words
      string max_tag = "";
      double max = 0;
      for (multimap<string, string>::const_iterator i = tagdic.lower_bound(vt[j].str);
      i != tagdic.upper_bound(vt[j].str); i++) {
      double p = membp[mep->get_class_id(i->second)];
      if (p > max) {
      max = p;
      max_tag = i->second;
      }
      }
      vp[j] = max_tag;
      } else {
      // unknown words
      vp[j] = mes.label;
      //    vent[j] += 99999;
      }
    */
  }
};


void generate_hypotheses(const int order, const Hypothesis & h,
                         const multimap<string, string> & tag_dictionary,
                         const vector<ME_Model> & vme,
                         list<Hypothesis> & vh)
{
  int n = h.vt.size();
  int pred_position = -1;
  double min_ent = 999999;
  string pred = "";
  double pred_prob = 0;
  for (int j = 0; j < n; j++) {
    if (h.vt[j].prd != "") continue;
    double ent = h.vent[j];
    if (ent < min_ent) {
      //        pred = h.vvp[j].begin()->first;
      //        pred_prob = h.vvp[j].begin()->second;
      min_ent = ent;
      pred_position = j;
    }
  }
  assert(pred_position >= 0 && pred_position < n);

  for (vector<pair<string, double> >::const_iterator k = h.vvp[pred_position].begin();
       k != h.vvp[pred_position].end(); k++) {
    Hypothesis newh = h;
    
    newh.vt[pred_position].prd = k->first;
    newh.order[pred_position] = order + 1;
    newh.prob = h.prob * k->second;
  
    // update the neighboring predictions
    for (int j = pred_position - UPDATE_WINDOW_SIZE; j <= pred_position + UPDATE_WINDOW_SIZE; j++) {
      if (j < 0 || j > n-1) continue;
      if (newh.vt[j].prd == "") newh.Update(j, tag_dictionary, vme);
    }
    vh.push_back(newh);
  }


}

void
bidir_decode_beam(vector<Token> & vt,
                  const multimap<string, string> & tag_dictionary,
                  const vector<ME_Model> & vme)
{
  int n = vt.size();
  if (n == 0) return;

  list<Hypothesis> vh;
  Hypothesis h(vt, tag_dictionary, vme);
  vh.push_back(h);
  
  for (size_t i = 0; i < n; i++) {
    list<Hypothesis> newvh;
    for (list<Hypothesis>::const_iterator j = vh.begin(); j != vh.end(); j++) {
      generate_hypotheses(i, *j, tag_dictionary, vme, newvh);
    }
    newvh.sort();
    while (newvh.size() > BEAM_NUM) {
      newvh.pop_front();
    }
    vh = newvh;
  }

  h = vh.back();
  for (size_t k = 0; k < n; k++) {
    //    cout << h.vt[k].str << "/" << h.vt[k].prd << "/" << h.order[k] << " ";
    vt[k].prd = h.vt[k].prd;
  }
  //  cout << endl;
  

}

static void
decode_no_context(vector<Token> & vt, const ME_Model & me_none)
{
  int n = vt.size();
  if (n == 0) return;

  for (size_t i = 0; i < n; i++) {
    ME_Sample mes = mesample(vt, i, "", "", "", "");
    me_none.classify(mes);
    vt[i].prd = mes.label;
  }
  
  for (size_t k = 0; k < n; k++) {
    cout << vt[k].str << "/" << vt[k].prd << " ";
  }
  cout << endl;

}

class ParenConverter
{
  map<string, string> ptb2pos;
  map<string, string> pos2ptb;
public:
  ParenConverter() {
    const static char* table[] = {
      "-LRB-", "(",
      "-RRB-", ")",
      "-LSB-", "[",
      "-RSB-", "]",
      "-LCB-", "{",
      "-RCB-", "}", 
      "***", "***", 
    };

    for (int i = 0;; i+=2) {
      if (string(table[i]) == "***") break;
      ptb2pos.insert(make_pair(table[i], table[i+1]));
      pos2ptb.insert(make_pair(table[i+1], table[i]));
    }
  }
  string Ptb2Pos(const string & s) {
    map<string, string>::const_iterator i = ptb2pos.find(s);
    if (i == ptb2pos.end()) return s;
    return i->second;
  }
  string Pos2Ptb(const string & s) {
    map<string, string>::const_iterator i = pos2ptb.find(s);
    if (i == pos2ptb.end()) return s;
    return i->second;
  }
};

ParenConverter paren_converter;

extern int netagging(vector<Token> & vt);

string
bidir_postag(const string & s, const vector<ME_Model> & vme, const vector<ME_Model> & chunking_vme, bool dont_tokenize)
{
  list<string> lt;
  if (dont_tokenize) {
    istringstream is(s);
    string token;
    while (is >> token) lt.push_back(token);
  } else {
    tokenize(s, lt);
  }

  vector<Token> vt;
  for (list<string>::const_iterator i = lt.begin(); i != lt.end(); i++) {
    string s = *i;
    //    s = paren_converter.Ptb2Pos(s);
    vt.push_back(Token(s, "?"));
  }
  
  const multimap<string, string> dummy;
  //  bidir_decode_search(vt, dummy, vme);
  bidir_decode_beam(vt, dummy, vme);
  for (size_t i = 0; i < vt.size(); i++) {
    vt[i].pos = vt[i].prd;
  }

  bidir_chuning_decode_beam(vt, chunking_vme);
  
  netagging(vt);

  string tmp;
  for (size_t i = 0; i < vt.size(); i++) {
    string s = vt[i].str;
    string p = vt[i].prd;
    //    s = paren_converter.Pos2Ptb(s);
    //    p = paren_converter.Pos2Ptb(p);
    /*
    if (i == 0) tmp += s + "/" + p;
    else        tmp += " " + s + "/" + p;
    */
    tmp += s + "\t";
    tmp += base_form(s, p) + "\t";
    tmp += p + "\t";
    tmp += vt[i].cprd + "\t";
    tmp += vt[i].ne + "\n";
  }
  return tmp;
}



int push_stop_watch()
{
  static struct timeval start_time, end_time;
  static bool start = true;
  if (start) {
    gettimeofday(&start_time, NULL);
    start = false;
    return 0;
  }

  gettimeofday(&end_time, NULL);
  int elapse_msec = (end_time.tv_sec - start_time.tv_sec) * 1000 +
    (int)((end_time.tv_usec - start_time.tv_usec) * 0.001);
  cerr << elapse_msec << " msec" << endl;
  start = true;
  return elapse_msec;
}

void
bidir_postagging(vector<Sentence> & vs,
                 const multimap<string, string> & tag_dictionary,
                 const vector<ME_Model> & vme)
{
  int num_classes = vme[0].num_classes();

  cerr << "now tagging";
  push_stop_watch();
  int n = 0, ntokens = 0;
  for (vector<Sentence>::iterator i = vs.begin(); i != vs.end(); i++) {
    Sentence & s = *i;
    ntokens += s.size();
    //    if (s.size() > 2) continue;
    bidir_decode_beam(s, tag_dictionary, vme);
    //bidir_decode_search(s, tag_dictionary, vme);
    //decode_no_context(s, vme[0]);

    cout << n << endl;
    /*
    for (size_t k = 0; k < s.size(); k++) {
      cout << s[k].str << "/" << s[k].prd << " ";
    }
    cout << endl;
    */
    //    if (n > 100) break;
    
    if (n++ % 10 == 0) cerr << ".";
  }
  cerr << endl;
  int msec = push_stop_watch();
  cerr << ntokens / (msec/1000.0) << " tokens / sec" << endl;
}


/*
 * $Log: bidir.cpp,v $
 * Revision 1.9  2005/09/01 14:16:30  tsuruoka
 * add hashfun_str
 * add stop_watch
 *
 * Revision 1.8  2005/02/16 10:45:39  tsuruoka
 * acl05 submit
 *
 * Revision 1.7  2005/01/12 07:32:39  tsuruoka
 * cyclic: windowsize 1 -> 2
 *
 * Revision 1.6  2005/01/10 13:44:00  tsuruoka
 * add beam
 *
 * Revision 1.5  2004/12/30 10:34:55  tsuruoka
 * add bidir_decode_search
 *
 * Revision 1.4  2004/12/25 11:22:04  tsuruoka
 * map -> hash_map
 *
 * Revision 1.3  2004/12/25 10:48:02  tsuruoka
 * use tag_dictionary in bidir_decode_deterministic()
 *
 * Revision 1.2  2004/12/25 09:23:09  tsuruoka
 * add classification_cache
 *
 * Revision 1.1  2004/12/21 13:54:46  tsuruoka
 * add bidir.cpp
 *
 */

