import sys
import json

def write_waiting_submission(username: str,
                             paths: list[str]) -> None:
    with open('.scripts/workflows/waiting_submission.jsonl', 'r+', encoding='utf-8') as f:
        existing = [json.loads(line.strip()) for line in f]
        for path in paths:
            new = {"username": username, "path": path}
            if new not in existing:
                f.write(json.dumps(new) + '\n')
        return

def main():
    if len(sys.argv) <= 2:
        sys.exit(1)
    
    username = sys.argv[1]
    paths_to_submit = sys.argv[2:]
    
    write_waiting_submission(username, paths_to_submit)

    return

if __name__ == "__main__":
    main()

# python .scripts/workflows/sample2.py octocat neko/file sushi/file