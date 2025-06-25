from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time


def get_paragraphs(driver):
    """Получает все параграфы текущей статьи"""
    paragraphs = driver.find_elements(By.TAG_NAME, "p")
    return [p.text for p in paragraphs if p.text.strip()]


def get_links(driver):
    """Получает все внутренние ссылки текущей статьи"""
    main_content = driver.find_element(By.ID, "bodyContent")
    links = main_content.find_elements(By.TAG_NAME, "a")
    return [link for link in links if
            link.get_attribute("href") and "/wiki/" in link.get_attribute("href") and ":" not in link.get_attribute(
                "href")]


def browse_paragraphs(driver):
    """Функция для листания параграфов"""
    paragraphs = get_paragraphs(driver)
    for i, p in enumerate(paragraphs, 1):
        print(f"\nПараграф {i}:\n{p}")
        if i % 3 == 0 and i != len(paragraphs):
            input("\nНажмите Enter для продолжения...")
    print("\nКонец статьи.")


def browse_links(driver):
    """Функция для выбора и перехода по ссылкам"""
    links = get_links(driver)
    unique_links = []
    seen = set()

    for link in links:
        href = link.get_attribute("href")
        if href not in seen:
            seen.add(href)
            unique_links.append(link)

    print("\nДоступные ссылки:")
    for i, link in enumerate(unique_links[:10], 1):  # Ограничим выбор 10 ссылками
        print(f"{i}. {link.text} ({link.get_attribute('href')})")

    while True:
        try:
            choice = int(input("\nВыберите номер ссылки для перехода (или 0 для отмены): "))
            if choice == 0:
                return None
            elif 1 <= choice <= len(unique_links[:10]):
                return unique_links[choice - 1]
            else:
                print("Некорректный ввод. Попробуйте снова.")
        except ValueError:
            print("Пожалуйста, введите число.")


def main():
    # Инициализация драйвера
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()

    # Запрос пользователя
    query = input("Введите ваш запрос для поиска в Википедии: ")
    driver.get(f"https://ru.wikipedia.org/wiki/{query}")

    current_page = query

    while True:
        print(f"\nТекущая страница: {current_page}")
        print("\nВыберите действие:")
        print("1. Листать параграфы текущей статьи")
        print("2. Перейти на одну из связанных страниц")
        print("3. Выйти из программы")

        choice = input("Ваш выбор (1-3): ")

        if choice == "1":
            browse_paragraphs(driver)
        elif choice == "2":
            link = browse_links(driver)
            if link:
                link.click()
                current_page = driver.current_url.split("/wiki/")[-1]
                time.sleep(2)  # Даем странице загрузиться
        elif choice == "3":
            print("Выход из программы...")
            break
        else:
            print("Некорректный ввод. Пожалуйста, выберите 1, 2 или 3.")

    driver.quit()


if __name__ == "__main__":
    main()