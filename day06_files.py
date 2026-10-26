from openai import OpenAI
from pathlib import Path
class ChatBot:
    def __init__(self):
            self.model = "qwen2.5:3b"
            self.client = OpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama"
            )
            self.sessions = {}
            self.chunks = self.load_chunks()
    def load_chunks(self):
        """读 docs/ 下所有 txt,按空行切段,返回一个列表"""
        chunks = []
        for path in Path("docs").glob("*.txt"):
            text = path.read_text(encoding="utf-8")
            paras = text.split("\n\n")
            for i in paras:
                if i.strip() != "":
                    chunks.append(i)
        if len(chunks) == 0:
            raise FileNotFoundError("⚠️ 启动失败:docs 里没有可用资料\n请检查 docs 文件夹是否和脚本在同一个目录下。")
        return chunks
    def ask(self, question, session_id):
        history = self.sessions.get(session_id, [])
        history.append({"role": "user", "content": question})
        resp = self.client.chat.completions.create(
            model = self.model,
            messages = history
        )
        answer = resp.choices[0].message.content
        history.append({"role": "assistant", "content": answer})
        self.sessions[session_id] = history
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
    def ask_with_files(self, question, session_id):
        """先检索、再拼 prompt、再回答"""
        context = self.retrieve(question, self.chunks)      # 1. 从 self.chunks 里检索出最相关的一段
        prompt = f"""请只根据下面这段资料回答问题。资料里没有的内容，就回答「资料里没有」。
            资料：{context}
            问题：{question}"""        # 2. 拼 prompt（昨天那句「资料里没有就说资料里没有」别忘了）
        return self.ask(prompt, session_id)     # 3. return self.ask(prompt)
if __name__ == "__main__":
    try:
        bot = ChatBot()
        print("共", len(bot.chunks), "段")
        print(bot.ask_with_files("我的显卡显存有多大？", "小豪"))# 应：8151 MiB
        print(bot.ask_with_files("升档要连续几天不断档？", "小豪")) # 应：5 天
        print(bot.ask_with_files("push 失败了怎么办？", "小豪"))# 应：先重试一到两次
    except FileNotFoundError as e:
        print(e)
#2026-10-25
#学了：用python读取docs文档，读取text文件，raise主动提出报错，搞懂了它的用法，复习了try
#卡在：如何读取文件，except和raise联合使用