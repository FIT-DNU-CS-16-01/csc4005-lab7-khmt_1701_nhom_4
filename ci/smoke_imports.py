import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

def main():
    import src.dataset
    import src.models
    import src.metrics
    import src.runtime
    import src.utils
    print("Import smoke test passed.")

if __name__ == "__main__":
    main()
