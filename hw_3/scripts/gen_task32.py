import numpy as np
from pathlib import Path
from matrixlib import NumMatrix

def main():
    np.random.seed(0)
    A = NumMatrix(np.random.randint(0, 10, (10, 10)))
    B = NumMatrix(np.random.randint(0, 10, (10, 10)))

    out = Path(__file__).resolve().parents[1] / "artifacts" / "3.2"
    out.mkdir(parents=True, exist_ok=True)

    (A + B).save_txt(out / "matrix+.txt")
    (A * B).save_txt(out / "matrix*.txt")
    (A @ B).save_txt(out / "matrix@.txt")

    print("A:\n", A, sep="")
    print("B:\n", B, sep="")
    print(f"Wrote artifacts to {out}")

if __name__ == "__main__":
    main()