import json
def main():
    data = [{"octo": "cat", "shiba": "inu"}, {"cat": "octo", "inu": "shiba"}]
    print_data = str(data).strip().replace('[', '').replace(']', '')
    print(print_data)
    return

if __name__ == "__main__":
    main()