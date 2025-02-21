import requests
import difflib
import os

# === KONFIGURACJA ===
URL = "https://example.com"  # Strona do monitorowania
CACHE_FILE = "cache.txt"  # Plik do przechowywania poprzedniej wersji strony
CHANGES_FILE = "changes.txt"  # Plik do zapisu wykrytych zmian

def get_page_source():
    """Pobiera kod źródłowy strony"""
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"❌ Błąd pobierania strony: {e}")
        return None

def load_previous_source():
    """Wczytuje poprzednią wersję strony z pliku"""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as file:
            return file.read()
    return ""

def save_current_source(source):
    """Zapisuje aktualny kod strony do pliku"""
    with open(CACHE_FILE, "w", encoding="utf-8") as file:
        file.write(source)

def detect_changes(old, new):
    """Porównuje starą i nową wersję strony"""
    return '\n'.join(difflib.unified_diff(old.splitlines(), new.splitlines(), lineterm=""))

def main():
    print("🔄 Sprawdzanie strony...")
    new_source = get_page_source()
    if not new_source:
        return

    old_source = load_previous_source()
    
    if old_source and old_source != new_source:
        diff = detect_changes(old_source, new_source)
        print("🔴 Wykryto zmianę na stronie!\n", diff)

        # Zapisujemy zmiany do pliku, który odczyta GitHub Actions
        with open(CHANGES_FILE, "w", encoding="utf-8") as file:
            file.write(diff)
    else:
        print("✅ Brak zmian.")

    save_current_source(new_source)

if __name__ == "__main__":
    main()
