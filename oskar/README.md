# Coreference Resolution

## Introduction

## Paper
https://www.overleaf.com/read/xfdmhbzwshty


## Installation of SpanBERT for coreference resolution.

1. First install the coref folder from mandarjoshi.
! git clone https://github.com/mandarjoshi90/coref.git
%cd coref

2. Temporary hack to fix dependencies. 
! sed 's/MarkupSafe==1.0/MarkupSafe==1.1.1/; s/scikit-learn==0.19.1/scikit-learn==0.21/; s/scipy==1.0.0/scipy==1.6.2/' < requirements.txt > tmp
! mv tmp requirements.txt

! sed 's/.D.GLIBCXX.USE.CXX11.ABI.0//' < setup_all.sh  > tmp
! mv tmp setup_all.sh 
! chmod u+x setup_all.sh 

3. Install Tensorflow 
% tensorflow_version 2.x
! pip uninstall -y tensorflow
! pip install -r requirements.txt --log install-log.txt -q
! ./setup_all.sh
