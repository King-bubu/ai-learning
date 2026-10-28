from day06_files import ChatBot
from eval_cases import cases

bot = ChatBot()
for i, c in enumerate(cases,1):
    ranked = bot.score_all(c["q"], bot.chunks)
    top = ranked[0][0]                                  # 最高分
    r = c["expect"]
    rank = 0
    tie = sum(1 for sc, _ in ranked if sc == top)         # 并列几段
    for  m, n in enumerate(ranked,1):
        if r in n[1]:
            rank = m
            break
    print(f"第{i}题  最高分{top}  并列{tie}段  正确段排第{rank}")