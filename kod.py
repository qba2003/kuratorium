import requests
from bs4 import BeautifulSoup
import hashlib

URL = "https://ko.poznan.pl/rodzice_uczniowie/konkursy_olimpiady_ru/konkursy_przedmiotowe_ru/2025/01/wyniki-wojewodzkich-konkursow-przedmiotowych-stopien-wojewodzki" # <--- Zmień na stronę, którą chcesz monitorować

def get_page_hash():
    """Pobiera kod źródłowy strony i zwraca jego hash"""
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return hashlib.sha256(soup.prettify().encode()).hexdigest()

def load_last_hash():
    """Wczytuje poprzedni hash strony (jeśli istnieje)"""
    try:
        with open("cache.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def save_new_hash(new_hash):
    """Zapisuje nowy hash strony"""
    with open("cache.txt", "w") as file:
        file.write(new_hash)

def log_changes():
    """Zapisuje zmiany w pliku `changes.txt`"""
    with open("changes.txt", "w") as file:
        file.write(f"Strona {URL} zmieniła się!")

# 1. Pobranie aktualnego kodu strony
new_hash = get_page_hash()

# 2. Wczytanie ostatniego zapisanego hasha
old_hash = load_last_hash()

# 3. Sprawdzenie, czy strona się zmieniła
if new_hash != old_hash:
    log_changes()  # Zapisujemy informację o zmianach
    save_new_hash(new_hash)  # Aktualizujemy zapisany kod strony
