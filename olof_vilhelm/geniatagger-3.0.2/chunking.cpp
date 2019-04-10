/*
 * $Id: bidir.cpp,v 1.1 2005/09/04 13:33:10 tsuruoka Exp $
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

const int TAG_WINDOW_SIZE = 1;
const int BEAM_NUM = 1;
//const int BEAM_NUM = 10;
const double BEAM_WINDOW = 0.01;
const bool ONLY_VERTICAL_FEATURES = false;
//const bool DISTANT_FEATURES = false;

enum DecodingStrategy { LEFT_TO_RIGHT, RIGHT_TO_LEFT, EASIEST_FIRST};
const DecodingStrategy decoding_strategy = EASIEST_FIRST;
//const DecodingStrategy decoding_strategy = LEFT_TO_RIGHT;
//const DecodingStrategy decoding_strategy = RIGHT_TO_LEFT;

static ME_Sample
mesample(const vector<Token> &vt, int pos,
         const string & tag_left2,  const string & tag_left1, 
         const string & tag_right1, const string & tag_right2)
{
  ME_Sample sample;

  sample.label = vt[pos].tag;

  string w[5], p[5], t[5];

  w[0] = "BOS2";
  if (pos > 1) w[0] = vt[pos-2].str;
  w[1] = "BOS";
  if (pos > 0) w[1] = vt[pos-1].str;
  w[2] = vt[pos].str;
  w[3] = "EOS";
  if (pos < (int)vt.size()-1) w[3] = vt[pos+1].str;
  w[4] = "EOS2";
  if (pos < (int)vt.size()-2) w[4] = vt[pos+2].str;

  p[0] = "BOS2";
  if (pos > 1) p[0] = vt[pos-2].pos;
  p[1] = "BOS";
  if (pos > 0) p[1] = vt[pos-1].pos;
  p[2] = vt[pos].pos;
  p[3] = "EOS";
  if (pos < (int)vt.size()-1) p[3] = vt[pos+1].pos;
  p[4] = "EOS2";
  if (pos < (int)vt.size()-2) p[4] = vt[pos+2].pos;
  
  std::stringstream buf;
  // first-order 
  for (int i = 0; i < 5; i++) {
    buf << "W" << (i - 2) << "_" << w[i];
    sample.features.push_back(buf.str());
    buf.str("");
    buf << "P" << (i - 2) << "_" << p[i];
    sample.features.push_back(buf.str());
    buf.str("");
  }
  // bigram
  for (int i = 0; i < 4; i++) {
    int j = i + 1;
    buf << "P" << (i - 2) << "P" << (j - 2) << "_" << p[i] << "_" << p[j];
    sample.features.push_back(buf.str());
    buf.str("");
    buf << "W" << (i - 2) << "W" << (j - 2) << "_" << w[i] << "_" << w[j];
    sample.features.push_back(buf.str());
    buf.str("");
  }
  // pos trigram
  for (int i = 0; i < 3; i++) {
    int j = i + 1;
    int k = i + 2;
    buf << "P" << (i - 2) << "P" << (j - 2) << "P" << (k - 2) << "_" << p[i] << "_" << p[j] << "_" << p[k];
    sample.features.push_back(buf.str());
    buf.str("");
  }
  
  t[0] = tag_left2;
  t[1] = tag_left1;
  t[2] = "";  
  t[3] = tag_right1;
  t[4] = tag_right2;
  // first-order
  for (int i = 0; i < 5; i++) {
    //  for (int i = 1; i < 4; i++) {
    if (t[i] == "") continue;
    buf << "T" << (i - 2) << "_" << t[i];
    sample.features.push_back(buf.str());
    buf.str("");
  }

  // second-order
  for (int i = 0; i < 4; i++) {
    int j = i + 1;
    if (t[i] == "") continue;
    if (t[j] == "") continue;
    buf << "T" << (i - 2) << "T" << (j - 2) << "_" << t[i] << "_" << t[j];
    sample.features.push_back(buf.str());
    buf.str("");
  }

  if (t[1] != "" && t[3] != "") {
    buf << "T" << (1 - 2) << "T" << (3 - 2) << "_" << t[1] << "_" << t[3];
    sample.features.push_back(buf.str());
    buf.str("");
  }
  if (t[0] != "" && t[1] != "" && t[3] != "") {
    buf << "T" << (0 - 2) << "T" << (1 - 2) << "T" << (3 - 2) << "_" << t[0] << "_" << t[1] << "_" << t[3]; 
    sample.features.push_back(buf.str());
    buf.str("");
  }
  if (t[1] != "" && t[3] != "" && t[4] != "") {
    buf << "T" << (1 - 2) << "T" << (3 - 2) << "T" << (4 - 2) << "_" << t[1] << "_" << t[3] << "_" << t[4]; 
    sample.features.push_back(buf.str());
    buf.str("");
  }

  
  /*
  for (int j = 0; j < vt.size(); j++)
    cout << vt[j].str << "/" << vt[j].pos << " ";
  cout << endl;
  cout << pos << endl;
  for (list<string>::const_iterator j = sample.features.begin(); j != sample.features.end(); j++) {
    cout << *j << " ";
  }
  cout << endl << endl;
  */
  
  return sample;
}

static double entropy(const vector<double>& v)
{
  double sum = 0, maxp = 0;
  for (int i = 0; i < v.size(); i++) {
    if (v[i] == 0) continue;
    sum += v[i] * log(v[i]);
    maxp = max(maxp, v[i]);
  }
    return -sum;
}

struct Hypothesis
{
  vector<Token> vt;
  vector<double> vent;
  vector<int> order;
  //  vector<int> model;
  vector< vector<pair<string, double> > > vvp;
  double prob;
  bool operator<(const Hypothesis & h) const {
    return prob < h.prob;
  }
  Hypothesis(const vector<Token> & vt_,
             const vector<ME_Model> & vme)
  {
    prob = 1.0;
    vt = vt_;
    int n = vt.size();
    vent.resize(n);
    vvp.resize(n);
    order.resize(n);
    //    model.resize(n);
    for (size_t i = 0; i < n; i++) {
      vt[i].cprd = "";
      Update(i, vme);
    }
  }
  void Print()
  {
    for (size_t k = 0; k < vt.size(); k++) {
      cout << vt[k].str << "/";
      //      if (vt[k].cprd == "") cout << "?";
      cout << vt[k].cprd;
      cout << " ";
    }
    cout << endl;
  }
  void Update(const int j,
              const vector<ME_Model> & vme)
  {
    string tag_left1 = "BOS", tag_left2 = "BOS2";
    if (j >= 1) tag_left1 = vt[j-1].cprd; // maybe bug??
    //    if (j >= 1 && vt[j-1] != "") pos_left1 = vt[j-1].cprd; // this should be correct
    if (j >= 2) tag_left2 = vt[j-2].cprd;
    string tag_right1 = "EOS", tag_right2 = "EOS2";
    if (j <= int(vt.size()) - 2) tag_right1 = vt[j+1].cprd;
    if (j <= int(vt.size()) - 3) tag_right2 = vt[j+2].cprd;
    ME_Sample mes = mesample(vt, j, tag_left2, tag_left1, tag_right1, tag_right2);
    
    vector<double> membp;
    const ME_Model * mep = NULL;
    int bits = 0;
    if (TAG_WINDOW_SIZE >= 2 && tag_left2  != "") bits += 8;
    if (tag_left1  != "") bits += 4;
    if (tag_right1 != "") bits += 2;
    if (TAG_WINDOW_SIZE >= 2 && tag_right2 != "") bits += 1;
    assert(bits >= 0 && bits < 16);
    mep = &(vme[bits]);
    membp = mep->classify(mes);
    assert(mes.label != "");
    //cout << "(" << j << ", " << bits << ") ";

    double maxp = membp[mep->get_class_id(mes.label)];
    //    vector<double> tmpv(membp);
    //    sort(tmpv.begin(), tmpv.end());
    //    double second = tmpv[1];

    switch (decoding_strategy) {
    case EASIEST_FIRST:
      vent[j] = -maxp;
      //      vent[j] = maxp; // easiest last
      //      vent[j] = second / maxp;
      //      vent[j] = entropy(membp);
      break;
    case LEFT_TO_RIGHT:
      vent[j] = j;
      break;
    case RIGHT_TO_LEFT:
      vent[j] = -j;
      break;
    }

    vvp[j].clear();
    //    vp[j] = mes.label;
    for (int i = 0; i < mep->num_classes(); i++) {
      double p = membp[i];
      if (p > maxp * BEAM_WINDOW)
        vvp[j].push_back(pair<string, double>(mep->get_class_label(i), p));
    }
  }
  bool IsErroneous() const
  {
    for (int i = 0; i < vt.size()-1; i++) {
      const string & a = vt[i].cprd;
      const string & b = vt[i+1].cprd;
      if (a == "" || b == "") continue;
      //      if (a[0] == 'B' && b[0] == 'B') {
      //        if (a.substr(2) == b.substr(2)) return true;
      //      }
      if (b[0] == 'I') {
        if (a[0] == 'O') return true;
        if (a.substr(2) != b.substr(2)) return true;
      }
    }
    return false;
  }
};

void generate_hypotheses(const int order, const Hypothesis & h,
                         const vector<ME_Model> & vme,
                         list<Hypothesis> & vh)
{
  int n = h.vt.size();
  int pred_position = -1;
  double min_ent = 999999;
  string pred = "";
  double pred_prob = 0;
  for (int j = 0; j < n; j++) {
    if (h.vt[j].cprd != "") continue;
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
    
    newh.vt[pred_position].cprd = k->first;
    newh.order[pred_position] = order + 1;
    newh.prob = h.prob * k->second;

    //    if (newh.IsErroneous()) {
    //      cout << "*errorneous" << endl;
    //      newh.Print();
    //      continue;
    //    }
    
    // update the neighboring predictions
    for (int j = pred_position - TAG_WINDOW_SIZE; j <= pred_position + TAG_WINDOW_SIZE; j++) {
      if (j < 0 || j > n-1) continue;
      if (newh.vt[j].cprd == "") newh.Update(j, vme);
    }
    vh.push_back(newh);
  }


}

static void convert_startend_to_iob2_sub(vector<string> & s)
{
  for (int i = 0; i < s.size(); i++) {
    string tag = s[i];
    string newtag = tag;
    if (tag[0] == 'S') {
      newtag = "B" + tag.substr(1);
    }
    if (tag[0] == 'E') {
      newtag = "I" + tag.substr(1);
    }
    s[i] = newtag;
  }
}

void
bidir_chuning_decode_beam(vector<Token> & vt,
                  const vector<ME_Model> & vme)
{
  int n = vt.size();
  if (n == 0) return;

  list<Hypothesis> vh;
  Hypothesis h(vt, vme);
  vh.push_back(h);
  
  for (size_t i = 0; i < n; i++) {
    list<Hypothesis> newvh;
    for (list<Hypothesis>::const_iterator j = vh.begin(); j != vh.end(); j++) {
      generate_hypotheses(i, *j, vme, newvh);
    }
    newvh.sort();
    while (newvh.size() > BEAM_NUM) {
      newvh.pop_front();
    }
    vh = newvh;
  }

  if (!vh.empty()) {
    h = vh.back();
  } else {
    cerr << "warning: no hypothesis found" << endl;
    h = Hypothesis(vt, vme);
  }

  vector<string> tags;
  for (size_t k = 0; k < n; k++) {
    //    cout << h.vt[k].str << "/" << h.vt[k].cprd << "/" << h.order[k] << " ";
    tags.push_back(h.vt[k].cprd);
  }

  convert_startend_to_iob2_sub(tags);
  for (size_t k = 0; k < n; k++) {
    vt[k].cprd = tags[k];
  }
  
  
  //  cout << endl;
  

}
/*
void
bidir_chunking(vector<Sentence> & vs,
               const vector<ME_Model> & vme)
{
  cerr << "now tagging";

  int n = 0;
  int ntokens = 0;
  for (vector<Sentence>::iterator i = vs.begin(); i != vs.end(); i++) {
    Sentence & s = *i;
    ntokens += s.size();
    bidir_decode_beam(s, vme);
    //    bidir_decode_search(s, vme[0], vme[4], vme[2], vme[6]);
    //    decode_no_context(s, vme[0]);
    //    decode_l1(s, vme[4]);

    cout << n << endl;
    if (n++ % 10 == 0) cerr << ".";
  }
  cerr << endl;

  //  cerr << ntokens / (msec/1000.0) << " tokens / sec" << endl;
}
*/

/*
 * $Log: bidir.cpp,v $
 * Revision 1.1  2005/09/04 13:33:10  tsuruoka
 * chunker
 *
 */

