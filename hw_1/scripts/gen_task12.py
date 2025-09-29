import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple


def run_cmd(args, *, input_text: Optional[str] = None) -> Tuple[str, str]:
    cmdline = "$ " + " ".join(map(str, args))
    res = subprocess.run(
        args,
        input=(input_text.encode("utf-8") if input_text is not None else None),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    out = res.stdout.decode("utf-8", errors="replace")
    return cmdline, out


def main():
    root = Path(__file__).resolve().parents[1]
    artifacts = root / "artifacts" / "1.2"
    artifacts.mkdir(parents=True, exist_ok=True)
    out_path = artifacts / "session.txt"

    py = sys.executable
    tail = str((root / "tail.py").resolve())
    test_txt = str((root / "test.txt").resolve())

    logs: list[str] = []

    # 1) Single file
    cmd, out = run_cmd([py, tail, test_txt])
    logs.append(cmd)
    logs.append(out.rstrip("\n"))
    logs.append("")

    # 2) Two files (shows headers between files)
    cmd, out = run_cmd([py, tail, test_txt, test_txt])
    logs.append(cmd)
    logs.append(out.rstrip("\n"))
    logs.append("")

    # 3) From stdin (17 lines)
    stdin_text = "\n".join(str(i) for i in range(1, 19)) + "\n"
    cmd, out = run_cmd([py, tail], input_text=stdin_text)
    logs.append(cmd + "  # via stdin")
    logs.append(out.rstrip("\n"))

    out_path.write_text("\n".join(logs) + "\n", encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
