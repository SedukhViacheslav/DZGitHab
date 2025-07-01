from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time


def main():
    # Настройка драйвера с опциями
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Открываем сайт
        driver.get("https://kkt-online.nalog.ru/?")
        print("Сайт открыт...")
        time.sleep(2)  # Даем странице полностью загрузиться

        # Кликаем на выпадающий список моделей
        dropdown = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".select2-selection--single"))
        )
        ActionChains(driver).move_to_element(dropdown).click().perform()
        print("Открыли список моделей...")

        # Вводим модель
        model_name = input("Введите модель KKT: ")

        # Ожидаем появление поля поиска
        search_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".select2-search__field"))
        )

        # Медленно вводим текст (имитация ручного ввода)
        for char in model_name:
            search_field.send_keys(char)
            time.sleep(0.15)

        # Ждем появления результатов
        time.sleep(2)

        # Выбираем первый вариант из списка
        first_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".select2-results__option"))
        )
        first_option.click()
        print(f"Выбрана модель: {model_name}")

        # Дальнейшие действия с серийным номером...

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        driver.save_screenshot("error.png")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()