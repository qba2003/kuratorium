import requests
from bs4 import BeautifulSoup

URL = "https://ko.poznan.pl/rodzice_uczniowie/konkursy_olimpiady_ru/konkursy_przedmiotowe_ru/2025/01/wyniki-wojewodzkich-konkursow-przedmiotowych-stopien-wojewodzki/"

def get_pdf_count():
    """Pobiera kod HTML strony i liczy wystąpienia 'pdf'"""
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.prettify().lower().count("pdf")  # Zlicza "pdf" w kodzie strony

def load_last_count():
    """Wczytuje ostatnią zapisaną liczbę PDF-ów (jeśli istnieje)"""
    try:
        with open("cache.txt", "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return -1  # -1 oznacza brak danych

def save_new_count(count):
    """Zapisuje nową liczbę PDF-ów"""
    with open("cache.txt", "w") as file:
        file.write(str(count))

def log_changes(new_count):
    """Zapisuje wykryte różnice do `changes.txt`"""
    with open("changes.txt", "w") as file:
        file.write(f"Liczba wystąpień 'pdf' na stronie zmieniła się!\n")
        file.write(f"Nowa liczba: {new_count}\n")
        file.write(f"Sprawdź tutaj: {URL}\n")

# 1. Pobranie aktualnej liczby "pdf" w HTML
new_count = get_pdf_count()

# 2. Wczytanie poprzedniej wartości
old_count = load_last_count()

# 3. Sprawdzenie, czy liczba się zmieniła
if new_count != old_count:
    log_changes(new_count)  # Zapisujemy zmiany
    save_new_count(new_count)  # Aktualizujemy zapisane dane
