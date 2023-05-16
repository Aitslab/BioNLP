import matplotlib.pyplot as plt
import pandas as pd
import json

df_train=pd.DataFrame()
df_eval=pd.DataFrame()
list_eval=[]
with open("train.out", encoding="utf8") as f:
    for line in f.readlines():
        line=line.strip().replace("'","\"")
        d = json.loads(line)
        if "loss" in d:
            df_train=df_train.append(d,ignore_index=True)
        elif "eval_loss" in d:
            df_eval=df_eval.append(d,ignore_index=True)
        else:
            print(d)

df_train.to_csv("out_train_res.tsv", sep="\t", index=None)        
df_eval.to_csv("out_eval_res.tsv",sep="\t",index=None)

#plt.figure(figsize=(15,10))
plt.plot(df_train["epoch"].tolist(), df_train["loss"].tolist(), label="train",linewidth=0.5)
plt.plot(df_eval["epoch"].tolist(), df_eval["eval_loss"].tolist(), label="evaluation",linewidth=0.5)
plt.legend()
plt.xlabel("train epochs")
plt.ylabel("training loss")
#plt.show()
plt.savefig("loss_plot.eps",format="eps")
