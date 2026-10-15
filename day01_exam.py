import pandas as pd
df = pd.read_csv("data/成绩数据.csv")

print(df.head(5))#1


print(df.shape[0])
print(df.shape[1])#2



print(df.groupby("班级")["Python成绩"].mean())#3


print(df.sort_values(by="Python成绩", ascending=False).head(5))#4


r=df[["高数成绩","英语成绩","Python成绩"]].corr(numeric_only=True)
print(r)#5


import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
df1 = df.groupby("班级")["Python成绩"].mean()
plt.bar(df1.index, df1.values)
plt.xlabel("班级")
plt.ylabel("Python成绩")
plt.title("三个班的Python平均分")
plt.show()#6


plt.scatter(df["出勤率"], df["Python成绩"])
plt.xlabel("出勤率")
plt.ylabel("Python成绩")
plt.title("出勤率 vs Python成绩")
plt.show()#7

#8出勤率和Python成绩没有明显关系