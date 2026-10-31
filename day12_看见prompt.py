from day06_files import ChatBot

bot = ChatBot()
q = "升档要连续几天不断档？"
ctx = bot.retrieve(q, bot.chunks, k=2)
print(bot.build_prompt(q, ctx))
#2026-10-31
#学了：从ask_with_files里拆出build_prompt
#卡在：改了措辞结果没变，其实是我动错了地方
