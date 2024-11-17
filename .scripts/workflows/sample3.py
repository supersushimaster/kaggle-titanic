def main():
    with open('.scripts/workflows/sample.txt', 'r+', encoding='utf-8') as f:
        f.read()
        print('r+権限で書き込みを開始します。')
        print('printでaaaと書きます。')
        print('aaa', file=f)
        print('writeでbbb, cccと書きます。')
        f.write('bbb\n')
        f.write('ccc' + '\n')
        return

if __name__ == "__main__":
    main()