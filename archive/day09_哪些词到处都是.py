from collections import Counter
from day06_files import ChatBot

bot = ChatBot()

df=Counter()
for chunk in bot.chunks:
    for bg in set(bot.bigrams(chunk)):
        df[bg]+=1
print("总段数", len(bot.chunks))
for bg, n in df.most_common(25):
    print(f"{bg} 出现在{n}段")
