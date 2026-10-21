from openai import OpenAI#从 openai 这个库里，把 OpenAI 这个类搬出来。​ 类你可以先理解成「一个能造东西的模板」。OpenAI 大写是因为它是类名。
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)#造一个客户端对象，叫 client。​ 两个参数：base_url：告诉它「模型服务在哪」。你本机 Ollama 的地址就是这个 。api_key：本地不校验，随便填，但这个参数必须有，不然报错
messages = [{"role": "user", "content": "你好，我叫小明"}]
resp1 = client.chat.completions.create(
    model="qwen2.5:3b",
    messages=messages
)
answer1 = resp1.choices[0].message.content
messages.append({"role": "assistant", "content": answer1})
messages.append({"role": "user", "content": "我叫什么名字"})
#发一次请求，把返回结果存进 resp。​ 这一行最长，拆三块看：
#client.chat.completions.create(...) —— 这串是「调用聊天接口」的固定写法，记住这个链式结构，所有 OpenAI 兼容接口都这么调
#model：用哪个模型
#messages：对话内容，一个列表里塞字典，每条字典是「谁说了什么」。role: "user" = 你说的，content = 具体内容
resp2 = client.chat.completions.create(
    model="qwen2.5:3b",
    messages=messages
)
answer2 = resp2.choices[0].message.content
print(answer1)
print(answer2)
