import requests
from bs4 import BeautifulSoup


def translate_text(text, source_lang='en', target_lang='ru'):
    try:
        url = f"https://api.mymemory.translated.net/get?q={text}&langpair={source_lang}|{target_lang}"
        response = requests.get(url)
        translation = response.json()['responseData']['translatedText']
        return translation
    except:
        return text  # Если перевод не удался, вернем оригинальный текст


def get_russian_words():
    url = "https://randomword.com/"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        english_word = soup.find("div", id="random_word").text.strip()
        english_definition = soup.find("div", id="random_word_definition").text.strip()

        russian_word = translate_text(english_word)
        russian_definition = translate_text(english_definition)

        return {
            "russian_word": russian_word,
            "russian_definition": russian_definition
        }
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


def word_game():
    print("Добро пожаловать в игру")
    while True:
        word_dict = get_russian_words()
        if word_dict is None:
            print("Не удалось получить слово. Попробуйте ещё раз.")
            continue

        word = word_dict.get("russian_word")
        word_definition = word_dict.get("russian_definition")

        print(f"Значение слова - {word_definition}")
        user = input("Что это за слово? ").strip()
        if user.lower() == word.lower():
            print("Все верно!")
        else:
            print(f"Ответ неверный, было загадано это слово - {word}")

        play_again = input("Хотите сыграть еще раз? y/n: ").strip().lower()
        if play_again != "y":
            print("Спасибо за игру!")
            break


word_game()