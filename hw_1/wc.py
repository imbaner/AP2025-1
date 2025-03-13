import sys

def wc_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            content_bytes = f.read()
    except FileNotFoundError:
        sys.exit(f"Файл {file_path} не найден.")
    byte_count = len(content_bytes)
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    lines = text.splitlines()
    words = text.split()
    return len(lines), len(words), byte_count

def wc_stdin():
    text = sys.stdin.read()
    byte_count = len(text.encode('utf-8'))
    lines = text.splitlines()
    words = text.split()
    return len(lines), len(words), byte_count

def main():
    args = sys.argv[1:]
    if args:
        total_lines = total_words = total_bytes = 0
        for file_path in args:
            lines, words, bytes_count = wc_file(file_path)
            total_lines += lines
            total_words += words
            total_bytes += bytes_count
            print(f"{lines:7} {words:7} {bytes_count:7} {file_path}")
        if len(args) > 1:
            print(f"{total_lines:7} {total_words:7} {total_bytes:7} total")
    else:
        lines, words, bytes_count = wc_stdin()
        print(f"{lines:7} {words:7} {bytes_count:7}")

if __name__ == '__main__':
    main()