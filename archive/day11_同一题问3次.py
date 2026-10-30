from day06_files import ChatBot

bot = ChatBot()
for i in range(3):
    a = bot.ask_with_files("升档要连续几天不断档？", f"stab_{i}")
    print(f"{i+1}: {a!r}")
