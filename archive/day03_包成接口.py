from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel
app = FastAPI()
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
class ChatRequest(BaseModel):
    question: str
@app.get("/health")
def health():
    return {"status": "ok"}
@app.post("/chat")
def chat(req: ChatRequest):
    messages = [{"role": "user", "content": req.question}]
    resp = client.chat.completions.create(
        model="qwen2.5:3b",
        messages=messages
    )
    answer = resp.choices[0].message.content
    return {"answer": answer}
#日志 2026-10-22
#学了：1.接口的本质，以前只能自己的电脑运行，现在任何程序都能通过网络来调用
#2.@app.post("/chat")是登记，不是现在调用
#3.代码中函数体需要请求才会调用
#4.只要写一个BaseModel的类，FastAPI就会自动校验不合格直接422
#卡在：服务停了没发现，脚本报ConnectionError