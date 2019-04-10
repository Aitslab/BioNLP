/*
 * $Id: postag.cpp,v 1.5 2004/12/21 13:54:46 tsuruoka Exp $
 */

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

const double BEAM_WIDTH = 3.0;
//const double BEAM_WIDTH = 6.0;

/*
struct ConfusingWordTable
{
  static const char * wl[];
  set<string> words;
  ConfusingWordTable() {
    for (int i = 0;; i++) {
      if (wl[i] == "///") break;
      words.insert(wl[i]);
    }
  }
  bool IsConfusing(const string & s) {
    if (words.find(s) != words.end()) return true;
    return false;
  }
};

const char * ConfusingWordTable::wl[] = {
  "about", "that", "off", "more", "up", "'s", "in", "down", "much", "as", "all",
  "on", "out", "around", "will", "over", "///"
};

static ConfusingWordTable confusing_word_table;
*/

void
tokenize(const string & s1, list<string> & lt);


string
normalize(const string & s)
{
  string tmp(s);
  for (size_t i = 0; i < tmp.size(); i++) {
    if (isdigit(tmp[i])) tmp[i] = '#';
  }
  return tmp;
}

ME_Sample
mesample(const vector<Token> &vt, int i, const string & prepos)
         //         const string & prepos2)
{
  ME_Sample sample;

  string str = vt[i].str;

  sample.label = normalize(vt[i].pos);

  sample.features.push_back("W0_" + str);
  string prestr = "BOS";
  if (i > 0) prestr = normalize(vt[i-1].str);
  string prestr2 = "BOS2";
  if (i > 1) prestr2 = normalize(vt[i-2].str);
  string poststr = "EOS";
  if (i < (int)vt.size()-1) poststr = normalize(vt[i+1].str);
  string poststr2 = "EOS2";
  if (i < (int)vt.size()-2) poststr2 = normalize(vt[i+2].str);
  sample.features.push_back("W-1_" + prestr);
  sample.features.push_back("W+1_" + poststr);

  //  sample.features.push_back("W-2_" + prestr2);
  //  sample.features.push_back("W+2_" + poststr2);
  
  //  string e_prestr  = "^^^" + prestr;
  //  string e_str     = "^^^" + str;
  //  string e_poststr = "^^^" + poststr;
  //  sample.features.push_back("W-1+1_" + prestr + "_" + poststr);

  sample.features.push_back("W-10_" + prestr + "_" + str);
  sample.features.push_back("W0+1_" + str  + "_" + poststr);
  //  sample.features.push_back("W-10_" + e_prestr.substr(e_prestr.size()-3) + "_" + e_str.substr(e_str.size()-3));
  //  sample.features.push_back("W0+1_" + e_str.substr(e_str.size()-3)  + "_" + e_poststr.substr(e_poststr.size()-3));

  //  if (str[str.size() - 1] == 's')
  //    sample.features.push_back("suf1_s");
  
  if (str.size() >= 3)
    sample.features.push_back("suf2_" + str.substr(str.size() - 2));
  if (str.size() >= 4)
    sample.features.push_back("suf3_" + str.substr(str.size() - 3));
  if (str.size() >= 5)
    sample.features.push_back("suf4_" + str.substr(str.size() - 4));
  if (str.size() >= 6)
    sample.features.push_back("suf5_" + str.substr(str.size() - 5));
  //  if (str.size() >= 3)
  //    sample.features.push_back("pre3_" + str.substr(0, 3));

  sample.features.push_back("P-1_" + prepos);
  //  sample.features.push_back("P-2-1_" + prepos2 + "_" + prepos);
  //  sample.features.push_back("W-2P-1_" + prestr2 + "_" + prepos);

  //  sample.features.push_back("W-1P-1_" + prestr  + "_" + prepos);
  sample.features.push_back("P-1W0_"  + prepos + "_" + str);
  //  sample.features.push_back("W+1P-1_" + poststr + "_" + prepos);

  //  sample.features.push_back("W-2_" + prestr2);
  //  sample.features.push_back("W+2_" + poststr2);
  
  //  if (isupper(str[0]) && prepos != "BOS")
  //  if (i > 0 && isupper(str[0]))
  if (isupper(str[0]))
    sample.features.push_back("ISUPPER");
  //    sample.features.push_back("ISUPPER_AND_NOT_BOS");

  /*
  if (confusing_word_table.IsConfusing(str)) {
    //    sample.features.push_back("W-10_" + prestr + "_" + str);
    //    sample.features.push_back("W0+1_" + str  + "_" + poststr);
    sample.features.push_back("P-1W0+1_" + prepos + "_" + str  + "_" + poststr);
  }
  */


  /*
  for (int j = 0; j < vt.size(); j++)
    cout << vt[j].str << " ";
  cout << endl;
  cout << i << endl;
  for (list<string>::const_iterator j = sample.features.begin(); j != sample.features.end(); j++) {
    cout << *j << " ";
  }
  cout << endl << endl;
  */
  
  return sample;
}

void
viterbi(vector<Token> & vt, const ME_Model & me)
{
  if (vt.size() == 0) return;
  
  vector< vector<double> > mat;
  vector< vector<int> > bpm;
    
  vector<double> vd(me.num_classes());
  for (size_t j = 0; j < vd.size(); j++) vd[j] = 0;

  mat.push_back(vd);

  for (size_t i = 0; i < vt.size(); i++) {

    vector<double> vd(me.num_classes());
    for (size_t j = 0; j < vd.size(); j++) vd[j] = -999999;
    vector<int> bp(me.num_classes());

    double maxl = -999999;
    for (size_t j = 0; j < vd.size(); j++) {
      if (mat[i][j] > maxl) maxl = mat[i][j];
    }
    
    for (size_t j = 0; j < vd.size(); j++) {
      if (mat[i][j] < maxl - BEAM_WIDTH) continue; // beam thresholding
      
      string prepos = me.get_class_label(j);
      if (i == 0) {
        if (j > 0) continue;
        prepos = "BOS";
      }
      //      prepos = me.get_class_name(j);
      //      if (i == 0 && prepos != "BOS") continue;

      ME_Sample mes = mesample(vt, i, prepos);
      vector<double> membp = me.classify(mes);
      for (size_t k = 0; k < vd.size(); k++) {
        double l = mat[i][j] + log(membp[k]);
        if (l > vd[k]) {
          bp[k] = j;
          vd[k] = l;
        }
      }
    }
    mat.push_back(vd);
    //    for (int k = 0; k < vd.size(); k++) cout << bp[k] << " ";
    //    cout << endl;
    bpm.push_back(bp);
  }
  /*
  for (int i = 0; i < vt.size(); i++) {
    int max_prd = 0;
    for (int j = 0; j < vd.size(); j++) {
      double l = mat[i+1][j];
      if (l > mat[i+1][max_prd]) {
        max_prd = j;
      }
    }
    vt[i].prd = me.get_class_name(max_prd);
  }
  */  

  //  cout << "viterbi ";
  int max_prd = 0;
  int n = vt.size();
  for (size_t j = 0; j < vd.size(); j++) {
    double l = mat[n][j];
    if (l > mat[n][max_prd]) {
      max_prd = j;
    }
  }
  vt[n-1].prd = me.get_class_label(max_prd);
  for (int i = vt.size() - 2; i >= 0; i--) {
    //    cout << max_prd << " ";
    //    cerr << max_prd << " ";
    if (max_prd < 0 || max_prd >= me.num_classes()) exit(0);
    max_prd = bpm[i+1][max_prd];
    vt[i].prd = me.get_class_label(max_prd);
  }
  //  cout << endl;

}

/*
string postag(const string & s, const ME_Model & me)
{
  list<string> lt;
  tokenize(s, lt);

  vector<Token> vt;
  for (list<string>::const_iterator i = lt.begin(); i != lt.end(); i++) {
    vt.push_back(Token(*i, "?"));
  }
  
  viterbi(vt, me);

  string tmp;
  for (size_t i = 0; i < vt.size(); i++) {
    if (i == 0) tmp += vt[i].str + "/" + vt[i].prd;
    else        tmp += " " + vt[i].str + "/" + vt[i].prd;
  }
  return tmp;
}
*/

/*
 * $Log: postag.cpp,v $
 * Revision 1.5  2004/12/21 13:54:46  tsuruoka
 * add bidir.cpp
 *
 * Revision 1.4  2004/12/20 12:06:24  tsuruoka
 * change the data
 *
 * Revision 1.3  2004/07/29 12:40:33  tsuruoka
 * modify features
 *
 * Revision 1.2  2004/07/26 03:46:48  tsuruoka
 * add confusing_word_table
 *
 * Revision 1.1  2004/07/16 13:40:42  tsuruoka
 * init
 *
 */

