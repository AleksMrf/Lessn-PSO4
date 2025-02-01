from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def init_driver():
    """Инициализирует веб-драйвер"""
    driver = webdriver.Chrome()  # Убедитесь, что chromedriver добавлен в PATH
    driver.maximize_window()
    return driver

def search_wikipedia(driver, query):
    """Открывает Википедию и выполняет поиск"""
    driver.get("https://ru.wikipedia.org/")
    search_box = driver.find_element(By.NAME, "search")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Ждём загрузки страницы
    return driver.current_url  # Возвращаем URL первой страницы

def get_paragraphs(driver):
    """Получает параграфы текущей статьи"""
    paragraphs = driver.find_elements(By.CSS_SELECTOR, "div.mw-parser-output > p")
    return [p.text for p in paragraphs if p.text.strip()]

def get_related_links(driver):
    """Получает ссылки на связанные статьи"""
    links = driver.find_elements(By.CSS_SELECTOR, "div.mw-parser-output > ul li a")
    related_links = {i + 1: (link.text, link.get_attribute("href")) for i, link in enumerate(links[:10])}
    return related_links

def main():
    driver = init_driver()
    try:
        query = input("Введите запрос для поиска на Википедии: ")
        original_url = search_wikipedia(driver, query)

        while True:
            print("\nЧто вы хотите сделать?")
            print("1. Листать параграфы текущей статьи")
            print("2. Перейти на связанную статью")
            print("3. Вернуться к первоначальному запросу")
            print("4. Выйти из программы")

            choice = input("Ваш выбор: ")

            if choice == "1":
                paragraphs = get_paragraphs(driver)
                if paragraphs:
                    for p in paragraphs:
                        print(f"\n{p}\n")
                        input("Нажмите Enter для продолжения...")
                else:
                    print("Параграфы не найдены.")

            elif choice == "2":
                related_links = get_related_links(driver)
                if related_links:
                    print("\nДоступные связанные статьи:")
                    for idx, (title, _) in related_links.items():
                        print(f"{idx}. {title}")

                    link_choice = int(input("Выберите номер статьи: "))
                    if link_choice in related_links:
                        driver.get(related_links[link_choice][1])
                        time.sleep(2)  # Ждём загрузки страницы
                    else:
                        print("Неверный выбор.")
                else:
                    print("Связанные статьи не найдены.")

            elif choice == "3":
                driver.get(original_url)
                time.sleep(2)  # Ждём загрузки страницы
                print("Возвращаемся к первоначальному запросу.")

            elif choice == "4":
                print("Выход из программы.")
                break

            else:
                print("Неверный выбор. Попробуйте снова.")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()