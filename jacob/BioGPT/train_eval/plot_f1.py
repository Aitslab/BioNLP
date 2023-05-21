#encoding utf8

import matplotlib.pyplot as plt
import json
import pandas as pd

entity = "cell"
epoch = "10"

infile= f'/proj/berzelius-2021-21/users/rafsan/alvis/rafsan/biobert_main/pytorch-biobert/biobert_pytorch_retrain/job_{entity}_epochs_{epoch}/train.out'
outpath = "res/plots_f1"

df_train=pd.DataFrame()
df_eval=pd.DataFrame()
with open(infile,encoding="utf8") as f:
    lines=f.readlines()

for line in lines:
    line=line.strip().replace("'","\"")
    d = json.loads(line)
    if "loss" in d:
        df_train=df_train.append(d,ignore_index=True)
    elif "eval_loss" in d:
        df_eval=df_eval.append(d,ignore_index=True)
    else:
        print(d)
            
#df_train.to_csv("out_train_res.tsv", sep="\t", index=None)        
#df_eval.to_csv("out_eval_res.tsv",sep="\t",index=None)
df_eval["rev_loss"] = 1-df_eval["eval_loss"]
#plt.figure(figsize=(15,10))
plt.plot(df_train["epoch"].tolist(), df_train["loss"].tolist(), label="train loss",linewidth=0.5)
plt.plot(df_eval["epoch"].tolist(), df_eval["eval_loss"].tolist(), label="eval loss",linewidth=0.5)
plt.plot(df_eval["epoch"].tolist(), df_eval["eval_f1"].tolist(), label="F1",linewidth=0.5)
plt.plot(df_eval["epoch"].tolist(), df_eval["rev_loss"].tolist(), label="1-eval loss",linewidth=0.5)
plt.legend()
plt.xlabel("train epochs")
plt.ylabel("parameters")
#plt.show()
plt.savefig(f'{outpath}/{entity}_epoch{epoch}_loss_f1_plot.eps',format="eps")    
