import numpy as np
from pathlib import Path
from matrixlib import HashMatrix

def save_txt(path: Path, arr: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(" ".join(str(int(v)) for v in row) for row in arr), encoding="utf-8")

def main():
    out = Path(__file__).resolve().parents[1] / "artifacts" / "3.3"
    out.mkdir(parents=True, exist_ok=True)

    n = 5
    rng = np.random.default_rng(0)
    A_arr = rng.integers(0, 10, size=(n, n))
    C_arr = A_arr.copy()
    C_arr[0, 0] += 97
    C_arr[0, 1] -= 97

    B_arr = np.eye(n, dtype=int)
    D_arr = B_arr.copy()

    A = HashMatrix(A_arr)
    B = HashMatrix(B_arr)
    C = HashMatrix(C_arr)
    D = HashMatrix(D_arr)

    assert hash(A) == hash(C) and (A_arr != C_arr).any()
    assert (B_arr == D_arr).all()

    AB = A @ B
    CD_true = C.true_matmul(D)

    save_txt(out / "A.txt", A.data)
    save_txt(out / "B.txt", B.data)
    save_txt(out / "C.txt", C.data)
    save_txt(out / "D.txt", D.data)
    save_txt(out / "AB.txt", AB.data)
    save_txt(out / "CD.txt", CD_true.data)

    (out / "hash.txt").write_text(f"hash(AB)={hash(AB)}\nhash(CD)={hash(CD_true)}\n", encoding="utf-8")

    print(f"Wrote artifacts to {out}")

if __name__ == "__main__":
    main()