path = 'month_salaries.txt'
def total_salary(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            total = 0
            count = 0
            for line in file:
                salary = line.strip().split(',')
                total += int(salary)
                count += 1
            average = total // count if count > 0 else 0
            return total, average
    except FileNotFoundError:
        print(f"File not found: {path}")
        return 0, 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0, 0


total, average = total_salary(path)
print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")
