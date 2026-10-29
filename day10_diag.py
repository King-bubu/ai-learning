# day10_diag.py —— 逐题诊断器：某道题为什么错
#
# 用法：
#   python day10_diag.py           自动扫 test 集，诊断所有排名 > 2 的题
#   python day10_diag.py 3 5       只看第 3、5 题
#   python day10_diag.py dev       自动扫 dev 集里的错题
#   python day10_diag.py dev 4     看 dev 集第 4 题
#
# 和 day10_eval.py 的分工：
#   eval 告诉你「哪几题错了」（一个数字）
#   diag 告诉你「为什么错」（切字、命中词、分数来源）

import sys
from day06_files import ChatBot
from eval_cases import cases as test_cases
from eval_dev import dev_cases


def diag_one(bot, i, c, topn=3):
    """诊断一道题：问题怎么切、top-N 是哪些段、每段靠哪些词得分。"""
    print("=" * 66)
    print(f"第{i}题：{c['q']}")
    print(f"期望：{c['expect']!r}")

    qb = bot.bigrams(bot.clean(c["q"]))
    print(f"问题切出({len(qb)}): {' '.join(sorted(qb))}")

    ranked = bot.score_all(c["q"], bot.chunks)
    rank = next((j for j, (sc, d) in enumerate(ranked, 1) if c["expect"] in d), 99)
    top = ranked[0][0]
    tie = sum(1 for sc, _ in ranked if sc == top)
    print(f"→ 正确段排第 {rank}｜最高分 {top:g}｜并列 {tie} 段")

    for j, (sc, d) in enumerate(ranked[:topn], 1):
        inter = qb & bot.bigrams(bot.clean(d))
        mark = "  ← 正确" if c["expect"] in d else ""
        print(f"  {j}. {sc:g}分  命中{sorted(inter)}  {d[:34]!r}{mark}")


def rank_of(bot, c):
    """某题的正确答案排第几。找不到就是 99。"""
    ranked = bot.score_all(c["q"], bot.chunks)
    return next((j for j, (sc, d) in enumerate(ranked, 1) if c["expect"] in d), 99)


def main():
    args = sys.argv[1:]
    bot = ChatBot()

    if args and args[0] == "dev":
        pool, name = dev_cases, "dev"
        args = args[1:]
    else:
        pool, name = test_cases, "test"

    if args:
        ids = [int(a) for a in args]
    else:
        # 不传题号：自动挑出所有错题（排名 > 2）
        ids = [i for i, c in enumerate(pool, 1) if c["expect"] and rank_of(bot, c) > 2]
        if not ids:
            print(f"{name} 集没有错题（全部排前 2），没什么可诊断的。")
            return
        print(f"{name} 集共有 {len(ids)} 道错题：{ids}")

    for i in ids:
        diag_one(bot, i, pool[i - 1])


if __name__ == "__main__":
    main()
#2026-10-29
#学了：停用词表修不好检索,MRR平均倒数排名，建了dev集
#卡在：给dev集出题