<p align="center">
  <img src="assets/logo.png" width="120" alt="SteganoSaurus">
</p>

<h1 align="center">SteganoSaurus</h1>

<p align="center">
  Hides a message inside ordinary text written by a local language model.
</p>

---

> **Status: v0.1, work in progress.** Learning project, unaudited.

## What it is

Conventional encryption produces obvious gibberish - anyone can tell something is being hidden. SteganoSaurus hides the **existence** of the message: the output is readable text that looks like plain model output.

Decoding requires the same model and the same context prompt.

## How it works

At each step the model proposes a ranked list of likely continuations. Both sides running the same model see the **same list**. The message is encoded not as letters but as a *choice* from that list: bit `0` picks the first candidate, bit `1` picks the second.

The receiver runs the text through the same model, observes which candidate was chosen, and recovers the bits.

## Install

```bash
git clone https://github.com/adambovzdarenko/SteganoSaurus.git
cd SteganoSaurus
python -m venv venv && source venv/bin/activate
pip install llama-cpp-python numpy
```

The model is not bundled - download a `.gguf` and put into the "/models" folder.

## Usage

```bash
python encode.py
python decode.py
```

## Threat model

**Protects against:** a passive observer who sees ordinary text and has no reason to suspect a payload.

**Does not protect against:** an adversary who knows the method and your model; traffic analysis; statistical steganalysis given many samples; coercion to reveal the prompt.

In v0.1 the prompt acts as the shared secret, and prompts are brute-forceable. Real cryptographic strength arrives in v0.2 with ChaCha20 and Argon2id.

## Roadmap

- [x] v0.1 - top-2, one bit per token
- [ ] v0.2 - encryption, top-k, 3 bits per token
- [ ] v1 - arithmetic coding
- [ ] v2 - ?

## Notes

- The better the model you use, the more natural the output will look.
- Do not use this for anything other than learning and your own privacy. NEVER USE IT FOR CRIMINAL PURPOSES. AND EVEN WORSE - DO NOT SELL SOFTWARE BUILT ON THIS METHOD. PRIVACY IS A HUMAN RIGHT, NOT A PRODUCT!

## Reference

Ziegler, Deng, Rush. *Neural Linguistic Steganography*, EMNLP 2019.
https://aclanthology.org/D19-1115/

## License

AGPL-3.0
