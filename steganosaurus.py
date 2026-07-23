import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent

ACTIONS = [
    ("Hide a message", "encode.py"),
    ("Reveal a message", "decode.py"),
]

BANNER = r"""
 _______________________________________
|                                       |
|┏━┛━┏┛┏━┛┏━┛┏━┃┏━ ┏━┃┏━┛┏━┃┃ ┃┏━┃┃ ┃┏━┛|
|━━┃ ┃ ┏━┛┃ ┃┏━┃┃ ┃┃ ┃━━┃┏━┃┃ ┃┏┏┛┃ ┃━━┃|
|━━┛ ┛ ━━┛━━┛┛ ┛┛ ┛━━┛━━┛┛ ┛━━┛┛ ┛━━┛━━┛|
|_______________________________________|
"""


def menu():
    #Menu - pick one action
    print(BANNER)

    for i, (label, _) in enumerate(ACTIONS, 1):
        print(f"  {i}. {label}")
    print("  q. Quit")

    while True:
        raw = input("\n> ").strip().lower()

        if raw in ("q", "quit", "exit"):
            return None

        if raw.isdigit() and 1 <= int(raw) <= len(ACTIONS):
            return ACTIONS[int(raw) - 1][1]

        print("Pick a number from the list, or q to quit.")


def run(script):
    #Run script in the same interpreter
    path = HERE / script

    if not path.exists():
        print(f"\nMissing file: {path}")
        return

    print()
    # sys.executable keeps inside the active virtualenv
    subprocess.run([sys.executable, str(path)])


def main():
    while True:
        script = menu()

        if script is None:
            print("\nBye.")
            return

        try:
            run(script)
        except KeyboardInterrupt:
            print("\nInterrupted.")

        input("\nPress Enter to return to the menu...")
        print("\n" * 2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye.")