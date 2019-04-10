/*
 * $Id: common.h,v 1.1 2004/12/21 13:54:45 tsuruoka Exp $
 */

#ifndef __POSTAGGER_COMMON_H_
#define __POSTAGGER_COMMON_H_

#include <string>
#include <vector>

struct Token
{
  std::string str;
  std::string pos;
  std::string prd;
  std::string cprd;// for chunking
  std::string tag; // for chunking
  std::string ne;
  Token(std::string s, std::string p) : str(s), pos(p) {}
};

typedef std::vector<Token> Sentence;


#endif

/*
 * $Log: common.h,v $
 * Revision 1.1  2004/12/21 13:54:45  tsuruoka
 * add bidir.cpp
 *
 */
