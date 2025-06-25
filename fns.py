from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time


def main():
    # Инициализация драйвера
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()

    try:
        # Открываем сайт
        driver.get("https://kkt-online.nalog.ru/?")
        print("Сайт открыт...")

        # Ожидаем загрузки элемента выбора модели ККТ
        model_selector = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "select2-selection--single"))
        )
        print("Элемент выбора модели найден...")

        # Кликаем на элемент выбора модели
        model_selector.click()
        print("Открываем список моделей...")

        # Пользователь вводит модель ККТ
        model_name = input("Введите модель ККТ: ")

        # Вводим модель в поиск
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "select2-search__field")))
        search_input.send_keys(model_name)
        print(f"Вводим модель '{model_name}'...")

        # Ожидаем появления результатов и выбираем первый
        try:
            first_result = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "select2-results__option"))
            )
            first_result.click()
            print("Модель выбрана...")
        except:
            print("Модель не найдена!")
            driver.save_screenshot("model_not_found.png")
            return

        # Ожидаем поле для ввода серийного номера
        serial_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "kkt-serial-number"))
        )

        # Пользователь вводит серийный номер
        serial_number = input("Введите заводской номер ККТ: ")
        serial_input.send_keys(serial_number)
        print(f"Вводим серийный номер '{serial_number}'...")

        # Находим и кликаем кнопку "Проверить"
        check_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn_kkt_check"))
        )
        check_button.click()
        print("Нажимаем кнопку 'Проверить'...")

        # Ждем 3 секунды для завершения проверки
        time.sleep(3)

        # Делаем скриншот
        driver.save_screenshot("resultat_proverki.png")
        print("Скриншот сохранен как 'resultat_proverki.png'")

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        driver.save_screenshot("error.png")
    finally:
        # Закрываем браузер
        driver.quit()
        print("Браузер закрыт.")


if __name__ == "__main__":
    main()