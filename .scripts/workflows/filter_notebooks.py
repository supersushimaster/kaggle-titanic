"""
# スクリプトの概要
    - コミットのusernameとノートブックファイルパスを受け取り、
      Config.need_submission=True とされているノートブックのみを抽出して、
      waiting_submission.json に情報を書き込みます。

# 呼び出しと引数
    - 以下のように、シェルからコミットのノートブック情報を受け取って実行されます。
          python filter_notebook.py octocat notebook/models/lightgbm/lgbm001
    - 第1引数はスクリプトのファイルパスです。
    - 第2引数はコミッターのusernameです。
      submissionを行うAPIトークンは、GitHub Secrets にusernameと紐づけて保存されるため必要です。
    - 第3引数以降はコミットで追加／修正されたモデルのファイルパスですが、
      need_submission がTrueになっているか不明な状態です。

# 処理
    - ノートブックのパスを1つずつ check_notebook() 関数に渡します。
        - この関数はノートブックを読み込み、 Config.need_submission に定義されているのと同じ真理値を返します。
        - この関数の返り値がTrueになったノートブックを、リスト paths_to_submit に格納します。

    - 次に、paths_to_submit とusernameを write_waiting_submission() 関数に渡します。
        - この関数は waiting_submission.jsonl（submissionが必要だがまだ行われていないノートブックの情報）に、
              {"username": "octocat", "path": "notebooks/models/lightgbm/lgbm001"}
          という形のJSONオブジェクトを追加します。

# 返り値
    - 標準出力には追加したJSON配列が流され、シェルスクリプトで使います。
    - 処理の結果は waiting_submission.jsonl に書き込まれ、submissionを行うモジュールで使います。

# 必要なもの
   - notebook/models/ への読み込み権限。
   - .scripts/workflows/waiting_submission.jsonl への読み書き権限。
   - 実行環境にPythonとnbformatがインストールされていること。
"""

import nbformat
import ast
import sys
import json

def check_notebook(path: str) -> bool:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
    except FileNotFoundError as e:
        print(f"ファイルが見つかりませんでした。\n入力値 {path} はスキップされました。\n{e}", file=sys.stderr)
        return False
    
    for cell in notebook.cells:
        if cell.cell_type != 'code':
            continue

        code = cell.source

        if 'class Config' not in code:
            continue
    
        try:
            tree = ast.parse(code)
        except SyntaxError:
            continue
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == 'Config':
                for statement in node.body:                           # Configクラス定義の内部を解析します。
                    if isinstance(statement, ast.Assign):
                        for target in statement.targets:              # 代入対象のクラス属性を解析します。
                            if (isinstance(target, ast.Name)          # need_submission への代入では、メソッドやタプルなどを使ってはいけません。
                                and target.id == 'need_submission'
                                and statement.value.value is True):
                                print(path, 'はsubmissionリストに追加されます。', file=sys.stderr)
                                return True
    print('次のファイルはsubmissionリストに追加されませんでした：', path, file=sys.stderr)
    return False

def write_waiting_submission(username: str,
                             paths: list[str]) -> None:
    with open('.scripts/workflows/waiting_submission.jsonl', 'r+', encoding='utf-8') as f:
        added = []
        existing = [json.loads(line.strip()) for line in f]
        print('現在の.jsonlファイル：\n', existing, file=sys.stderr)
        for path in paths:
            new = {"username": username, "path": path}
            if new not in existing:
                print('newを書き込みます。', file=sys.stderr)
                added.append(new)
                f.write(json.dumps(new) + '\n')
    return added

def main():
    if len(sys.argv) <= 2:
        sys.exit(1)
    
    username = sys.argv[1]
    paths = sys.argv[2:]

    paths_to_submit = []
    for path in paths:
        if check_notebook(path):
            paths_to_submit.append(path)
    
    added = write_waiting_submission(username, paths_to_submit)
    print(added)
    return

if __name__ == "__main__":
    main()