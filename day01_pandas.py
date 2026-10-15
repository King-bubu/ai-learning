import pandas as pd
df =pd.read_csv("data/成绩数据.csv")

print(df.head(2))
print(df.tail(2))
print(df.info())
print(df.shape)

print(df["学号"])
print(df.loc[1])
print(df.iloc[3])

print(df[df["高数成绩"]>60])

df.groupby("班级")["高数成绩"].mean()
df.groupby("性别")["高数成绩"].mean()

df.sort_values(by="高数成绩",ascending=False).head(3)