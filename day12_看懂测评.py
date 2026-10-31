"""把「一次测评」拆开给你看：它到底在比什么、k 又是在哪一步起作用。

这个脚本不测任何东西，它只是把测评内部的三个数字打出来：
  1. 我以为答案在哪一段（expect）
  2. 程序实际排出来的前 4 名是谁
  3. 取 1 段 / 取 2 段，分别是对还是错

跑法：python day12_看懂测评.py
"""
from day06_files import ChatBot
from eval_cases import cases
from eval_dev import dev_cases

bot = ChatBot()


def show(title, case):
    print("=" * 62)
    print(title)
    print("  问题：" + case["q"])
    print("  我认为答案在这一段，开头是：" + case["expect"])
    print()
    ranked = bot.score_all(case["q"], bot.chunks)
    for i, (sc, d) in enumerate(ranked[:4], 1):
        one_line = d[:26].replace("\n", " ")
        mark = "   ← 答案就在这一段" if case["expect"] in d else ""
        print(f"    第{i}名  {sc:>2} 分   {one_line}...{mark}")
    print()
    k1 = case["expect"] in ranked[0][1]
    k2 = any(case["expect"] in d for sc, d in ranked[:2])
    print("    只取 1 段（k=1）→ " + ("对" if k1 else "错"))
    print("    取前 2 段（k=2）→ " + ("对" if k2 else "错"))
    print()


show("例 1 · 标准题：答案本来就排第 1 名", cases[2])
show("例 2 · 关键题：答案排第 2 名，k=1 会把它漏掉", cases[5])
show("例 3 · 硬靶子：答案排第 4 名，k=2 也救不了", dev_cases[7])
