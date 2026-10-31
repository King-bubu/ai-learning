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
            self.stopwords = ["我", "的", "了", "怎么办", "什么"]      # 只放语义虚词
            self.markers   = ["问", "答"]                       # 文档格式标记，换文档要重看
            self.punct     = "，。？！：、；（）「」《》——…\n\t .,?!:;()[]{}"   # 标点，一个字符集
    def clean(self, text):
        """只负责清理：去行首标记、去空格、去标点、去停用词"""
        lines = []
        for line in text.split("\n"):
            s = line.lstrip()
            for m in self.markers:
                if s.startswith(m + "："):          # ← 你补：把 s 的前缀切掉
                    s = s[len(m)+1:]
            lines.append(s)
        text = "\n".join(lines)
        text = text.replace(" ", "")
        table = str.maketrans("", "", self.punct)
        text = text.translate(table)
        for w in self.stopwords:
            text = text.replace(w, "")
        return text
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
            messages = history,
            temperature=0
        )
        answer = resp.choices[0].message.content
        history.append({"role": "assistant", "content": answer})
        self.sessions[session_id] = history
        return answer
    def bigrams(self, text):
        """把一段文字切成所有相邻两字的组合。'显卡显存' → {'显卡','卡显','显存'}"""
        return {text[i:i+2] for i in range(len(text) - 1)}
    def score_all(self, question, docs, mode="raw"):
        q=self.bigrams(self.clean(question))
        s = []
        for i in docs:
            d = self.bigrams(self.clean(i))
            hit = len(d & q)
            if mode == "raw":
                score = hit
            elif mode == "norm":
                score = hit/len(d)
            elif mode == "sqrt":
                score = hit/(len(d)**0.5)
            else:
                raise ValueError(f"未知的 mode: {mode}")
            s.append((score, i))
        return sorted(s, key=lambda x: x[0], reverse = True)
    def retrieve(self, question, docs, mode="raw", k=2):
        """返回最相关的 k 段，用换行拼成一个字符串"""
        ranked = self.score_all(question, docs, mode)
        top = ranked[:k] 
        return "\n---\n".join(d for sc, d in top)

    def build_prompt(self, question, context):
        """只负责拼 prompt，不碰模型、不碰检索"""
        prompt = ("请只根据下面这些资料回答问题。资料里没有的内容，就回答「资料里没有」。\n"
                f"资料：{context}\n"
                f"问题：{question}")
        return prompt

    def ask_with_files(self, question, session_id):
        context = self.retrieve(question, self.chunks, k=2)
        prompt = self.build_prompt(question, context)
        return self.ask(prompt, session_id)
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