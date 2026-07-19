from llama_cpp import Llama
import numpy as np

MODEL_PATH = '/home/adam/stego/tinyllama-1.1b-chat-v1.0-q4_k_m.gguf'
N_CTX = 2048

lm = Llama(model_path = MODEL_PATH,
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
        piece = llm.detokenize([tid])
        if b"\n" in piece or b"\r" in piece:
            continue
        good.append(tid)
        if len(good) == 2:
            break

    return good[0], good[1]


cover = input("Paste container: ")
sec_key = input("Enter secret key: ")

remaining = cover.encode("utf-8")

llm.reset()
llm.eval(llm.tokenize(sec_key.encode("utf-8")))

bits = ""

while remaining:
    a, b = top2()

    piece_a = llm.detokenize([a])
    piece_b = llm.detokenize([b])
    hit_a = remaining.startswith(piece_a)
    hit_b = remaining.startswith(piece_b)

    if hit_a and hit_b:
        if len(piece_a) >= len(piece_b):
            hit_b = False
        else:
            hit_a = False

    if hit_a:
        bits += "0"
        token, piece = a, piece_a
    elif hit_b:
        bits += "1"
        token, piece = b, piece_b
    else:
        print("\nSomething's wrong! Check the container and try again")
        print(f"Expected:    {piece_a!r} or {piece_b!r}")
        print(f"Reality: {remaining[:20]!r}")
        break

    remaining = remaining[len(piece):]
    llm.eval([token])

usable = len(bits) - (len(bits) % 8)
data = bytes(int(bits[i:i + 8], 2) for i in range(0, usable, 8))

print(f"\Bit: {len(bits)}")
print("Message:", data.decode("utf-8", errors="replace"))