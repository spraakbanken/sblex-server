import sys

from sblex.fm.morphology import MemMorphology


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "assets/testing/saldo.lex"
    print(f"loading from {arg}")
    MemMorphology.from_path(arg)


if __name__ == "__main__":
    main()
