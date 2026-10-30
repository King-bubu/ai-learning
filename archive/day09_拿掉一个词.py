"""day9 消融实验：一次跑完所有停用词组合，输出对照表。

消融实验（ablation）= 把某个东西拿掉，看指标掉多少。
拿掉之后不掉分的东西，就是没在干活的东西。
"""
from itertools import combinations
from day06_files import ChatBot
from eval_cases import cases

bot = ChatBot()
ALL = ["我", "的", "了", "怎么办"]


def run(sw):
    """用指定的停用词表跑一遍评测，返回（分数，错题号列表）"""
    bot.stopwords = sw
    bad = []
    for i, c in enumerate(cases, 1):
        got = bot.retrieve(c["q"], bot.chunks, "raw", k = 1)
        if c["expect"] not in got:
            bad.append(i)
    return 10 - len(bad), bad


print("=" * 66)
print("表 B：每个词覆盖多少段（在没 clean 的原文上数）")
print("=" * 66)
for w in ALL:
    n = sum(1 for c in bot.chunks if w in c)
    print(f"  {w:6s} 覆盖 {n}/{len(bot.chunks)} 段")

print()
print("=" * 66)
print("表 C：留一法（leave-one-out）—— 从 4 个里去掉 1 个，剩 3 个")
print("=" * 66)
base_score, base_bad = run(ALL)
print(f"  {'基线（4 个全留）':16s} {str(ALL):32s} {base_score}/10  错{base_bad}")
for w in ALL:
    rest = [x for x in ALL if x != w]
    sc, bad = run(rest)
    delta = sc - base_score
    tag = "← 掉分了，它在干活" if delta < 0 else "← 不掉分，白留"
    print(f"  {'去掉「' + w + '」':16s} {str(rest):32s} {sc}/10  错{bad}  {delta:+d} {tag}")

print()
print("=" * 66)
print("表 D：全部 16 种组合（留一法只是其中 5 行）")
print("=" * 66)
bot.stopwords = ALL
for r in range(len(ALL) + 1):
    for sw in combinations(ALL, r):
        sc, bad = run(list(sw))
        print(f"  {sc}/10  {str(list(sw)):40s} 错{bad}")

bot.stopwords = ALL  # 还原，别把 demo 的改动留进下一次
print()
print("已还原 stopwords =", bot.stopwords)
#2026-10-28
#学了：消融实验——拿掉它掉不掉分
#卡在：
