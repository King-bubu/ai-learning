"""Day 12 第 3 关：只改 prompt 里的措辞，看模型行为怎么变。

三组对照，问的都是资料里绝对没有的问题（杭州天气）。
资料完全相同（同一个问题检索出来的同一份），唯一的差别在 prompt 的两处：

    ① 限定词    请「只」根据  /  请参考
    ② 兜底句    有没有「资料里没有就说没有」

注意：这里故意不用 build_prompt —— 因为实验要动的就是措辞本身，
      用固定措辞的方法就改不了了。

跑法：python day12_三组措辞.py
"""
from day06_files import ChatBot

bot = ChatBot()

QUESTION = "杭州今天天气怎么样？"
ctx = bot.retrieve(QUESTION, bot.chunks, k=2)      # 三组共用这一份资料


def make_prompt(rule, fallback=True):
    """rule = 限定词；fallback = 要不要那句退路"""
    tail = "资料里没有的内容，就回答「资料里没有」。" if fallback else ""
    return (
        f"{rule}下面这些资料回答问题。{tail}\n"
        f"资料：{ctx}\n"
        f"问题：{QUESTION}"
    )


groups = [
    ("A 组", "请只根据", True),
    ("B 组", "请参考   ", True),
    ("C 组", "请参考   ", False),
]

for i, (name, rule, fallback) in enumerate(groups, 1):
    print("=" * 68)
    print(f"{name}　限定词：{rule}　兜底句：{'有' if fallback else '删掉了'}")
    print("-" * 68)
    print("提问：" + QUESTION)
    print("回答：" + bot.ask(make_prompt(rule, fallback), f"措辞{i}"))
    print()
