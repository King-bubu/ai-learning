from fastapi import FastAPI
from day06_files import ChatBot      # ← 注意这一行
from pydantic import BaseModel

bot = ChatBot()
app = FastAPI()

class AskRequest(BaseModel):
    question: str
    session_id: str

@app.get("/health")
def health():
    return {"status": "ok"}
@app.post("/askf")
def askf(req: AskRequest):
    return {"answer":bot.ask_with_files(req.question, req.session_id)}
@app.post("/ask")
def ask(req: AskRequest):
    return {"answer":bot.ask(req.question, req.session_id)}
#2026-10-26
#学了：if __name__ == "__main__":怎么用； 把 `ChatBot` 包成 HTTP 服务；撞上「多用户串号」，用session_id历史本去修好，更加清楚三件代码之间的联系，grep
# 卡在：加入历史本，有多处参数要加， 复制代码出现&#8203；