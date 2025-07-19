import pandas as pd

# Загружаем данные из файла dz.csv
df = pd.read_csv('dz.csv')

# Группируем данные по городам и вычисляем среднюю зарплату
average_salary_by_city = df.groupby('City')['Salary'].mean().reset_index()

# Выводим результат
print(average_salary_by_city)