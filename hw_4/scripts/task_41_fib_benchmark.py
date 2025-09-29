import time, threading, multiprocessing as mp
from pathlib import Path

def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

def worker(n: int, idx: int, out_list):
    out_list[idx] = fib(n)

def run_sync(n: int, reps: int):
    start = time.perf_counter()
    sink = 0
    for _ in range(reps):
        sink ^= fib(n)
    return time.perf_counter() - start, sink

def run_threads(n: int, reps: int):
    start = time.perf_counter()
    results = [None]*reps
    threads = [threading.Thread(target=worker, args=(n, i, results)) for i in range(reps)]
    for t in threads: t.start()
    for t in threads: t.join()
    return time.perf_counter() - start, sum(r or 0 for r in results)

def run_processes(n: int, reps: int):
    start = time.perf_counter()
    with mp.Manager() as mgr:
        results = mgr.list([None]*reps)
        procs = [mp.Process(target=worker, args=(n, i, results)) for i in range(reps)]
        for p in procs: p.start()
        for p in procs: p.join()
        total = sum(r or 0 for r in results)
    return time.perf_counter() - start, total

def main():
    import argparse
    mp.set_start_method("spawn", force=True)
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=36)
    ap.add_argument("--reps", type=int, default=10)
    args = ap.parse_args()

    out_dir = Path(__file__).resolve().parents[1] / "artifacts" / "4.1"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "timings.txt"

    ts_sync, _ = run_sync(args.n, args.reps)
    ts_thr, _ = run_threads(args.n, args.reps)
    ts_proc, _ = run_processes(args.n, args.reps)

    report = (
        f"Fibonacci benchmark (n={args.n}, reps={args.reps})\n"
        f"sync:        {ts_sync:.3f} s\n"
        f"threading:   {ts_thr:.3f} s\n"
        f"processing:  {ts_proc:.3f} s\n"
    )
    out_path.write_text(report, encoding="utf-8")
    print(report, end="")

if __name__ == "__main__":
    main()