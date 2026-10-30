"""Day 11 小实验：资料错了，模型会跟着错吗？

这个脚本不改任何代码，只是把三种不同的「资料」塞给同一个 ask()，
看它对同一个问题会怎么答。

三组对照：
  A  真资料          显存 8151 MiB / RTX 5060
  B  假资料（改过的） 显存 4096 MiB / RTX 3060
  C  不给资料        纯靠模型自己的知识

跑法：python day11_fake.py
"""
from day06_files import ChatBot

bot = ChatBot()


def ask_with_context(question, context, sid):
    """把指定的一段资料拼进 prompt，再交给模型 —— 和 ask_with_files 里的做法一样，
       区别只是这里由我们说了算给哪一段。"""
    prompt = f"""请只根据下面这些资料回答问题。资料里没有的内容，就回答「资料里没有」。
            资料：{context}
            问题：{question}"""
    return bot.ask(prompt, sid)


# 找出写着 8151 的那段真资料
real = next(d for d in bot.chunks if "8151" in d)

# 在它上面改两个数字，其余一字不动
fake = real.replace("8151", "4096").replace("RTX 5060", "RTX 3060")

question = "我的显卡显存有多大？"

print("问题：", question)
print("=" * 64)

print("\n【A 组】给真资料")
print("  资料里写的是：" + real[:70].replace("\n", " ") + " ...")
print("  回答 →", ask_with_context(question, real, "A"))

print("\n" + "=" * 64)
print("\n【B 组】给假资料（把 8151 改成 4096，RTX 5060 改成 RTX 3060）")
print("  资料里写的是：" + fake[:70].replace("\n", " ") + " ...")
print("  回答 →", ask_with_context(question, fake, "B"))

print("\n" + "=" * 64)
print("\n【C 组】不给资料，直接问")
print("  回答 →", bot.ask(question, "C"))

print("\n" + "=" * 64)
