import requests
from bs4 import BeautifulSoup

URL = "https://ko.poznan.pl/rodzice_uczniowie/konkursy_olimpiady_ru/konkursy_przedmiotowe_ru/2025/01/wyniki-wojewodzkich-konkursow-przedmiotowych-stopien-wojewodzki/"  # Zmień na stronę, którą chcesz monitorować

def get_page_content():
    """Pobiera kod HTML strony"""
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.prettify()  # Zwraca sformatowany kod HTML

def load_last_content():
    """Wczytuje poprzedni kod strony (jeśli istnieje)"""
    try:
        with open("cache.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return ""

def save_new_content(content):
    """Zapisuje nowy kod HTML strony"""
    with open("cache.txt", "w", encoding="utf-8") as file:
        file.write(content)

def log_changes(new_content):
    """Zapisuje wykryte różnice do pliku `changes.txt`"""
    with open("changes.txt", "w", encoding="utf-8") as file:
        file.write("Strona zmieniła się! Oto nowy kod HTML:\n\n")
        file.write(new_content)

# 1. Pobranie aktualnego kodu HTML strony
new_content = get_page_content()

# 2. Wczytanie ostatnio zapisanego kodu HTML
old_content = load_last_content()

# 3. Sprawdzenie, czy strona się zmieniła
if new_content != old_content:
    log_changes(new_content)  # Zapisujemy zmiany
    save_new_content(new_content)  # Aktualizujemy zapisany kod strony
