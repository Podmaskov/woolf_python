path = 'cats_info.txt'

def get_cats_info(path):
    cats_info = []
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                cat_id, name, age = line.strip().split(',')
                cats_info.append({
                    "id": cat_id,
                    "name": name,
                    "age": int(age)
                })
    except FileNotFoundError:
        print(f"File not found: {path}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return cats_info

cats_info = get_cats_info(path)
print(cats_info)
