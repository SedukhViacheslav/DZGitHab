import pandas as pd

# Загрузка данных из CSV-файла в DataFrame
df = pd.read_csv('World-happiness-report-2024.csv')

# Вывод первых 5 строк данных
print("Первые 5 строк данных:")
print(df.head(5))

# Вывод информации о данных
print("\nИнформация о данных:")
print(df.info())

# Вывод статистического описания данных
print("\nСтатистическое описание данных:")
print(df.describe())