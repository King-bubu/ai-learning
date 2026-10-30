from day06_files import ChatBot
from eval_cases import cases

bot = ChatBot()
for k in (1, 2, 3, 4):
    bad = []
    for i, c in enumerate(cases, 1):
        if c["expect"] not in bot.retrieve(c["q"], bot.chunks, k=k):
            bad.append(i)
    print(f"k={k}  {10-len(bad)}/10  错{bad}")
