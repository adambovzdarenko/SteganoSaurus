from llama_cpp import Llama
import numpy as np

MODEL_PATH = '/home/adam/stego/tinyllama-1.1b-chat-v1.0-q4_k_m.gguf'
PROMPT = "Today the weather is"
N_CTX = 2048

llm = Llama(model_path = '/home/adam/stego/tinyllama-1.1b-chat-v1.0-q4_k_m.gguf',
            logits_all = True,
            n_gpu_layers=0,
            n_threads=2,
            verbose=False,
            n_ctx = N_CTX)

BAD_TOKENS = {llm.token_eos(), llm.token_bos()}

def top2():
    logits = np.array(llm.scores[llm.n_tokens - 1], dtype=np.float64)
    order = np.argsort(-logits)

    good = []
    for tid in order:
        tid = int(tid)
        if tid in BAD_TOKENS:
            continue
        good.append(tid)
        if len(good) == 2:
            break

    return good[0], good[1]

inp = input("Enter your text: ")
sec_key = input("Enter secret key: ")
# Converting input to binary
data = inp.encode(encoding="utf-8");
inp_binary = ''.join(format(byte, '08b') for byte in data)
print(inp_binary)

llm.reset()
llm.eval(llm.tokenize(sec_key.encode("utf-8")))

chosen = []
for bit in inp_binary:
    a, b = top2()
    token = a if bit == "0" else b
    chosen.append(token)
    llm.eval([token])

cover = llm.detokenize(chosen).decode("utf-8", errors="replace")

print(cover)