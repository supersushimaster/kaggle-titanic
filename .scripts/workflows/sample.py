def main():
    path = '.scripts/workflows/available_submissions.txt'
    try:
        with open(path, 'r', encoding='utf-8') as f:
            print(f.readline())
    except FileNotFoundError as e:
        print(f"ファイルが見つかりませんでした。\n入力値 {path} はスキップされました。\n{e}")
        return False

if __name__ == '__main__':
    main()