from llama_cpp import Llama
import numpy as np
from pathlib import Path

MODELS_DIR = Path(__file__).parent / "models"

N_CTX = 2048

def choose_model():
    files = sorted(MODELS_DIR.glob("*.gguf"))

    if not files:
        raise SystemExit(f"No models in {MODELS_DIR}")

    if len(files) == 1:
        print(f"Models: {files[0].name}")
        return str(files[0])

    print("\nAvailable models:")
    for i, f in enumerate(files, 1):
        size = f.stat().st_size / 1024**3
        print(f"  {i}. {f.name}  ({size:.1f} GB)")

    while True:
        raw = input("\nNumber: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(files):
            return str(files[int(raw) - 1])
        print("Wrong number")

MODEL_PATH = choose_model()


llm = Llama(model_path = MODEL_PATH,
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