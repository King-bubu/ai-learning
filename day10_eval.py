# day10_eval.py —— 统一评测脚本：一次跑 dev 和 test，两套指标并排看
#
# 为什么要有这个脚本：
#   以前你每换一次配置，就要改一遍 day10_mrr.py。
#   现在配置变了，只跑这一个脚本，dev 和 test 的数字一起出来。
#
#   但记住规矩：**调参只看 dev，报数才看 test。**
#   两个数字并排显示，是为了让你看见"dev 涨了 test 没涨"这种过拟合。

from day06_files import ChatBot
from eval_cases import cases as test_cases
from eval_dev import dev_cases


def evaluate(bot, cases, k=2, verbose=True):
    """在 cases 上评测。返回 (命中率, MRR, 每题排名列表)。

    expect 为 None 的题是"资料里没有"型，检索层没法判对错，跳过不计分。
    """
    hit = 0
    total = 0.0
    ranks = []
    counted = 0

    for i, c in enumerate(cases, 1):
        if c["expect"] is None:
            if verbose:
                print(f"  {i:2d}. ——  生成层题，检索层不评   {c['q']}")
            continue

        ranked = bot.score_all(c["q"], bot.chunks)
        rank = next(
            (j for j, (sc, d) in enumerate(ranked, 1) if c["expect"] in d),
            99,
        )
        counted += 1
        ranks.append(rank)

        if rank <= k:
            hit += 1
            total += 1.0 / rank

        if verbose:
            mark = "✓" if rank == 1 else ("△" if rank <= k else "✗")
            print(f"  {i:2d}. {mark} 排第 {rank:2d}   {c['q']}")

    if counted == 0:
        return 0.0, 0.0, ranks
    return hit / counted, total / counted, ranks


def report(bot, name, cases, k=2):
    print(f"\n===== {name}｜{len(cases)} 题｜k={k} =====")
    hit, mrr, ranks = evaluate(bot, cases, k=k)
    print(f"  → 命中率 hit@{k} = {hit:.2f}   MRR@{k} = {mrr:.4f}")
    return hit, mrr


if __name__ == "__main__":
    bot = ChatBot()

    print("当前配置：")
    print(f"  stopwords = {bot.stopwords}")
    print(f"  markers   = {bot.markers}")
    print(f"  chunks    = {len(bot.chunks)} 段")

    report(bot, "dev（调参用）", dev_cases, k=2)
    report(bot, "test（冻结，只报数）", test_cases, k=2)

    print("\n" + "-" * 55)
    print("提醒：dev 涨了 test 没涨 = 过拟合。dev 和 test 都涨才算改对了。")
