# Coreference Resolution

## Introduction

## Paper
https://www.overleaf.com/read/xfdmhbzwshty


## Data
In the project we are using the UCDenver [CRAFT corpus](https://github.com/UCDenver-ccp/craft-shared-tasks).


## Installation of SpanBERT for coreference resolution on colab.

**Reference:** Jonathan K. Kummerfeld's Notebook. 

**1. Install the coref tool from mandarjoshi90.**
```
! git clone https://github.com/mandarjoshi90/coref.git
%cd coref
```

**2. Dependency Fix.**
```
! sed 's/MarkupSafe==1.0/MarkupSafe==1.1.1/; s/scikit-learn==0.19.1/scikit-learn==0.21/; s/scipy==1.0.0/scipy==1.6.2/' < requirements.txt > tmp
! mv tmp requirements.txt

! sed 's/.D.GLIBCXX.USE.CXX11.ABI.0//' < setup_all.sh  > tmp
! mv tmp setup_all.sh 
! chmod u+x setup_all.sh 
```

**3. Install Tensorflow**
```
% tensorflow_version 2.x
! pip uninstall -y tensorflow
! pip install -r requirements.txt --log install-log.txt -q
! ./setup_all.sh
```


## Installation of SpanBERT for coreference resolution on Centos7 Cluster 

**1.Versions**

Python 3.6.8
Anaconda3 2020.11

**2. Install the coref tool from mandarjoshi90.**
```
! git clone https://github.com/mandarjoshi90/coref.git
%cd coref
```

**3. Install missbehaving & missing packets**
```
pip install psycopg2-binary
pip install h5py
pip install nltk
```

**4. CUDA & cuDNN**
```
# For the cluster to work: if your running localy you can dowload these yourself.
conda install cudatoolkit=10.0.130
conda install cudnn=7.6.0
```

**5. Run requirments.txt**
Use the modified version in this repository.

```
pip install --no-cache-dir --no-build-isolation -r requirements.txt --log install-log.txt -q
```

**6. Run Setup **
```
./setup_all.sh
```
