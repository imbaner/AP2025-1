import sys
from pathlib import Path


WHITESPACE = set(b" \t\r\n\v\f")


def count_stream(stream) -> tuple[int, int, int]:
    bufsize = 1024 * 64
    total_bytes = 0
    total_lines = 0
    total_words = 0
    in_word = False

    while True:
        chunk = stream.read(bufsize)
        if not chunk:
            break
        total_bytes += len(chunk)
        total_lines += chunk.count(b"\n")
        for b in chunk:
            if b in WHITESPACE:
                in_word = False
            else:
                if not in_word:
                    total_words += 1
                    in_word = True
    return total_lines, total_words, total_bytes


def wc_file(path: Path) -> tuple[int, int, int]:
    with path.open("rb") as f:
        return count_stream(f)


def wc_stdin() -> tuple[int, int, int]:
    return count_stream(sys.stdin.buffer)


def main() -> None:
    args = sys.argv[1:]
    if args:
        total_lines = total_words = total_bytes = 0
        had_error = False
        for file_path in args:
            p = Path(file_path)
            try:
                lines, words, bytes_count = wc_file(p)
            except FileNotFoundError:
                sys.stderr.write(f"wc: {file_path}: No such file or directory\n")
                had_error = True
                continue
            total_lines += lines
            total_words += words
            total_bytes += bytes_count
            print(f"{lines:7} {words:7} {bytes_count:7} {file_path}")
        if len(args) > 1:
            print(f"{total_lines:7} {total_words:7} {total_bytes:7} total")
        if had_error:
            sys.exit(1)
    else:
        lines, words, bytes_count = wc_stdin()
        print(f"{lines:7} {words:7} {bytes_count:7}")


if __name__ == '__main__':
    main()