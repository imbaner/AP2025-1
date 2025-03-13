import sys

def tail_file(file_path, n):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        sys.exit(f"Файл {file_path} не найден.")
    return lines[-n:]

def main():
    args = sys.argv[1:]
    if args:
        for idx, file_path in enumerate(args):
            if len(args) > 1:
                print(f"==> {file_path} <==")
            for line in tail_file(file_path, 10):
                print(line, end='')
            if len(args) > 1 and idx != len(args) - 1:
                print()
    else:
        lines = sys.stdin.readlines()
        for line in lines[-17:]:
            print(line, end='')

if __name__ == '__main__':
    main()