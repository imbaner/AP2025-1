import math, os, time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pathlib import Path

def integrate_sequential(f, a, b, *, n_iter=10_000_000):
    acc = 0.0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc

def _chunk_sum(f, a, step, i0, i1):
    acc = 0.0
    for i in range(i0, i1):
        acc += f(a + i * step) * step
    return acc

def integrate_parallel(f, a, b, *, n_iter=10_000_000, n_jobs=1, executor="thread"):
    step = (b - a) / n_iter
    base = n_iter // n_jobs
    ranges = []
    start = 0
    for j in range(n_jobs):
        end = start + base + (1 if j < (n_iter % n_jobs) else 0)
        ranges.append((start, end))
        start = end

    ex_cls = ThreadPoolExecutor if executor == "thread" else ProcessPoolExecutor
    with ex_cls(max_workers=n_jobs) as ex:
        futs = [ex.submit(_chunk_sum, f, a, step, i0, i1) for (i0, i1) in ranges]
        return sum(f.result() for f in futs)

def main():
    out_dir = Path(__file__).resolve().parents[1] / "artifacts" / "4.2"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "integrate_timings.csv"

    cpu = os.cpu_count() or 2
    max_jobs = cpu * 2
    a, b = 0.0, math.pi / 2

    lines = ["n_jobs,kind,seconds,value"]

    t0 = time.perf_counter()
    v0 = integrate_sequential(math.cos, a, b, n_iter=10_000_000)
    t1 = time.perf_counter() - t0
    lines.append(f"1,sequential,{t1:.3f},{v0:.9f}")

    for n_jobs in range(1, max_jobs + 1):
        t0 = time.perf_counter()
        v_t = integrate_parallel(math.cos, a, b, n_iter=10_000_000, n_jobs=n_jobs, executor='thread')
        t_t = time.perf_counter() - t0
        lines.append(f"{n_jobs},threads,{t_t:.3f},{v_t:.9f}")

        t0 = time.perf_counter()
        v_p = integrate_parallel(math.cos, a, b, n_iter=10_000_000, n_jobs=n_jobs, executor='process')
        t_p = time.perf_counter() - t0
        lines.append(f"{n_jobs},processes,{t_p:.3f},{v_p:.9f}")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()