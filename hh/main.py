import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.options import Options

# Настройки браузера
options = Options()
options.headless = False  # Для отладки оставляем видимым
driver = webdriver.Firefox(options=options)


def accept_cookies(driver):
    try:
        cookie_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-qa="cookies-policy-warning-accept"]'))
        )
        cookie_btn.click()
        print("Cookies приняты")
    except:
        pass


def scroll_page(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def parse_salary(vacancy):
    try:
        # Точно указанный селектор для зарплаты
        salary_element = vacancy.find_element(By.CSS_SELECTOR,
                                              'span.magritte-text___pbpft_3-0-47.magritte-text_style-primary___AQ7MW_3-0-47.magritte-text_typography-label-1-regular___pi3R-_3-0-47')
        salary_text = salary_element.text
        # Очищаем текст от лишних пробелов и неразрывных пробелов
        return ' '.join(salary_text.replace('\u202f', ' ').split())
    except NoSuchElementException:
        return "Не указана"


try:
    url = "https://hh.ru/search/vacancy?text=кассовой&area=78"
    print(f"Открываем страницу: {url}")
    driver.get(url)

    accept_cookies(driver)

    print("Ожидаем загрузки вакансий...")
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy"]'))
        )
    except TimeoutException:
        print("Вакансии не загрузились. Проверьте вручную:")
        print(url)
        driver.save_screenshot('debug.png')
        raise

    print("Прокручиваем страницу...")
    scroll_page(driver)
    time.sleep(3)

    vacancies = driver.find_elements(By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy"]')
    print(f"Найдено вакансий: {len(vacancies)}")

    parsed_data = []
    for i, vacancy in enumerate(vacancies, 1):
        try:
            title = vacancy.find_element(By.CSS_SELECTOR, '[data-qa="serp-item__title"]').text
            company = vacancy.find_element(By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy-employer"]').text
            salary = parse_salary(vacancy)
            link = vacancy.find_element(By.CSS_SELECTOR, '[data-qa="serp-item__title"]').get_attribute('href')

            parsed_data.append([title, company, salary, link])
            print(f"{i}. {title[:50]}... | {company[:20]}... | {salary}")

        except Exception as e:
            print(f"Ошибка в вакансии #{i}: {str(e)}")
            continue

    if parsed_data:
        filename = "hh_yaroslavl_tehnik.csv"
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['Название', 'Компания', 'Зарплата', 'Ссылка'])
            writer.writerows(parsed_data)
        print(f"\nСохранено {len(parsed_data)} вакансий в {filename}")
    else:
        print("\nНе найдено подходящих вакансий")

except Exception as e:
    print(f"\nКритическая ошибка: {str(e)}")
    driver.save_screenshot('error.png')
    print("Скриншот сохранен как error.png")

finally:
    input("\nНажмите Enter для закрытия браузера...")
    driver.quit()