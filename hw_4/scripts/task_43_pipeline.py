import sys, time, codecs
import threading
from datetime import datetime
from pathlib import Path
import multiprocessing as mp
from collections import deque

def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

SENTINEL = "::QUIT::"

def proc_A(q_in: mp.Queue, q_AB: mp.Queue):
    buf = deque()
    stop = threading.Event()

    def reader():
        while True:
            msg = q_in.get()
            if msg == SENTINEL:
                buf.append(SENTINEL)
                break
            buf.append(msg)

    def forwarder():
        while not stop.is_set():
            if buf:
                msg = buf.popleft()
                if msg == SENTINEL:
                    q_AB.put(SENTINEL)
                    break
                low = msg.lower()
                q_AB.put(low)
            time.sleep(5)

    t1 = threading.Thread(target=reader, daemon=True)
    t2 = threading.Thread(target=forwarder, daemon=True)
    t1.start(); t2.start()
    t1.join(); t2.join()
    stop.set()

def proc_B(q_AB: mp.Queue, q_back: mp.Queue):
    while True:
        msg = q_AB.get()
        if msg == SENTINEL:
            q_back.put(SENTINEL)
            break
        enc = codecs.decode(msg, "rot_13")
        sys.stdout.write(f"[{ts()}] B OUT: {enc}\n")
        sys.stdout.flush()
        q_back.put(f"[{ts()}] {enc}")

def main():
    mp.set_start_method("spawn", force=True)
    q_in = mp.Queue(); q_AB = mp.Queue(); q_back = mp.Queue()

    A = mp.Process(target=proc_A, args=(q_in, q_AB), name="A")
    B = mp.Process(target=proc_B, args=(q_AB, q_back), name="B")
    A.start(); B.start()

    out_dir = Path(__file__).resolve().parents[1] / "artifacts" / "4.3"
    out_dir.mkdir(parents=True, exist_ok=True)
    log_path = out_dir / "session.txt"
    log = open(log_path, "w", encoding="utf-8")

    print("Type lines and press Enter. Ctrl-D (EOF) to quit.")
    try:
        for line in sys.stdin:
            line = line.rstrip("\n")
            stamp = f"[{ts()}] MAIN IN: {line}"
            print(stamp)
            log.write(stamp + "\n")
            q_in.put(line)
    except EOFError:
        pass
    finally:
        q_in.put(SENTINEL)

    while True:
        msg = q_back.get()
        if msg == SENTINEL:
            break
        log.write(msg + "\n")
        log.flush()

    A.join(); B.join()
    log.close()
    print(f"Log saved to {log_path}")

if __name__ == "__main__":
    main()