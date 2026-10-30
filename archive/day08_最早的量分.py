from day06_files import ChatBot
from eval_cases import cases

bot = ChatBot()

for mode in["raw", "norm", "sqrt"]:
    right = len(cases)
    for i ,c in enumerate(cases, 1):
        hit = bot.retrieve(c["q"], bot.chunks, mode, k=1)
        ok = c["expect"] in hit
        print(f"{'✓' if ok else '✗'} 第{i}题[{c['type']}] {c['q']}")
        if not ok:
            right-=1
            print(f"    期望来自 {c['expect']}")
            print(f"    实际选中 {hit[:40]}...")
    print(f"{mode:6s} {right} / {len(cases)}")
#2026-10-27
#学了：测评检索
#卡在：归一化
