import numpy as np
from pathlib import Path
from matrixlib import MatrixSimple

def main():
    np.random.seed(0)
    A = MatrixSimple.from_iter(np.random.randint(0, 10, (10, 10)))
    B = MatrixSimple.from_iter(np.random.randint(0, 10, (10, 10)))

    out = Path(__file__).resolve().parents[1] / "artifacts" / "3.1"
    out.mkdir(parents=True, exist_ok=True)

    (out / "matrix+.txt").write_text((A + B).to_text(), encoding="utf-8")
    (out / "matrix*.txt").write_text((A * B).to_text(), encoding="utf-8")
    (out / "matrix@.txt").write_text((A @ B).to_text(), encoding="utf-8")
    print(f"Wrote artifacts to {out}")

if __name__ == "__main__":
    main()