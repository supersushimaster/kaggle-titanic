import sys
def main():
    with open('.scripts/workflows/sample.txt', 'r+', encoding='utf-8') as f:
        f.read()
        print('r+権限で書き込みを開始します。', file=sys.stderr)
        print('printでaaaと書きます。', file=sys.stderr)
        print('aaa', file=f)
        print('writeでbbb, cccと書きます。', file=sys.stderr)
        f.write('bbb\n')
        f.write('ccc' + '\n')
    print(44)
    return

if __name__ == "__main__":
    main()