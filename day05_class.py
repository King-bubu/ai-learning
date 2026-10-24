from openai import OpenAI

docs = [
    "我的电脑是联想拯救者，CPU 是 i7-13620H，10 核 16 线程，内存 16 GB。显卡是 RTX 5060 Laptop，显存 8151 MiB。",
    "我的学习档位分三档：最低档 2.5 小时，标准档 4 小时，满档 6 到 7 小时。连续 5 天不断档才可以升一档。",
    "我的 GitHub 用户名是 King-bubu，学习仓库叫 ai-learning，每天一个可运行的练习，一天一次提交。",
]
class ChatBot:

    def __init__(self):
        self.model = "qwen2.5:3b"
        self.client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"
        )
        self.history=[]
    def ask(self, question):
        self.history.append({"role": "user", "content": question})
        resp = self.client.chat.completions.create(
            model = self.model,
            messages = self.history
        )
        answer = resp.choices[0].message.content
        self.history.append({"role": "assistant", "content": answer})
        return answer
    def bigrams(self, text):
        """把一段文字切成所有相邻两字的组合。'显卡显存' → {'显卡','卡显','显存'}"""
        return {text[i:i+2] for i in range(len(text) - 1)}
    def retrieve(self, question, docs):
        s=[]
        for i in range(len(docs)):
            score = len(self.bigrams(docs[i]) & self.bigrams(question))
            s.append((score, docs[i]))
        return max(s)[1]
    
    def ask_with_docs(self, question, docs):
        context = self.retrieve(question,docs)
        prompt = """请只根据下面这段资料回答问题。资料里没有的内容，就回答「资料里没有」。
            资料：{context}
            问题：{question}"""
        return self.ask(prompt)
        
bot = ChatBot()
print(bot.ask("用一句话解释：在编程里，类和对象的区别是什么"))
print(bot.ask("我叫小明，记住"))
print(bot.ask("我叫什么名字？"))

a = ChatBot()      # 没有资料的 bot
b = ChatBot()      # 有资料可查的 bot

print("A(瞎猜):", a.ask("我的显卡显存有多大？"))
print("B(有资料):", b.ask_with_docs("我的显卡显存有多大？", docs))

#2026-10-24
#学了：类里面的魔法调用函数__init__()
#卡在：1为什么第一个def不需要主动调用就可执行；2history和messages