from llama_cpp import Llama
import numpy as np

llm = Llama(model_path = '/home/adam/stego/tinyllama-1.1b-chat-v1.0-q4_k_m.gguf',
            logits_all = True,
            n_gpu_layers=0,
            n_threads=2,
            verbose=False)
llm.reset()

inp = input("Enter your text: ")
sec_key = input("Enter secret key: ")
# Converting input to binary
data = inp.encode(encoding="utf-8");
inp_binary = ''.join(format(byte, '08b') for byte in data)
print(inp_binary)

llm.eval(llm.tokenize(sec_key.encode("utf-8")))

logits_scr = llm.scores[llm.n_tokens - 1]


def top2():
    logits = np.array(llm.scores[llm.n_tokens - 1], dtype=np.float64)
    order = np.argsort(-logits)
    return int(order[0]), int(order[1])

shifted = logits - logits.max()   # защита от переполнения
weights = np.exp(shifted)          # оценки → положительные веса
probs = weights / weights.sum()    # нормировка, сумма = 1

top_logits = np.argsort(-probs)[:10]

for i, tid in enumerate(top_logits, 1):
    piece = llm.detokenize([int(tid)]).decode("utf-8", errors="replace")
    print(f"{i:>3} {int(tid):>7} {probs[tid]*100:>9.4f}%  {piece!r}")

