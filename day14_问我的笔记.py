"""Day 14：问我自己写的东西 —— 不用题库，我自己知道答得对不对。"""
from day06_files import ChatBot

bot = ChatBot()

问题们 = [
    "什么是MRR?",   # 填一个你昨天真的忘了的名词
    "push失败了怎么办?",   # 填一个你昨天真的卡住的操作
    "day8学了什么?",   # 填一个关于我自己学习进度的问题
]

for i, q in enumerate(问题们, 1):
    print("=" * 60)
    print(f"问 {i}：{q}")
    print("答：" + bot.ask_with_files(q, f"自用{i}"))
    print()
#2026-11-04
#学了：接进全部 md 后段数 309→1878，检索反而退化；raw 偏爱长段、sqrt 偏爱短标题，同一个根因
#做了：load_chunks 改读全部 md，ask_with_files 改 sqrt + k=5，三条自测全对，MRR 能答了
#卡在：问「day8学了什么」检出前 5 名全是标题，按空行切段让标题和内容分了家
