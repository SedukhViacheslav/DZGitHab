import requests
from bs4 import BeautifulSoup
from googletrans import Translator

# Инициализируем переводчик
translator = Translator()


# Создаём функцию, которая будет получать и переводить информацию
def get_russian_words():
    url = "https://randomword.com/"
    try:
        response = requests.get(url)

        # Создаём объект Soup
        soup = BeautifulSoup(response.content, "html.parser")
        # Получаем слово
        english_word = soup.find("div", id="random_word").text.strip()
        # Получаем описание слова
        english_definition = soup.find("div", id="random_word_definition").text.strip()

        # Переводим слово и определение на русский
        russian_word = translator.translate(english_word, src='en', dest='ru').text
        russian_definition = translator.translate(english_definition, src='en', dest='ru').text

        return {
            "russian_word": russian_word,
            "russian_definition": russian_definition
        }
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


# Создаём функцию, которая будет делать саму игру
def word_game():
    print("Добро пожаловать в игру")
    while True:
        # Получаем переведённое слово и определение
        word_dict = get_russian_words()
        if word_dict is None:
            print("Не удалось получить слово. Попробуйте ещё раз.")
            continue

        word = word_dict.get("russian_word")
        word_definition = word_dict.get("russian_definition")

        # Начинаем игру
        print(f"Значение слова - {word_definition}")
        user = input("Что это за слово? ").strip()
        if user.lower() == word.lower():
            print("Все верно!")
        else:
            print(f"Ответ неверный, было загадано это слово - {word}")

        # Создаём возможность закончить игру
        play_again = input("Хотите сыграть еще раз? y/n: ").strip().lower()
        if play_again != "y":
            print("Спасибо за игру!")
            break


word_game()