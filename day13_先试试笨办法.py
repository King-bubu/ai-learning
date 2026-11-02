"""Day 13 第 1 关：先用最笨的办法判分，看它怎么错。

我们想干嘛：判断「它的回答对不对」。
最直觉的判法：写的标准答案，和它答的一模一样，就算对。

跑法：python day13_先试试笨办法.py
"""
from day06_files import ChatBot

bot = ChatBot()

Q = "升档要连续几天不断档？"
EXPECTED = "升档需要连续5天不断档"          # 我自己写的「标准答案」

for i in range(3):
    got = bot.ask_with_files(Q, f"笨办法{i}")
    print(f"第 {i+1} 次：{got}")
    print(f"    和标准答案一模一样吗？ {got == EXPECTED}")
    print()
