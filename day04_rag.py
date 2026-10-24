#1. RAG解决的问题:会幻觉 —— 一本正经答错，还自带解释。   
#知识有截止日期 —— 训练完之后新发生的事它不知道，想更新就得重训。
#细节被压缩磨平了 —— 知识全泡在参数里，只能模糊联想，没法精确查询。
#2.解决上述问题的办法：prompt = 资料 + 问题
#3.Retrieval 检索 从资料里挑出相关的几段      
# Augmented 增强 增强的是这次输入，不是模型     
# Generation 生成 模型看着“资料+问题”生成答案
from openai import OpenAI
docs = [
    "我的电脑是联想拯救者，CPU 是 i7-13620H，10 核 16 线程，内存 16 GB。显卡是 RTX 5060 Laptop，显存 8151 MiB。",
    "我的学习档位分三档：最低档 2.5 小时，标准档 4 小时，满档 6 到 7 小时。连续 5 天不断档才可以升一档。",
    "我的 GitHub 用户名是 King-bubu，学习仓库叫 ai-learning，每天一个可运行的练习，一天一次提交。",
]

question = "我的显卡显存有多大？"
def bigrams(text):
    """把一段文字切成所有相邻两字的组合。'显卡显存' → {'显卡','卡显','显存'}"""
    return {text[i:i+2] for i in range(len(text) - 1)}
def retrieve(question, docs):
    """从 docs 里挑出跟 question 最相关的那一段"""
    s=[]
    for i in range(len(docs)):
        score = len(bigrams(docs[i]) & bigrams(question))
        s.append((score, docs[i]))
    return max(s)[1]
    # ① 遍历 docs，用 bigrams 算每段和 question 有多少个两字组合撞上了
    # ② 挑出分数最高的那一段
    # ③ return 那一段的下标
    pass
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
messages1 = [{"role": "user", "content": question}]
resp1 = client.chat.completions.create(
    model="qwen2.5:3b",
    messages=messages1
)
answer1 = resp1.choices[0].message.content
print(answer1)
context = retrieve(question, docs)
prompt = f"""请只根据下面这段资料回答问题。资料里没有的内容，就回答「资料里没有」。
资料：{context}
问题：{question}"""
messages2 = [{"role": "user", "content": prompt}]
resp2 = client.chat.completions.create(
    model="qwen2.5:3b",
    messages=messages2
)
answer2 = resp2.choices[0].message.content
print(answer2)
#2026-10-23
#学了：了解了RAG，RAG = 检索出资料塞进 prompt；模型参数没变，变的只是这次输入
#卡在：第一次看论文，看了好几遍，不认真逐句解析看不懂，朴素检索在小语料上永远"看起来对"，看不出质量问题