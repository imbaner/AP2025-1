import sys

def main():
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            sys.exit(f"Файл {file_name} не найден.")
    else:
        lines = sys.stdin.readlines()

    for i, line in enumerate(lines, start=1):
        sys.stdout.write(f"{i:6}\t{line}")

if __name__ == '__main__':
    main()